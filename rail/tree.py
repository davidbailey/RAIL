from collections import OrderedDict, UserDict

class Tree(UserDict):
    def __init__(self, name: str, parent=None, sort: bool=True) -> None:
        self.data = {}
        self.name = name
        self.parent = parent
        self.sort = sort

    def addChild(self, name: str) -> 'Tree':
        self.data[name] = Tree(name=name, parent=self, sort=self.sort)
        if self.sort:
            self.data = OrderedDict(sorted(self.data.items(), key=lambda x: x[1].name))
        return self.data[name]

    def path(self) -> str:
        if self.parent:
            return self.parent.path() + '/' + self.name
        else:
            return '/' + self.name

    def to_print(self) -> None:
        print(self.path())
        for child in self.data.values():
            child.to_print()

    def to_latex(self) -> None:
        print('child { node{' + self.name + '}')
        for child in self.data.values():
            child.to_latex()
        print('}')

    def to_dict_list(self) -> dict:
        outdict = {}
        outdict['name'] = self.name
        outdict['children'] = []
        for child in self.data.values():
            outdict['children'].append(child.to_dict_list())
        return outdict
