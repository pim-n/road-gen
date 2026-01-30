from typing import Tuple

import numpy as np
from matplotlib import pyplot as plt

from .base_road_generator import BaseRoadGenerator
from ..prefabs import prefabs
from ..integrator.integrator import integrate_road

class SegmentedRoadGenerator(BaseRoadGenerator):
    def __init__(
        self,
        length: int | float,
        ds: int | float,
        velocity: int | float,
        mu: float = 0.7,
        g: float = 9.81,
        seed: int | None = None
        ):
        """Initialize a SegmentedRoadGenerator with given or random seed.

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
            segments: list[str],
            alpha: float = 100
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Generate a curvature profile from a list of segments.

        Args:
            segments (list[str]): List of segments.
            alpha (float, optional): Dirichlet concentration parameter. A higher value leads to more uniform apportionment of the length amongst the segments, while a lower value allows more random apportionment. Defaults to 1.0.
        
        Raises:
            ValueError: "No valid radius for this turn segment" means a turn is too tight given its segment length and the velocity. To fix this, you can try to reduce the amount of segments or increase length. Increasing alpha (Dirichlet concentration parameter) can also help because this reduces the odds of very small lengths being assigned to turn segments. 
        
        Returns:
            Tuple[np.ndarray, np.ndarray]: x and y coordinates of the waypoints describing the random road.
        """
        if not all(segment in prefabs.PREFABS.keys() for segment in segments):
            raise ValueError(f"Invalid segment type provided. Available choices: {prefabs.SEGMENTS.keys()}")
        
        self.segments = segments
        self.alpha = alpha
        num_points = int(self.length / self.ds)

        # divide num_points into len(segments) randomly sized parts.
        parts = self._rng.dirichlet(np.full(len(segments), alpha), size=1)[0]
        parts = parts * num_points
        parts = np.round(parts).astype(int)

        # correct round off so the sum of parts is still total length L.
        if sum(parts) != num_points:
            parts[0] += num_points - sum(parts)


        curvature = np.zeros(num_points)
        current_index = 0

        for seg_name, seg_length in zip(segments, parts):
            seg_function = prefabs.PREFABS[seg_name]

            if seg_name == 'straight':
                curvature_s = seg_function(seg_length)
            else:
                R_min_angle = seg_length / (np.pi / 2)
                R_max_angle = seg_length / (np.pi / 6)

                # physics limit
                R_min = max(self.min_radius, R_min_angle)

                if R_min > R_max_angle:
                    raise ValueError("No valid radius for this turn segment")

                rand_radius = self._rng.uniform(R_min, R_max_angle)

                if seg_name.startswith("u_turn"):
                    curvature_s = seg_function(rand_radius)
                else:
                    curvature_s = seg_function(seg_length, rand_radius)

            curvature[current_index:(current_index + seg_length)] = curvature_s
            current_index += seg_length

            x, y = integrate_road(curvature)

        return x * self.ds, y * self.ds