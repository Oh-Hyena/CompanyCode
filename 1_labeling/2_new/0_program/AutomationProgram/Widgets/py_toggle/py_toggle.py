# Import QT CORE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from qt_core import *

class PyToggle(QCheckBox):
    def __init__(
        self,
        width = 60,
        bg_color = "#777",
        circle_color = "#DDD",
        active_color = "#a7a7f7"
    ):
        QCheckBox.__init__(self)

        self.name = ""

        # Set Default Parameters
        self.setFixedSize(width, 20)

        # Colors
        self._bg_color = bg_color
        self._circle_color = circle_color
        self._active_color = active_color

        # Create Animation
        self._circle_position = 3
        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.setDuration(300) # Time in milisec

        # Connect State Changed
        self.stateChanged.connect(self.start_transition)

    # Create New Set and Get Property
    @pyqtProperty(float) # Get
    def circle_position(self):
        return self._circle_position

    @circle_position.setter # Set
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()

    def start_transition(self, value):
        self.animation.stop() # Stop animation if running
        if value:
            self.animation.setEndValue(self.width() - (20 - 2))
        else:
            self.animation.setEndValue(3)

        # Start Animation
        self.animation.start()

    # Set New Hit Area
    def hitButton(self, pos:QPoint):
        return self.contentsRect().contains(pos)

    # Draw New Items
    def paintEvent(self, e):
        # Set Painter
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Set As No Pen
        p.setPen(Qt.PenStyle.NoPen)

        # Draw Rectangle
        rect = QRect(0, 0, self.width(), self.height())

        # Check If is Checked
        if not self.isChecked():
            # Draw BG
            p.setBrush(QColor(self._bg_color))
            p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2)

            # Draw Circle
            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(self._circle_position, 3, (20 - (2 * 3)), (20 - (2 * 3)))
        else:
            # Draw BG
            p.setBrush(QColor(self._active_color))
            p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2)

            # Draw Circle
            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(self._circle_position, 3, (20 - (2 * 3)), (20 - (2 * 3)))

        # End Draw
        p.end()

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name