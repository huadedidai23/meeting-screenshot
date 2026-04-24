# -*- coding: utf-8 -*-
"""会议截图工具 - 主程序入口"""
import sys
import os
from PyQt5.QtWidgets import QApplication

from meeting_screenshot.gui.main_window import MainWindow
from meeting_screenshot.gui.tray_icon import TrayIcon
from meeting_screenshot.core.screen_monitor import ScreenMonitor


class MeetingScreenshotApp:
    """主应用程序"""

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("会议截图工具")
        self.app.setQuitOnLastWindowClosed(False)

        self.main_window = MainWindow()
        self.tray_icon = None
        self.monitor = None
        self.current_config = None

        # 连接信号
        self.main_window.start_monitoring.connect(self._start_monitoring)

    def _start_monitoring(self, config):
        """开始监控"""
        self.current_config = config

        # 创建监控器
        self.monitor = ScreenMonitor(
            save_folder=config["save_folder"],
            region=config.get("region"),
            threshold=config["threshold"],
            interval=config["interval"],
            on_screenshot=self._on_screenshot
        )

        # 创建托盘图标
        if not self.tray_icon:
            self.tray_icon = TrayIcon(self.app)
            self.tray_icon.pause_clicked.connect(self._pause_monitoring)
            self.tray_icon.resume_clicked.connect(self._resume_monitoring)
            self.tray_icon.reconfig_clicked.connect(self._show_main_window)
            self.tray_icon.open_folder_clicked.connect(self._open_folder)
            self.tray_icon.exit_clicked.connect(self._exit_app)

        # 启动监控
        self.monitor.start()
        self.tray_icon.show_message("会议截图工具", "监控已启动")

    def _on_screenshot(self, count):
        """截图回调"""
        if self.tray_icon:
            self.tray_icon.update_count(count)

    def _pause_monitoring(self):
        """暂停监控"""
        if self.monitor:
            self.monitor.pause()

    def _resume_monitoring(self):
        """继续监控"""
        if self.monitor:
            self.monitor.resume()

    def _show_main_window(self):
        """显示主窗口"""
        self.main_window.show()
        self.main_window.activateWindow()

    def _open_folder(self):
        """打开截图文件夹"""
        if self.current_config:
            folder = self.current_config["save_folder"]
            if os.path.exists(folder):
                os.startfile(folder)

    def _exit_app(self):
        """退出程序"""
        if self.monitor:
            self.monitor.stop()
        self.app.quit()

    def run(self):
        """运行应用"""
        self.main_window.show()
        return self.app.exec_()


def main():
    app = MeetingScreenshotApp()
    sys.exit(app.run())


if __name__ == "__main__":
    main()
