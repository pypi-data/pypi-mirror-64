# -*- coding: utf-8 -*-
"""
Graphics scene module containing :class:`~nodedge.graphics_scene.GraphicsScene` class.
"""

import logging
import math
from typing import Optional

from PyQt5.QtCore import QLine, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPen, QTransform
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsScene,
    QGraphicsSceneDragDropEvent,
    QGraphicsSceneMouseEvent,
    QWidget,
)


class GraphicsScene(QGraphicsScene):
    """:class:`~nodedge.scene.Scene` class

    The graphics scene contains the background grid."""

    #: pyqtSignal emitted when some item is selected in the `Scene`
    itemSelected = pyqtSignal()
    #: pyqtSignal emitted when items are deselected in the `Scene`
    itemsDeselected = pyqtSignal()

    def __init__(self, scene: "Scene", parent: Optional[QWidget] = None) -> None:  # type: ignore
        """
        :param scene: reference to the :class:`~nodedge.scene.Scene`
        :type scene: :class:`~nodedge.scene.Scene`
        :param parent: parent widget
        :type parent: QWidget
        """

        super().__init__(parent)

        self.__logger = logging.getLogger(__file__)
        self.__logger.setLevel(logging.INFO)

        self.scene = scene
        self.initUI()

    def initUI(self):
        """Set up this ``QGraphicsScene``"""
        self.initSizes()
        self.initStyle()
        self.setBackgroundBrush(self._color_background)

    # noinspection PyAttributeOutsideInit
    def initStyle(self):
        """Initialize ``QObjects`` like ``QColor``, ``QPen`` and ``QBrush``"""
        self._color_background = QColor("#ffffff")
        self._color_light = QColor("#ffffff")
        self._color_dark = QColor("#ffffff")

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)

        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)

    # noinspection PyAttributeOutsideInit
    def initSizes(self):
        """Set up internal attributes like `grid_size`, `scene_width` and `scene_height`."""
        self.grid_size = 20
        self.grid_squares = 5
        self.scene_width = 64000
        self.scene_height = 64000

    def setScene(self, width, height):
        """
        Set `width` and `height` of the graphics scene.
        """
        self.setSceneRect(-width // 2, -height // 2, width, height)

    def drawBackground(self, painter, rectangle):
        """
        Draw background scene grid.
        """
        super().drawBackground(painter, rectangle)

        # Create the background grid
        left = int(math.floor(rectangle.left()))
        right = int(math.ceil(rectangle.right()))
        top = int(math.floor(rectangle.top()))
        bottom = int(math.ceil(rectangle.bottom()))

        first_left = left - (left % self.grid_size)
        first_top = top - (top % self.grid_size)

        # Compute all lines to be drawn
        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.grid_size):
            line = QLine(x, top, x, bottom)
            if (x // self.grid_size) % self.grid_squares == 0:
                lines_dark.append(line)
            else:
                lines_light.append(line)

        for y in range(first_top, bottom, self.grid_size):
            line = QLine(left, y, right, y)
            if (y // self.grid_size) % self.grid_squares == 0:
                lines_dark.append(line)
            else:
                lines_light.append(line)

        # Draw the lines
        painter.setPen(self._pen_light)
        painter.drawLines(*lines_light)

        painter.setPen(self._pen_dark)
        painter.drawLines(*lines_dark)

    def dragMoveEvent(self, event: QGraphicsSceneDragDropEvent) -> None:
        """
        Handle Qt's mouse's drag move event.

        :param event: Mouse release event
        :type event: ``QGraphicsSceneDragDropEvent``
        """
        pass

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        Handle Qt's mouse's button press event.

        :param event: Mouse release event
        :type event: ``QGraphicsSceneMouseEvent``
        """
        item: Optional[QGraphicsItem] = self.itemAt(event.scenePos(), QTransform())

        if (
            item is not None
            and item not in self.selectedItems()
            and item.parentItem() not in self.selectedItems()
            and not event.modifiers() & Qt.ShiftModifier  # type: ignore
        ):
            self.__logger.debug(f"Pressed item: {item}")
            self.__logger.debug(f"Pressed parent item: {item.parentItem()}")
            self.__logger.debug(
                f"Selected items in graphics scene: {self.selectedItems()}"
            )
            for item in self.selectedItems():
                item.setSelected(False)

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        """
        Handle Qt's mouse's button release event.

        :param event: Mouse release event
        :type event: ``QGraphicsSceneMouseEvent``
        """
        item = self.itemAt(event.scenePos(), QTransform())

        if item is not None:
            item.setSelected(True)

        super().mouseReleaseEvent(event)
