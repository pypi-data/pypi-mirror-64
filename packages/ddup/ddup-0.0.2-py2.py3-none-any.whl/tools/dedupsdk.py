import json
import os
import sys
import threading
import numpy as np
from time import time
import torch
import argparse
import multiprocessing
import h5py
import os.path as osp
from dedup.utils.chunks import get_chunks
from dedup.utils.hash import get_hash


def parse_args():
    parser = argparse.ArgumentParser(
        description="""
        Given two image lists, compare the phash of the images in the first list to those in the second to find dulplicate pairs.\n
        Result will be saved in the given dir.
        """,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "path1",
        help="path of the first image list",
        default=None,
        type=str,
    )
    parser.add_argument(
        "path2",
        help="path of the second image list",
        default=None,
        type=str
    )
    parser.add_argument(
        "save_dir",
        help="Folder path to save the results",
        default=None,
        type=str
    )
    parser.add_argument(
        "--log",
        help="Add this to show detail log",
        default=False,
        action="store_true"
    )
    if len(sys.argv) == 1:
        parser.print_help()
    return parser.parse_args()


def load_config(args):
    """
    Given the arguemnts, load, check and initialize the configs.
    Args:
        args (argument): arguments includes `path1`, `path2`, `save_dir`
    """
    # 判断 p 是否为合法路径
    if args.path1 is not None:
        if os.path.isdir(args.path1):
            print("path1 should be a file.")
            sys.exit(0)
        if not os.path.exists(args.path1):
            print("path1 does not exist")
            sys.exit(0)
    # 判断 d 是否为合法路径
    if args.path2 is not None:
        if os.path.isdir(args.path2):
            print("path2 should be a file.")
            sys.exit(0)
        if not os.path.exists(args.path2):
            print("path2 does not exist")
            sys.exit(0)
    if args.save_dir is not None:
        if not os.path.isdir(args.save_dir):
            print("save_dir should be a folder.")
            sys.exit(0)
        if not os.path.exists(args.save_dir):
            print("save_dir does not exist, try to create it")
            os.makedirs(args.save_dir)
            print("save_dir created at {}".format(args.save_dir))
            sys.exit(0)
    return args.path1, args.path2, args.save_dir, args.log


def main():
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
                phash_all.append((index, hash_array))
                if log_trigger:
                    print(
                        "ThreadID {}, {}/{}, index={}, path={}, hash={}".format(self.threadID, i, len(self.chunk), v[0],
                                                                                v[1],
                                                                                hash), flush=True)
            thread_t2 = time()
            if log_trigger:
                print("{} 计算完成， 用时 {:.4f} second".format(
                    self.name, thread_t2 - thread_t1), flush=True)

    list_path1, list_path2, save_dir, log_trigger = load_config(parse_args())

    imglist_read = []
    phash_results = []

    # calculate ad save phash
    for list_path in [list_path1, list_path2]:
        print("Start to calculate phash for {}".format(list_path), flush=True)
        filename = osp.splitext(list_path.split("/")[-1])[0]
        phash_save_path = save_dir

        # 设置线程数
        thread_num = multiprocessing.cpu_count()

        # region 单线程预处理部分
        # ===================== 单线程预处理部分 =========================

        imglist = open(list_path).readlines()
        imglist = [x.strip("\n") for x in imglist]
        imglist_read.append(imglist)
        print("Number of images = {}".format(len(imglist)))

        imglist_tuple = list(zip(list(range(len(imglist))), imglist))

        filechunks = get_chunks(imglist_tuple, thread_num)
        thread_num = len(filechunks)
        phash_all = []
        # endregion

        # region 多线程计算部分
        # ===================== 多线程计算部分 =========================

        t1 = time()
        # 开启多线程
        threadLock = threading.Lock()
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
        print("Calculation finish. Time consumption: {:.4f} second".format(
            t2 - t1), flush=True)
        print(
            "Average speed: {:.4f} img/s".format(len(imglist) / (t2 - t1)), flush=True)
        # endregion

        # ===================== 后续处理部分 =========================
        # 按 index 排序
        phash_all.sort(key=lambda x: x[0])
        phash_all = [x[1] for x in phash_all]
        phash_results.append(phash_all)
        # 存储结果
        with h5py.File(osp.join(phash_save_path, filename + "_phash.hdf5"), "w") as f:
            f.create_dataset("data", data=phash_all)
        print("Save phash result (hdf5) to " +
              osp.join(phash_save_path, filename + "_phash.hdf5"), flush=True)
        print("=" * 60)

    # use phash to dedup
    print('Start to dedup')
    tensor1 = torch.Tensor(phash_results[0]).to('cuda:0')
    tensor2 = torch.Tensor(phash_results[1]).to('cuda:0')

    files1 = np.array(imglist_read[0])
    files2 = np.array(imglist_read[1])

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
    with open(osp.join(save_dir, "dedup.json"), "w") as jf:
        json.dump(result_dict, jf, ensure_ascii=False,
                  indent=4, separators=(',', ':'))
    print('Dedup done. Result save at {}'.format(
        osp.join(save_dir, "dedup.json")))
    print("Dedup total time consumption: {:.4f} second".format(t2 - t1))
    print("Total dul image pairs: {}".format(s))
    print("Dedup speed: {:.4f} img/s".format(len(files1) / (t2 - t1)))


if __name__ == '__main__':
    main()
