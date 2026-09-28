from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
from PyQt5.QtCore import Qt


class PriceGraph(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.prices = []
        self.setMinimumSize(300, 200)

    def update_prices(self, prices):
        self.prices = prices
        self.update()  # triggers repaint

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        padding = 40

        # background
        painter.fillRect(0, 0, w, h, QColor(245, 245, 245))

        # axes
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)
        painter.drawLine(padding, padding, padding, h - padding)       # y axis
        painter.drawLine(padding, h - padding, w - padding, h - padding)  # x axis

        # axis labels
        painter.setFont(QFont("Arial", 8))
        painter.drawText(5, padding, "Price")
        painter.drawText(w - padding, h - 10, "Round")

        if len(self.prices) < 2:
            painter.drawText(w // 2 - 50, h // 2, "No data yet")
            return

        max_p = max(self.prices) if max(self.prices) > 0 else 1
        min_p = min(self.prices)
        price_range = max_p - min_p if max_p != min_p else 1

        # plot price line
        pen = QPen(QColor(0, 120, 200), 2)
        painter.setPen(pen)

        def to_x(i):
            return padding + int((i / (len(self.prices) - 1)) * (w - 2 * padding))

        def to_y(p):
            return (h - padding) - int(((p - min_p) / price_range) * (h - 2 * padding))

        for i in range(1, len(self.prices)):
            x1 = to_x(i - 1)
            y1 = to_y(self.prices[i - 1])
            x2 = to_x(i)
            y2 = to_y(self.prices[i])
            painter.drawLine(x1, y1, x2, y2)

        # draw dots at each data point
        pen = QPen(QColor(200, 50, 50), 4)
        painter.setPen(pen)
        for i, p in enumerate(self.prices):
            painter.drawPoint(to_x(i), to_y(p))