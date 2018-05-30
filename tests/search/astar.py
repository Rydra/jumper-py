from node import Node
from search.astar import search


def test_search_should_find_path_between_two_nodes(mocker):
    finder = mocker.MagicMock()
    start_node = Node(10, 10)
    end_node = Node(15, 15)

    clearance = 0

    final_node = search(finder, start_node, end_node, clearance, {})