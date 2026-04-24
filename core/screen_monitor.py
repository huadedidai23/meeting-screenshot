# -*- coding: utf-8 -*-
"""屏幕监控引擎"""
import os
import time
import threading
from PIL import Image

from meeting_screenshot.core.image_compare import calculate_difference
from meeting_screenshot.utils.screenshot import capture_region


class ScreenMonitor:
    """屏幕监控器，检测画面变化并保存截图"""

    def __init__(self, save_folder, region=None, threshold=5.0,
                 interval=1.5, on_screenshot=None):
        self.save_folder = save_folder
        self.region = region
        self.threshold = threshold
        self.interval = interval
        self.on_screenshot = on_screenshot  # 回调函数(count)

        self._running = False
        self._paused = False
        self._thread = None
        self._lock = threading.Lock()
        self._counter = 0
        self._previous_frame = None

    @property
    def counter(self):
        return self._counter

    @property
    def is_running(self):
        return self._running

    @property
    def is_paused(self):
        return self._paused

    def start(self):
        """启动监控"""
        if self._running:
            return
        os.makedirs(self.save_folder, exist_ok=True)
        self._running = True
        self._paused = False
        self._previous_frame = None
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()

    def stop(self):
        """停止监控"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=3)
            self._thread = None

    def pause(self):
        """暂停监控"""
        self._paused = True

    def resume(self):
        """继续监控"""
        self._paused = False

    def _monitor_loop(self):
        """监控主循环"""
        while self._running:
            if self._paused:
                time.sleep(0.3)
                continue

            try:
                current_frame = capture_region(self.region)

                if self._previous_frame is not None:
                    diff = calculate_difference(self._previous_frame, current_frame)
                    if diff >= self.threshold:
                        self._save_screenshot(current_frame)
                        self._previous_frame = current_frame
                else:
                    # 第一帧直接保存
                    self._save_screenshot(current_frame)
                    self._previous_frame = current_frame

            except Exception:
                pass

            time.sleep(self.interval)

    def _save_screenshot(self, img):
        """保存截图"""
        with self._lock:
            self._counter += 1
            filename = f"{self._counter:03d}.png"
            filepath = os.path.join(self.save_folder, filename)
            img.save(filepath, "PNG")
            if self.on_screenshot:
                self.on_screenshot(self._counter)
