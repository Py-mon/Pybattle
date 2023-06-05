import inspect
import typing
from inspect import isclass
from pathlib import Path
from types import UnionType
from typing import Any, Literal, Optional, Self, Type, get_args, get_origin

from diagrams import Cluster, Diagram, Edge
from diagrams import Node as NodeType
from diagrams.gcp.compute import GKE, ContainerOptimizedOS, Run
from diagrams.gcp.database import Spanner
from diagrams.gcp.devtools import GCR, Build
from diagrams.generic.blank import Blank

# https://diagrams.mingrammer.com/docs/nodes/onprem


def get_files(directory: Path) -> dict[Path, Path | dict[Path, Path | dict]]:
    """Get all the .py files and folders in a directory."""
    dct = {}
    for path in directory.glob("*"):
        if path.is_dir() and path.name != "__pycache__":
            dct[path] = get_files(path)
        elif path.suffix == ".py":
            dct[path] = path
    return dct


class Icon:
    Circle = ContainerOptimizedOS
    #Box = Resource
    Class = Build
    BaseClass = GCR
    Subclass = GKE
    Main = Run
    Blank = Blank
    Utils = Spanner


class Node:
    nodes: list[Self] = []

    def __init__(
        self,
        label: str = "",
        value: type = object,
        icon: Type[NodeType] = Icon.Class,
        cluster: Optional[Cluster] = None,
    ) -> None:
        self._label = label
        self.value = value
        self._constructor = icon
        self.cluster = cluster

        self._update()

        type(self).nodes.append(self)

    def _update(self):
        self._node = self.icon(self.label, nodeid=self.label)

    @property
    def icon(self):
        return self._constructor

    @icon.setter
    def icon(self, new: Type[NodeType]):
        self._constructor = new
        self._update()

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label: str):
        self._label = label
        self._update()

    @classmethod
    def get(cls, name: str):
        for node in cls.nodes:
            if node.label == name:
                return node

    def pair(self, node: Self, color="", label=""):
        self._node.connect(node._node, Edge(color=color, xlabel=label))

    def connect_arrow(self, node: Self, color="", label=""):
        self._node.connect(node._node, Edge(reverse=True, color=color, xlabel=label))


DIR = Path("C:/Users/jacob/Downloads/Programming/Python/Pybattle/Github/pybattle")


def create_clusters(directory: Path, files, cluster: Optional[Cluster] = None):
    """Create the nodes and clusters."""
    if directory == files:
        import_name = ".".join(directory.parts[8:])[:-3]
        exec(f"import {import_name}")
        module = eval(import_name)

        with Cluster(directory.stem):
            for item in module.__dict__.values():
                try:
                    if item.__module__ != import_name:  # Not Imported
                        continue
                except AttributeError:
                    pass

                if isclass(item):
                    Node(item.__name__, item, cluster=cluster)

    else:
        with Cluster(directory.stem) as cluster_:
            for directory_, files_ in files.items():
                create_clusters(directory_, files_, cluster_)


def is_injection(anno):
    if get_args(anno):
        anno = get_origin(anno)
    return anno not in list(__builtins__.__dict__.values()) + list(
        typing.__dict__.values()
    ) + [inspect.Parameter.empty]


def has_dependency_injection(cls) -> Literal[False] | Any:
    """Return a dependency injection if the class has one, otherwise False."""
    for param in inspect.signature(cls.__init__).parameters.values():
        if is_injection(param.annotation):
            if isinstance(param.annotation, UnionType):
                for type_ in param.annotation.__args__:
                    if is_injection(type_):
                        return type_
            else:
                if not isinstance(param.annotation, str):
                    return param.annotation
    return False


def connect_nodes():
    for node in Node.nodes:
        if node.value.__base__ != object:  # Subclass
            base = Node.get(node.value.__base__.__name__)
            if base is not None:
                node.icon = Icon.Subclass
                base.icon = Icon.BaseClass

                node.connect_arrow(base)

        dependency = has_dependency_injection(node.value)
        if dependency:
            dependency_ = Node.get(dependency.__name__)
            if dependency_ is not None:
                node.icon = Icon.Subclass
                dependency_.icon = Icon.BaseClass

                node.pair(dependency_)


with Diagram() as graph:
    for directory, files in get_files(DIR).items():
        create_clusters(directory, files, None)

    connect_nodes()
