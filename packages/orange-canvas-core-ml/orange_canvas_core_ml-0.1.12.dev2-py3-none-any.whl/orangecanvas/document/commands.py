"""
Undo/Redo Commands

"""
import typing
from typing import Callable, Optional, Tuple, Any

from AnyQt.QtWidgets import QUndoCommand

if typing.TYPE_CHECKING:
    from ..scheme import (
        Scheme, SchemeNode, SchemeLink, BaseSchemeAnnotation,
        SchemeTextAnnotation, SchemeArrowAnnotation
    )
    Pos = Tuple[float, float]
    Rect = Tuple[float, float, float, float]
    Line = Tuple[Pos, Pos]


class AddNodeCommand(QUndoCommand):
    def __init__(self, scheme, node, parent=None):
        # type: (Scheme, SchemeNode, Optional[QUndoCommand]) -> None
        super().__init__("Add %s" % node.title, parent)
        self.scheme = scheme
        self.node = node

    def redo(self):
        self.scheme.add_node(self.node)

    def undo(self):
        self.scheme.remove_node(self.node)


class RemoveNodeCommand(QUndoCommand):
    def __init__(self, scheme, node, parent=None):
        # type: (Scheme, SchemeNode, Optional[QUndoCommand]) -> None
        super().__init__("Remove %s" % node.title, parent)
        self.scheme = scheme
        self.node = node

        links = scheme.input_links(node) + \
                scheme.output_links(node)

        for link in links:
            RemoveLinkCommand(scheme, link, parent=self)

    def redo(self):
        # redo child commands
        super().redo()
        self.scheme.remove_node(self.node)

    def undo(self):
        self.scheme.add_node(self.node)
        # Undo child commands
        super().undo()


class AddLinkCommand(QUndoCommand):
    def __init__(self, scheme, link, parent=None):
        # type: (Scheme, SchemeLink, Optional[QUndoCommand]) -> None
        super().__init__("Add link", parent)
        self.scheme = scheme
        self.link = link

    def redo(self):
        self.scheme.add_link(self.link)

    def undo(self):
        self.scheme.remove_link(self.link)


class RemoveLinkCommand(QUndoCommand):
    def __init__(self, scheme, link, parent=None):
        # type: (Scheme, SchemeLink, Optional[QUndoCommand]) -> None
        super().__init__("Remove link", parent)
        self.scheme = scheme
        self.link = link

    def redo(self):
        self.scheme.remove_link(self.link)

    def undo(self):
        self.scheme.add_link(self.link)


class InsertNodeCommand(QUndoCommand):
    def __init__(
            self,
            scheme,     # type: Scheme
            new_node,   # type: SchemeNode
            old_link,   # type: SchemeLink
            new_links,  # type: Tuple[SchemeLink, SchemeLink]
            parent=None # type: Optional[QUndoCommand]
    ):  # type: (...) -> None
        super().__init__("Insert widget into link", parent)
        self.scheme = scheme
        self.inserted_widget = new_node
        self.original_link = old_link
        self.new_links = new_links

    def redo(self):
        self.scheme.add_node(self.inserted_widget)
        self.scheme.remove_link(self.original_link)
        self.scheme.add_link(self.new_links[0])
        self.scheme.add_link(self.new_links[1])

    def undo(self):
        self.scheme.remove_link(self.new_links[0])
        self.scheme.remove_link(self.new_links[1])
        self.scheme.add_link(self.original_link)
        self.scheme.remove_node(self.inserted_widget)


class AddAnnotationCommand(QUndoCommand):
    def __init__(self, scheme, annotation, parent=None):
        # type: (Scheme, BaseSchemeAnnotation, Optional[QUndoCommand]) -> None
        super().__init__("Add annotation", parent)
        self.scheme = scheme
        self.annotation = annotation

    def redo(self):
        self.scheme.add_annotation(self.annotation)

    def undo(self):
        self.scheme.remove_annotation(self.annotation)


class RemoveAnnotationCommand(QUndoCommand):
    def __init__(self, scheme, annotation, parent=None):
        # type: (Scheme, BaseSchemeAnnotation, Optional[QUndoCommand]) -> None
        super().__init__("Remove annotation", parent)
        self.scheme = scheme
        self.annotation = annotation

    def redo(self):
        self.scheme.remove_annotation(self.annotation)

    def undo(self):
        self.scheme.add_annotation(self.annotation)


class MoveNodeCommand(QUndoCommand):
    def __init__(self, scheme, node, old, new, parent=None):
        # type: (Scheme, SchemeNode, Pos, Pos, Optional[QUndoCommand]) -> None
        super().__init__("Move", parent)
        self.scheme = scheme
        self.node = node
        self.old = old
        self.new = new

    def redo(self):
        self.node.position = self.new

    def undo(self):
        self.node.position = self.old


class ResizeCommand(QUndoCommand):
    def __init__(self, scheme, item, new_geom, parent=None):
        # type: (Scheme, SchemeTextAnnotation, Rect, Optional[QUndoCommand]) -> None
        super().__init__("Resize", parent)
        self.scheme = scheme
        self.item = item
        self.new_geom = new_geom
        self.old_geom = item.rect

    def redo(self):
        self.item.rect = self.new_geom

    def undo(self):
        self.item.rect = self.old_geom


class ArrowChangeCommand(QUndoCommand):
    def __init__(self, scheme, item, new_line, parent=None):
        # type: (Scheme, SchemeArrowAnnotation, Line, Optional[QUndoCommand]) -> None
        super().__init__("Move arrow", parent)
        self.scheme = scheme
        self.item = item
        self.new_line = new_line
        self.old_line = (item.start_pos, item.end_pos)

    def redo(self):
        self.item.set_line(*self.new_line)

    def undo(self):
        self.item.set_line(*self.old_line)


class AnnotationGeometryChange(QUndoCommand):
    def __init__(
            self,
            scheme,  # type: Scheme
            annotation,  # type: BaseSchemeAnnotation
            old,  # type: Any
            new,  # type: Any
            parent=None  # type: Optional[QUndoCommand]
    ):  # type: (...) -> None
        super().__init__("Change Annotation Geometry", parent)
        self.scheme = scheme
        self.annotation = annotation
        self.old = old
        self.new = new

    def redo(self):
        self.annotation.geometry = self.new  # type: ignore

    def undo(self):
        self.annotation.geometry = self.old  # type: ignore


class RenameNodeCommand(QUndoCommand):
    def __init__(self, scheme, node, old_name, new_name, parent=None):
        # type: (Scheme, SchemeNode, str, str, Optional[QUndoCommand]) -> None
        super().__init__("Rename", parent)
        self.scheme = scheme
        self.node = node
        self.old_name = old_name
        self.new_name = new_name

    def redo(self):
        self.node.set_title(self.new_name)

    def undo(self):
        self.node.set_title(self.old_name)


class TextChangeCommand(QUndoCommand):
    def __init__(
            self,
            scheme,       # type: Scheme
            annotation,   # type: SchemeTextAnnotation
            old_content,  # type: str
            old_content_type,  # type: str
            new_content,  # type: str
            new_content_type,  # type: str
            parent=None   # type: Optional[QUndoCommand]
    ):  # type: (...) -> None
        super().__init__("Change text", parent)
        self.scheme = scheme
        self.annotation = annotation
        self.old_content = old_content
        self.old_content_type = old_content_type
        self.new_content = new_content
        self.new_content_type = new_content_type

    def redo(self):
        self.annotation.set_content(self.new_content, self.new_content_type)

    def undo(self):
        self.annotation.set_content(self.old_content, self.old_content_type)


class SetAttrCommand(QUndoCommand):
    def __init__(
            self,
            obj,         # type: Any
            attrname,    # type: str
            newvalue,    # type: Any
            name=None,   # type: Optional[str]
            parent=None  # type: Optional[QUndoCommand]
    ):  # type: (...) -> None
        if name is None:
            name = "Set %r" % attrname
        super().__init__(name, parent)
        self.obj = obj
        self.attrname = attrname
        self.newvalue = newvalue
        self.oldvalue = getattr(obj, attrname)

    def redo(self):
        setattr(self.obj, self.attrname, self.newvalue)

    def undo(self):
        setattr(self.obj, self.attrname, self.oldvalue)


class SimpleUndoCommand(QUndoCommand):
    """
    Simple undo/redo command specified by callable function pair.
    Parameters
    ----------
    redo: Callable[[], None]
        A function expressing a redo action.
    undo : Callable[[], None]
        A function expressing a undo action.
    text : str
        The command's text (see `QUndoCommand.setText`)
    parent : Optional[QUndoCommand]
    """

    def __init__(
            self,
            redo,  # type: Callable[[], None]
            undo,  # type: Callable[[], None]
            text,  # type: str
            parent=None  # type: Optional[QUndoCommand]
    ):  # type: (...) -> None
        super().__init__(text, parent)
        self._redo = redo
        self._undo = undo

    def undo(self):
        # type: () -> None
        """Reimplemented."""
        self._undo()

    def redo(self):
        # type: () -> None
        """Reimplemented."""
        self._redo()
