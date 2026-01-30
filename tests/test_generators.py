import numpy as np

import pytest

from road_gen.generators.random_road_generator import RandomRoadGenerator
from road_gen.generators.segmented_road_generator import SegmentedRoadGenerator

@pytest.fixture
def base_params():
    length = 1_000
    ds = 10
    velocity = 10
    
    return length, ds, velocity

@pytest.fixture
def seg_params():
    segments = ["straight", "turn_left", "straight", "turn_right"]
    alpha = 100
    
    return segments, alpha


def test_random_road_generator(base_params):
    """Test whether fixing the seed for RandomRoadGenerator produces identical output."""
    generator_1 = RandomRoadGenerator(*base_params)
    x1, y1 = generator_1.generate()
    
    generator_2 = RandomRoadGenerator(seed = generator_1.seed, *base_params)
    x2, y2 = generator_2.generate()

    assert np.array_equal(x1, x2)
    assert np.array_equal(y1, y2)
    
def test_segmented_road_generator(base_params, seg_params):
    """Test whether fixing the seed for SegmentedRoadGenerator produces identical output."""
    generator_1 = SegmentedRoadGenerator(*base_params)
    x1, y1 = generator_1.generate(*seg_params)
    
    generator_2 = SegmentedRoadGenerator(seed = generator_1.seed, *base_params)
    x2, y2 = generator_2.generate(*seg_params)

    assert np.array_equal(x1, x2)
    assert np.array_equal(y1, y2)