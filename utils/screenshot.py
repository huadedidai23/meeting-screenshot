# -*- coding: utf-8 -*-
"""截图工具模块"""
import mss
from PIL import Image


def get_monitors():
    """获取所有显示器信息，返回 mss monitors 列表"""
    with mss.mss() as sct:
        return list(sct.monitors)


def capture_region(region=None):
    """
    截取指定区域

    Args:
        region: dict {left, top, width, height}，None 则截取所有显示器的虚拟桌面

    Returns:
        PIL Image 对象
    """
    with mss.mss() as sct:
        if region is None:
            monitor = sct.monitors[0]
            region = {
                "left": monitor["left"],
                "top": monitor["top"],
                "width": monitor["width"],
                "height": monitor["height"]
            }
        screenshot = sct.grab(region)
        return Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
