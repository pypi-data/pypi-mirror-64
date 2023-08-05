import pytest
from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import QMainWindow

from nodedge.edge import Edge
from nodedge.editor_widget import EditorWidget
from nodedge.node import Node
from nodedge.scene import Scene


@pytest.fixture
def emptyScene(qtbot):
    window = QMainWindow()
    editor = EditorWidget(window)
    qtbot.addWidget(editor)

    return editor.scene


@pytest.fixture
def undefinedNode(emptyScene: Scene) -> Node:
    node = Node(emptyScene)  # noqa: F841

    return emptyScene.nodes[0]
