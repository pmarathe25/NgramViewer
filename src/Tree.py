from collections import defaultdict
from functools import reduce
import operator

class Tree(defaultdict):
    def __init__(self, value = None):
        super(Tree, self).__init__(Tree)
        self.value = value

    def get(self, indexList):
        return reduce(operator.getitem, indexList, self)

def main():
    root = Tree()
    root[1][2][3].value = 5
    print root[1][2][3].value
    root.get([1, 2, 3, 4]).value = "leaves"
    print root[1][2][3][4].value
    print root.get([1, 2, 3, 4]).value

if __name__ == '__main__':
    main()
