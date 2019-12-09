"""
A class to implement a tree structure
"""
from collections import OrderedDict, UserDict


class Tree(UserDict):  # pylint: disable=too-many-ancestors
    """
    A class to implement a tree structure
    """

    def __init__(self, name: str, parent=None, sort: bool = True) -> None:
        UserDict.__init__(self)
        self.data = {}
        self.name = name
        self.parent = parent
        self.sort = sort

    def add_child(self, name: str) -> "Tree":
        """
        Add a child to the tree
        """
        self.data[name] = Tree(name=name, parent=self, sort=self.sort)
        if self.sort:
            self.data = OrderedDict(sorted(self.data.items(), key=lambda x: x[1].name))
        return self.data[name]

    def path(self) -> str:
        """
        Print the path from the root to the child
        """
        if self.parent:
            return self.parent.path() + "/" + self.name
        return "/" + self.name

    def to_print(self) -> None:
        """
        Print all of a tree
        """
        print(self.path())
        for child in self.data.values():
            child.to_print()

    def to_latex(self) -> None:
        """
        Print a tree in LaTeX format
        """
        print("child { node{" + self.name + "}")
        for child in self.data.values():
            child.to_latex()
        print("}")

    def to_dict_list(self) -> dict:
        """
        Print a tree in an alternating dict list format
        """
        outdict = {}
        outdict["name"] = self.name
        outdict["children"] = []
        for child in self.data.values():
            outdict["children"].append(child.to_dict_list())
        return outdict
