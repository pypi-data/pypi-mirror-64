import os.path as osp

from imagehash import phash
from PIL import Image

# 用于替换损坏图像的纯黑图
black = phash(
    Image.open(osp.join(osp.split(osp.realpath(__file__))[0], "black.png")))
# black = phash(Image.open("black.png"))


def get_hash(path):
    """With an image path, calculate the specified hash of the image

    If the image provided is broken, a pure black image
    will be used as replacement, providing an image hash
    with all zeros.

    Args:
        path (str): path of the input image

    Return:
        hash (:obj:`ImageHash`)
    """
    try:
        img = Image.open(path)
        hash = phash(img)
    except Exception:
        hash = black
    return hash
