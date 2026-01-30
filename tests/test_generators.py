import numpy as np

import pytest

from road_gen.generators.random_road_generator import RandomRoadGenerator

@pytest.fixture
def test_params():
    length = 1_000
    ds = 10
    velocity = 10
    
    return length, ds, velocity


def test_random_road_generator(test_params):
    """Test whether fixing the seed for RandomRoadGenerator produces identical output."""
    generator_1 = RandomRoadGenerator(*test_params)
    x1, y1 = generator_1.generate()
    
    generator_2 = RandomRoadGenerator(seed = generator_1.seed, *test_params)
    x2, y2 = generator_2.generate()

    assert np.array_equal(x1, x2)
    assert np.array_equal(y1, y2)
    