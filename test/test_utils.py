import manos.utils as utils


def test_image_area_factors():
    assert utils.image_area_factors(8, 8, 25) == [(5, 5)]
    assert utils.image_area_factors(8, 8, 24) == [(3, 8), (4, 6)]


def test_smaller_sizes():
    pass
    # assert utils.smaller_sizes(2,3) == {(1, 2), (1, 3), (3, 1), (2, 1), (2, 2), (1, 1)}
    # assert utils.smaller_sizes(2,3) == utils.smaller_sizes(3,2)


def test_possible_positions_for_size():
    assert (
        utils.possible_positions_for_size(8, 8, 7, 8)
        == {(0, 8, 0, 7), (1, 8, 0, 8), (0, 7, 0, 8), (0, 8, 1, 8)}
    )
    # import numpy as np
    # test_array = np.ndarray(shape=(4,4), buffer=np.array(range(16)), dtype=int)
    nnn = utils.possible_positions_for_size(4, 4, 2, 3)
    assert len(nnn) == 12
