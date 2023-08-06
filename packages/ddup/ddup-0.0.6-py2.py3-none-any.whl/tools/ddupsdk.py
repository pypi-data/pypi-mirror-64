import argparse
import json
import multiprocessing
import os
import os.path as osp
import sys
import threading
from time import time

import h5py
import numpy as np
import torch
from ddup.utils.chunks import get_chunks
from ddup.utils.hash import get_hash


class InvalidInputException(Exception):
    pass


def parse_args():
    parser = argparse.ArgumentParser(
        description="""
        Given two image lists, compare the phash of the images in the
        first list to those in the second to find dulplicate pairs.\n
        Result will be saved in the given dir.
        """,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "--path1",
        help="path of the first image list",
        default=None,
        type=str,
    )
    parser.add_argument(
        "--list1",
        help="The first image list",
        default=None,
        nargs="+",
    )
    parser.add_argument(
        "--path2",
        help="path of the second image list",
        default=None,
        type=str)
    parser.add_argument(
        "--list2",
        help="The second image list",
        default=None,
        nargs="+",
    )
    parser.add_argument(
        "--out",
        help="Folder path to save the results",
        default="./ddup_output",
        type=str)
    parser.add_argument(
        "--log",
        help="Add this to show detail log",
        default=False,
        action="store_true")
    if len(sys.argv) == 1:
        parser.print_help()
    return parser.parse_args()


def load_config(args):
    """
    Given the arguemnts, load, check and initialize the configs.

    Args:
        args (argument): `list1`, `path1`, `list2`, `path2`, `out`, `log`
    """
    if args.list1 is None and args.path1 is None:
        raise InvalidInputException("You should provide either list1 or path1")
    elif args.list1 is not None and args.path1 is not None:
        raise InvalidInputException(
            "You can only provide one of list1 or path1")
    else:
        if args.list1 is not None:
            if len(args.list1) <= 0:
                raise InvalidInputException("list1 should not be empty")
            input1 = args.list1
        else:
            if os.path.isdir(args.path1):
                raise InvalidInputException("path1 should be a file.")
            if not os.path.exists(args.path1):
                raise FileNotFoundError("path1 does not exist")
            input1 = args.path1
    if args.list2 is None and args.path2 is None:
        if args.list1 is not None:
            args.list2 = args.list1
            input2 = args.list2
        elif args.path1 is not None:
            args.path2 = args.path1
            input2 = args.path2
    elif args.list2 is not None and args.path2 is not None:
        raise InvalidInputException(
            "You can only provide one of list2 or path2")
    else:
        if args.list2 is not None:
            if len(args.list2) <= 0:
                raise InvalidInputException("list2 should not be empty")
            input2 = args.list2
        else:
            if os.path.isdir(args.path2):
                raise InvalidInputException("path2 should be a file.")
            if not os.path.exists(args.path2):
                raise InvalidInputException("path2 does not exist")
            input2 = args.path2
    if args.out is not None:
        if not os.path.exists(args.out):
            print("Output dir does not exist, try to create it")
            os.makedirs(args.out)
            print("Output dir created at {}".format(args.out))
    return input1, input2, args.out, args.log


def hash_calculate(imglist, save_path, log_trigger):
    """Calculate hash of all images in the input list

    Args:
        imglist (list): list of images
        save_path (str): path to save hash results (in hdf5 format)
        log_trigger (bool): whether to show detail log

    Return:
        hash_results (list): The hash results of all images
                             in the list in order
    """

    class myThread(threading.Thread):

        def __init__(self, threadID, chunk):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.chunk = chunk

        def run(self):
            if log_trigger:
                print("开启线程： " + self.name, flush=True)

            thread_t1 = time()
            for i, v in enumerate(self.chunk):
                index = v[0]
                hash = get_hash(v[1])
                hash_array = hash.hash.flatten()
                hash_results.append((index, hash_array))
                if log_trigger:
                    print(
                        "ThreadID {}, {}/{}, index={}, path={}, hash={}".
                        format(self.threadID, i, len(self.chunk), v[0], v[1],
                               hash),
                        flush=True)
            thread_t2 = time()
            if log_trigger:
                print(
                    "{} 计算完成， 用时 {:.4f} second".format(self.name,
                                                       thread_t2 - thread_t1),
                    flush=True)

    # region 单线程预处理部分
    # ===================== 单线程预处理部分 =========================
    # 设置线程数
    thread_num = multiprocessing.cpu_count()
    print("Number of images = {}".format(len(imglist)))

    imglist_tuple = list(zip(list(range(len(imglist))), imglist))

    filechunks = get_chunks(imglist_tuple, thread_num)
    thread_num = len(filechunks)
    hash_results = []
    # endregion

    # region 多线程计算部分
    # ===================== 多线程计算部分 =========================

    t1 = time()
    # 开启多线程
    # 线程锁
    # threadLock = threading.Lock()
    threads = []

    for i in range(thread_num):
        # 创建线程
        thread = myThread(i + 1, filechunks[i])
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for t in threads:
        t.join()

    t2 = time()
    print(
        "Calculation finish. Time consumption: {:.4f} second".format(t2 - t1),
        flush=True)
    print(
        "Average speed: {:.4f} img/s".format(len(imglist) / (t2 - t1 + 1e-5)),
        flush=True)
    # endregion

    # ===================== 后续处理部分 =========================
    # 按 index 排序
    hash_results.sort(key=lambda x: x[0])
    hash_results = [x[1] for x in hash_results]
    # 存储结果
    with h5py.File(save_path, "w") as f:
        f.create_dataset("data", data=hash_results)
    print("Save phash result (hdf5) to " + save_path, flush=True)
    print("=" * 60)

    return hash_results


def hash_compare(hash1, hash2, imglist1, imglist2, log_trigger):
    """With two imglists and hash result lists, compare the hash
    distances to find dul img pairs


    Args:
        hash1 (list): hash results of all images in imglist1
        hash2 (list): hash results of all images in imglist2
        imglist1: all the img paths in list1 or file1
        imglist2: all the img paths in list2 or file2
        save_path (str): path to save compare results (in json format)
        log_trigger (bool): whether to show detail log

    Return:
        result_dict (dict): Dedup result in dict form
    """
    # use phash to ddup
    print('Start to ddup')
    tensor1 = torch.Tensor(hash1).to('cuda:0')
    tensor2 = torch.Tensor(hash2).to('cuda:0')

    files1 = np.array(imglist1)
    files2 = np.array(imglist2)

    t1 = time()
    s = 0
    result_dict = {}
    for i in range(tensor1.size(0)):
        x = tensor1[i:i + 1, :]
        diff = (x - tensor2).abs().sum(dim=-1)
        score, index = torch.sort(diff)
        mask = score < 3
        score = score[mask].cpu().numpy()
        index = index[mask].cpu().numpy()
        names = files2[index]

        # dataset 自我去去重时，去掉同一图片与自己比较的结果
        mask = names != files1[i]
        score = score[mask]
        index = index[mask]
        names = names[mask]

        if len(index) > 0:
            s += 1
            result_dict[files1[i]] = list(names)
            if log_trigger:
                print('>>', files1[i])
                print('\n'.join(list(names)))
    t2 = time()

    print('Dedup done.')
    print("Dedup total time consumption: {:.4f} second".format(t2 - t1))
    print("Total dul image pairs: {}".format(s))
    print("Dedup speed: {:.4f} img/s".format(len(files1) / (t2 - t1 + 1e-5)))

    return result_dict


def main():
    input1, input2, save_dir, log_trigger = load_config(parse_args())

    hash1_save_path = osp.join(save_dir, "hash1.hdf5")
    hash2_save_path = osp.join(save_dir, "hash2.hdf5")
    ddup_json_save_path = osp.join(save_dir, "ddup_output.json")

    # calculate hash
    if input1 == input2:
        print("This is self compare")
        if type(input1) is list:
            imglist = input1
        else:
            imglist = open(input1).readlines()
            imglist = [x.strip("\n") for x in imglist]
        print("Start to calculate hash for input1", flush=True)
        hash1 = hash_calculate(imglist, hash1_save_path, log_trigger)
        ddup_result = hash_compare(hash1, hash1, imglist, imglist, log_trigger)
        """
        对于以下情况:
        1. 仅有 input1， 没有 input2
        2. input1 == input2
        认为属于【自我去重】
        此时将比对结果 dict 以【组】的形式重新整理，避免同一张图多次出现
        """
        result_dict_save = {}
        for k, v in ddup_result.items():
            group = v + [k]
            if len(result_dict_save.keys()) == 0:
                result_dict_save[group[0]] = group
            else:
                if set(group) not in [
                        set(x) for x in result_dict_save.values()
                ]:
                    result_dict_save[group[0]] = group
    else:
        if type(input1) is list:
            imglist1 = input1
        else:
            imglist1 = open(input1).readlines()
            imglist1 = [x.strip("\n") for x in imglist1]
        if type(input2) is list:
            imglist2 = input2
        else:
            imglist2 = open(input2).readlines()
            imglist2 = [x.strip("\n") for x in imglist2]

        print("Start to calculate hash for input1", flush=True)
        hash1 = hash_calculate(imglist1, hash1_save_path, log_trigger)
        print("Start to calculate hash for input2", flush=True)
        hash2 = hash_calculate(imglist2, hash2_save_path, log_trigger)
        result_dict_save = hash_compare(hash1, hash2, imglist1, imglist2,
                                        log_trigger)
    with open(ddup_json_save_path, "w") as jf:
        json.dump(
            result_dict_save,
            jf,
            ensure_ascii=False,
            indent=4,
            separators=(',', ':'))
    print('Result save at {}'.format(ddup_json_save_path))


if __name__ == '__main__':
    main()
