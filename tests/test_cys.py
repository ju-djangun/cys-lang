from anytree.search import findall

from cys import __version__
from cys.states import *


def test_version():
    assert __version__ == '0.0.1'

def test_find(line_tree: AbstractLineTreeManager):
    line_num = "_" + str(1)
    search_result = findall(
        line_tree.root_node,
        filter_ = lambda node: node.name.endswith(line_num) == True
        )
    for result in search_result:
        assert result
