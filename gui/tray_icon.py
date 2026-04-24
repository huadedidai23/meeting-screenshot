# -*- coding: utf-8 -*-
"""系统托盘图标和菜单"""
import os
import sys
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject, pyqtSignal


class TrayIcon(QObject):
    """系统托盘图标"""
    pause_clicked = pyqtSignal()
    resume_clicked = pyqtSignal()
    reconfig_clicked = pyqtSignal()
    open_folder_clicked = pyqtSignal()
    exit_clicked = pyqtSignal()

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.screenshot_count = 0
        self.is_paused = False
        self._init_tray()

    def _init_tray(self):
        """初始化托盘图标和菜单"""
        self.tray = QSystemTrayIcon(self.app)

        # 使用系统图标（简化版，实际应该用自定义图标）
        icon = self.app.style().standardIcon(self.app.style().SP_ComputerIcon)
        self.tray.setIcon(icon)

        # 创建菜单
        menu = QMenu()

        # 标题
        title_action = QAction("会议截图工具 v0.1", menu)
        title_action.setEnabled(False)
        menu.addAction(title_action)

        menu.addSeparator()

        # 暂停/继续
        self.pause_action = QAction("暂停监控", menu)
        self.pause_action.triggered.connect(self._toggle_pause)
        menu.addAction(self.pause_action)

        # 截图计数
        self.count_action = QAction("已截图：0 张", menu)
        self.count_action.setEnabled(False)
        menu.addAction(self.count_action)

        menu.addSeparator()

        # 重新配置
        reconfig_action = QAction("重新配置", menu)
        reconfig_action.triggered.connect(self.reconfig_clicked.emit)
        menu.addAction(reconfig_action)

        # 打开文件夹
        open_folder_action = QAction("打开截图文件夹", menu)
        open_folder_action.triggered.connect(self.open_folder_clicked.emit)
        menu.addAction(open_folder_action)

        menu.addSeparator()

        # 退出
        exit_action = QAction("退出程序", menu)
        exit_action.triggered.connect(self.exit_clicked.emit)
        menu.addAction(exit_action)

        self.tray.setContextMenu(menu)
        self.tray.show()

    def _toggle_pause(self):
        """切换暂停/继续状态"""
        if self.is_paused:
            self.is_paused = False
            self.pause_action.setText("暂停监控")
            self.resume_clicked.emit()
        else:
            self.is_paused = True
            self.pause_action.setText("继续监控")
            self.pause_clicked.emit()

    def update_count(self, count):
        """更新截图计数"""
        self.screenshot_count = count
        self.count_action.setText(f"已截图：{count} 张")

    def show_message(self, title, message):
        """显示托盘通知"""
        self.tray.showMessage(title, message, QSystemTrayIcon.Information, 2000)
