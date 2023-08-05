import math
from abc import ABC
from typing import Tuple

import gym
import matplotlib.pyplot as plt
import numpy as np
import math

from shapely.geometry import Polygon, Point

import gym_grasshoppers.util.utils as utils
from gym_grasshoppers.exception.invalid_geojson_exception import InvalidGeojsonException
from gym_grasshoppers.garden.garden import Garden
from gym_grasshoppers.lawn_mower.action.move import Move
from gym_grasshoppers.lawn_mower.action.turn import Turn
from gym_grasshoppers.lawn_mower.lawn_mower import LawnMower


class GrassHoppers(gym.Env, ABC):
    """This is the grasshoppers environment for the OpenAI gym."""
    metadata = {'render.modes': ['human']}
    _MINIMUM_ANGLE = -180
    _MAXIMUM_ANGLE = 180
    _MINIMUM_DISTANCE = 0.1
    _MINIMUM_SPEED = 0
    _MAXIMUM_SPEED = 1

    def __init__(self, garden_grass_height, garden_geojson: str, mower_angle: int, mower_height: float,
                 mower_radius: float, mower_volume: float, mower_mulching: bool, max_steps: int) -> None:
        super().__init__()

        self._garden = Garden(garden_grass_height, garden_geojson)
        self._lawn_mower = LawnMower(self._garden.starting_point.x, self._garden.starting_point.y,
                                     mower_angle, mower_height, mower_radius, mower_volume, mower_mulching)
        self._garden_diagonal = utils.calculate_distance((self._garden.minimum_y, self._garden.minimum_x),
                                                         (self._garden.maximum_y, self._garden.maximum_x))

        if self._lawn_mower.mulching is False and self._garden.compost_heap is None:
            raise InvalidGeojsonException('A compost heap is necessary when the lawn mower can not mulch!')

        if self._garden.grass.exterior.intersects(self._garden.starting_point.buffer(
                utils.calculate_scaled_radius(self._lawn_mower.position.x, self._lawn_mower.radius))):
            raise InvalidGeojsonException('The starting point is too close to the boundary of the garden in the '
                                          'provided GeoJSON!')

        self._observation_space = gym.spaces.Box(low=np.zeros(160000, dtype=int),
                                                 high=np.full(160000, 255, dtype=int),
                                                 dtype=np.int)
        self._action_space = gym.spaces.Box(low=np.array([self._MINIMUM_ANGLE, self._MINIMUM_DISTANCE]),

                                            high=np.array([self._MAXIMUM_ANGLE, self._garden_diagonal]),
                                            dtype=np.float16)

        self._previous_mowed_area = 0
        self._episode_count = 0
        self._state = self.reset()
        self.viewer = None
        self.step_count = 0
        self._max_steps = max_steps

    @property
    def state(self):
        return self._state

    @property
    def observation_space(self):
        return self._observation_space

    @property
    def action_space(self):
        return self._action_space

    @property
    def max_steps(self):
        return self._max_steps

    def step(self, action: Tuple[int, float]) -> Tuple[np.array, float, bool, dict]:
        """This method is used to execute one step in the environment."""
        angle = action[0]
        distance = action[1]

        Turn(self._lawn_mower, angle).execute()
        Move(self._lawn_mower, distance, self._garden).execute()

        reward = self.__calculate_reward()

        self._lawn_mower.current_volume = \
            utils.calculate_polygon_area(self._garden.mowed_path) * self._garden.grass_height

        garden_array = utils.garden_to_array(self._garden, self._lawn_mower)

        self._state = garden_array

        self.step_count += 1

        return self._state, reward, self.__is_done(), {}

    def reset(self) -> np.array:
        """This method is used to reset the environment, including the lawn mower and the garden."""
        self._previous_mowed_area = 0
        self.step_count = 0
        self._garden.reset()
        self._lawn_mower.reset(self._garden.starting_point.x, self._garden.starting_point.y)
        garden_array = utils.garden_to_array(self._garden, self._lawn_mower)
        return garden_array

    def render(self, mode='human') -> None:
        """This method is used to show the environment."""
        if mode == "human":
            """Renders using matplotlib pyplot"""
            plt.clf()
            utils.plot_polygon(self._garden.grass, 'green')
            if self._garden.mowed_path is not None:
                utils.plot_polygon(self._garden.mowed_path, 'white')
                for interior in self._garden.mowed_path.interiors:
                    utils.plot_polygon(Polygon(interior), 'green')
            for obstacle in self._garden.obstacles:
                utils.plot_polygon(obstacle, 'white')
            utils.plot_point(self._lawn_mower.position, 'pink')
            utils.plot_point(self._garden.starting_point, 'blue')
            utils.plot_point(self._garden.compost_heap, 'brown')
            plt.draw()
            plt.pause(0.00000001)
            plt.savefig('resources/out/' + str(self._episode_count) + '_mowerpath.png')

    def __calculate_reward(self) -> float:
        """This method is used to calculate the reward."""
        current_mowed_area = utils.calculate_polygon_area(self._garden.mowed_path)
        reward = current_mowed_area - self._previous_mowed_area
        self._previous_mowed_area = current_mowed_area
        return reward

    def __is_done(self) -> bool:
        """This method is used to check whether the garden is fully/enough mowed."""
        current_mowable_area = utils.calculate_polygon_area(self._garden.grass.boundary
                                                            .buffer(self._lawn_mower.radius)
                                                            .difference(self._garden.grass))
        for obstacle in self._garden.obstacles:
            current_mowable_area -= utils.calculate_polygon_area(obstacle.union(obstacle.boundary
                                                                                .buffer(self._lawn_mower.radius)))

        current_mowable_area -= utils.calculate_polygon_area(self._garden.mowed_path)

        done = math.isclose(current_mowable_area, 0) or self.step_count >= self._max_steps

        if done:
            self._episode_count += 1

        return done

    def get_mower_location(self) -> Point:
        return self._lawn_mower.position
