# -*- coding: utf-8 -*-
"""区域框选器"""
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QRect, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPen, QFont


class RegionSelector(QWidget):
    """全屏半透明覆盖层，拖拽框选区域"""
    region_selected = pyqtSignal(dict)

    def __init__(self, monitors):
        super().__init__()
        self.monitors = monitors
        self.start_pos = None
        self.current_pos = None
        self._init_ui()

    def _init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setCursor(Qt.CrossCursor)
        self.showFullScreen()

    def paintEvent(self, event):
        painter = QPainter(self)
        # 半透明遮罩
        painter.fillRect(self.rect(), QColor(0, 0, 0, 128))

        if self.start_pos and self.current_pos:
            rect = QRect(self.start_pos, self.current_pos).normalized()
            # 框选区域高亮
            painter.fillRect(rect, QColor(74, 159, 216, 32))
            pen = QPen(QColor(74, 159, 216), 2, Qt.DashLine)
            painter.setPen(pen)
            painter.drawRect(rect)
            # 尺寸标签
            painter.setPen(QColor(255, 255, 255))
            painter.setFont(QFont("Arial", 12))
            size_text = f"{rect.width()} x {rect.height()}"
            painter.drawText(rect.center(), size_text)

        # 顶部提示
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Microsoft YaHei", 13))
        painter.drawText(self.rect(), Qt.AlignHCenter | Qt.AlignTop,
                        "\n\n拖拽鼠标框选区域    |    ESC 取消")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.pos()
            self.current_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.start_pos:
            self.current_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.start_pos:
            rect = QRect(self.start_pos, self.current_pos).normalized()
            if rect.width() > 10 and rect.height() > 10:
                region = {
                    "left": rect.x(),
                    "top": rect.y(),
                    "width": rect.width(),
                    "height": rect.height(),
                    "monitor_index": 0
                }
                self.region_selected.emit(region)
                self.close()
            else:
                # 框选太小，重置让用户重新框选
                self.start_pos = None
                self.current_pos = None
                self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
