# -*- coding: utf-8 -*-
"""主配置窗口"""
import os
from datetime import datetime
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QSlider, QRadioButton, QFileDialog,
                              QLineEdit, QButtonGroup)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from meeting_screenshot.core.config import load_config, save_config
from meeting_screenshot.utils.screenshot import get_monitors
from meeting_screenshot.gui.region_selector import RegionSelector


class MainWindow(QWidget):
    """主配置窗口"""
    start_monitoring = pyqtSignal(dict)  # 发送配置参数

    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.monitors = get_monitors()
        self._init_ui()
        self._load_config_to_ui()

    def _init_ui(self):
        self.setWindowTitle("会议截图工具 v0.1")
        self.setFixedSize(420, 580)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(24, 24, 24, 24)

        # 标题
        title_layout = QHBoxLayout()
        title = QLabel("会议截图工具")
        title.setFont(QFont("Microsoft YaHei", 16, QFont.Bold))
        title_layout.addWidget(title)
        version_label = QLabel("v0.1")
        version_label.setStyleSheet("color: #4A9FD8; font-size: 11px; font-weight: 500; background: #E8F4FC; padding: 2px 8px; border-radius: 10px;")
        title_layout.addWidget(version_label)
        title_layout.addStretch()
        layout.addLayout(title_layout)

        # 保存位置
        layout.addWidget(QLabel("保存位置"))
        folder_layout = QHBoxLayout()
        self.folder_input = QLineEdit()
        self.folder_input.setPlaceholderText("选择保存文件夹")
        folder_layout.addWidget(self.folder_input)
        browse_btn = QPushButton("浏览")
        browse_btn.clicked.connect(self._browse_folder)
        folder_layout.addWidget(browse_btn)
        layout.addLayout(folder_layout)

        # 截图模式
        layout.addWidget(QLabel("截图模式"))
        self.mode_group = QButtonGroup()
        self.fullscreen_radio = QRadioButton("全屏截图（默认）")
        self.region_radio = QRadioButton("框选区域")
        self.mode_group.addButton(self.fullscreen_radio, 0)
        self.mode_group.addButton(self.region_radio, 1)
        layout.addWidget(self.fullscreen_radio)

        region_layout = QHBoxLayout()
        region_layout.addWidget(self.region_radio)
        self.reselect_btn = QPushButton("重新框选")
        self.reselect_btn.clicked.connect(self._select_region)
        region_layout.addWidget(self.reselect_btn)
        region_layout.addStretch()
        layout.addLayout(region_layout)

        # 变化阈值
        threshold_label = QLabel("变化阈值")
        layout.addWidget(threshold_label)
        threshold_layout = QHBoxLayout()
        self.threshold_slider = QSlider(Qt.Horizontal)
        self.threshold_slider.setMinimum(1)
        self.threshold_slider.setMaximum(20)
        self.threshold_slider.setValue(5)
        self.threshold_slider.valueChanged.connect(self._update_threshold_label)
        threshold_layout.addWidget(self.threshold_slider)
        self.threshold_value_label = QLabel("5%")
        threshold_layout.addWidget(self.threshold_value_label)
        layout.addLayout(threshold_layout)

        # 截图间隔
        interval_label = QLabel("截图间隔")
        layout.addWidget(interval_label)
        interval_layout = QHBoxLayout()
        self.interval_slider = QSlider(Qt.Horizontal)
        self.interval_slider.setMinimum(10)
        self.interval_slider.setMaximum(50)
        self.interval_slider.setValue(15)
        self.interval_slider.valueChanged.connect(self._update_interval_label)
        interval_layout.addWidget(self.interval_slider)
        self.interval_value_label = QLabel("1.5 秒")
        interval_layout.addWidget(self.interval_value_label)
        layout.addLayout(interval_layout)

        layout.addStretch()

        # 开始按钮
        self.start_btn = QPushButton("开始记录")
        self.start_btn.setFixedHeight(50)
        self.start_btn.clicked.connect(self._start_clicked)
        layout.addWidget(self.start_btn)

        hint = QLabel("启动后将自动缩小到系统托盘")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet("color: #888888; font-size: 12px;")
        layout.addWidget(hint)

        self.setLayout(layout)

    def _load_config_to_ui(self):
        """从配置加载到 UI"""
        if self.config.get("last_save_folder"):
            self.folder_input.setText(self.config["last_save_folder"])
        else:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            default_folder = os.path.join(desktop, f"会议截图_{datetime.now().strftime('%Y-%m-%d_%H-%M')}")
            self.folder_input.setText(default_folder)

        if self.config.get("screenshot_mode") == "region":
            self.region_radio.setChecked(True)
        else:
            self.fullscreen_radio.setChecked(True)

        self.threshold_slider.setValue(int(self.config.get("threshold", 5.0)))
        self.interval_slider.setValue(int(self.config.get("interval", 1.5) * 10))

    def _browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择保存文件夹")
        if folder:
            self.folder_input.setText(folder)

    def _select_region(self):
        selector = RegionSelector(self.monitors)
        selector.region_selected.connect(self._on_region_selected)
        selector.show()

    def _on_region_selected(self, region):
        self.config["region"] = region
        self.region_radio.setChecked(True)

    def _update_threshold_label(self, value):
        self.threshold_value_label.setText(f"{value}%")

    def _update_interval_label(self, value):
        self.interval_value_label.setText(f"{value / 10:.1f} 秒")

    def _start_clicked(self):
        save_folder = self.folder_input.text()
        if not save_folder:
            return

        config = {
            "save_folder": save_folder,
            "screenshot_mode": "region" if self.region_radio.isChecked() else "fullscreen",
            "region": self.config.get("region") if self.region_radio.isChecked() else None,
            "threshold": self.threshold_slider.value(),
            "interval": self.interval_slider.value() / 10.0
        }

        self.config["last_save_folder"] = save_folder
        self.config["screenshot_mode"] = config["screenshot_mode"]
        self.config["threshold"] = config["threshold"]
        self.config["interval"] = config["interval"]
        save_config(self.config)

        self.start_monitoring.emit(config)
        self.hide()
