# -*- coding: utf-8 -*-

from motomagic.data_preparation import load_trip, get_blocks_indices

def test_split_in_blocks():
    folder = "data/new_logger"
    filename = "2016-12-06_16-30-59.zip"
    trip = load_trip(folder, filename)
    mini_trip = trip[:5000]
    block_indices = get_blocks_indices(mini_trip)
    assert block_indices == [(0, 1034), (1035, 2057), (2058, 3077), (3078, 4097)]
