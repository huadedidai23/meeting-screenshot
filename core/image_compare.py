# -*- coding: utf-8 -*-
"""图像对比模块"""
import numpy as np
from PIL import Image, ImageChops


def calculate_difference(img1, img2, pixel_threshold=30):
    """
    计算两张图片的差异百分比

    Args:
        img1: PIL Image 对象
        img2: PIL Image 对象
        pixel_threshold: 像素差异阈值，默认 30

    Returns:
        float: 差异百分比 (0-100)
    """
    # 转为灰度图并缩放到统一小尺寸加速对比
    gray1 = img1.convert('L').resize((320, 240))
    gray2 = img2.convert('L').resize((320, 240))

    # 计算像素差异
    diff = np.array(ImageChops.difference(gray1, gray2))

    # 统计差异超过阈值的像素数量
    changed_pixels = np.sum(diff > pixel_threshold)
    total_pixels = diff.size

    return (changed_pixels / total_pixels) * 100
