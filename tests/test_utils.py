from utils import string_map_to_array, array_to_nodes


def test_convert_a_string_map_into_a_map_array():
    map = """
            01010
            01010
            01110
            00000
            """
    array_map = string_map_to_array(map)

    assert len(array_map) == 4
    assert array_map[0] == ["0", "1", "0", "1", "0"]
    assert array_map[1] == ["0", "1", "0", "1", "0"]
    assert array_map[2] == ["0", "1", "1", "1", "0"]
    assert array_map[3] == ["0", "0", "0", "0", "0"]


def test_convert_an_array_list_into_array_of_nodes():
    map = [
        ["0", "1", "0", "1", "0"],
        ["0", "1", "0", "1", "0"],
        ["0", "1", "1", "1", "0"],
        ["0", "0", "0", "0", "0"],
    ]

    nodes, min_x, max_x, min_y, max_y = array_to_nodes(map)
    assert len(nodes) == 4
    assert min_x == 0
    assert max_x == 5
    assert min_y == 0
    assert max_y == 4
