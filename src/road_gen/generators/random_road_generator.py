from typing import Tuple
import numpy as np

from .base_road_generator import BaseRoadGenerator
from ..integrator.integrator import integrate_road

class RandomRoadGenerator(BaseRoadGenerator):
    def __init__(
            self,
            length: int | float,
            ds: int | float,
            velocity: int | float,
            mu: float = 0.7,
            g: float = 9.81,
            seed: int | None = None
            ):
        
        """Initialize a RandomRoadGenerator with a given or random seed.

        Args:
            length (int | float): The total length of the road in meters.
            ds (int | float): The step size in meters.
            velocity (int | float): Velocity in meters per second.
            mu (float): Coefficient of friction. Defaults to 0.7 (dry asphalt).
            g (float): Acceleration due to gravity (m/s^2). Defaults to 9.81.
            seed (int | None, optional): Set a seed for the generator. Default is a random seed.
        """

        super().__init__(length, ds, velocity, mu, g, seed)

    def generate(
            self,
            straight_section_prob: float = 0.05,
            straight_section_max_rel_size: float = 0.1
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Generate a random road according to specified parameters.

        Args:
            straight_section_prob (float, optional): Probability at every step i that a straight section will start. Defaults to 0.05.
            straight_section_max_rel_size (float, optional): The maximum size that straight section(s) can have relative to the total length of the path. Defaults to 0.1.

        Returns:
            Tuple[np.ndarray, np.ndarray]: x and y coordinates of the waypoints describing the random road.
        """
        
        self.straight_section_prob = straight_section_prob
        self.straight_section_max_rel_size = straight_section_max_rel_size
        
        num_points = int(self.length / (self.ds))
        max_curvature = 1 / self.min_radius
        
        white_noise = self._rng.standard_normal(num_points)
        curvature = np.clip(white_noise, -max_curvature, max_curvature)

        # Randomly add multiple straight sections
        i = 0
        while i < num_points:
            if np.random.rand() < straight_section_prob:
                # Random straight segment length
                max_len = int(num_points * straight_section_max_rel_size)
                seg_len = np.random.randint(1, max_len + 1)
                curvature[i:i+seg_len] = 0  # set curvature to zero for straight
                i += seg_len  # skip over straight segment
            else:
                i += 1

        x, y = integrate_road(curvature)

        return x * self.ds, y * self.ds
       