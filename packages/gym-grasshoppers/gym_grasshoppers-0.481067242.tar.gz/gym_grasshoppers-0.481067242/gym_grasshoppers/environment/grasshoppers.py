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
    _MINIMUM_ANGLE = -180.
    _MAXIMUM_ANGLE = 180.
    _MINIMUM_DISTANCE = 0.1
    _MAXIMUM_DISTANCE = math.inf
    _MINIMUM_SPEED = 0
    _MAXIMUM_SPEED = 1

    def __init__(self, garden_grass_height, garden_geojson: str, mower_angle: float, mower_height: float,
                 mower_radius: float, mower_volume: float, mower_mulching: bool) -> None:
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
        # TODO 16000 niet hardcoded
        self._observation_space = gym.spaces.Box(low=np.zeros(160000, dtype=int),
                                                 high=np.full(160000, 255, dtype=int),
                                                 dtype=np.int)
        self._action_space = gym.spaces.Box(low=np.array([self._MINIMUM_ANGLE, self._MINIMUM_DISTANCE]),

                                            high=np.array([self._MAXIMUM_ANGLE, self._garden_diagonal]),
                                            dtype=np.float16)
        self._ep_ct = 0
        self._state = self.reset()
        self._ep_ct = 0
        self.viewer = None
        self._max_pooling_model = None

    @property
    def state(self):
        return self._state

    @property
    def observation_space(self):
        return self._observation_space

    @property
    def action_space(self):
        return self._action_space

    def step(self, action: Tuple[float, float]) -> Tuple[np.array, float, bool, dict]:
        """This method is used to execute one step in the environment."""
        angle = action[0]
        distance = action[1]

        Turn(self._lawn_mower, angle).execute()
        Move(self._lawn_mower, distance, self._garden).execute()

        reward = self.__calculate_reward(distance)

        self._lawn_mower.current_volume = \
            utils.calculate_polygon_area(self._garden.mowed_path) * self._garden.grass_height

        garden_array = utils.garden_to_array(self._garden, self._lawn_mower)

        self._state = garden_array

        return self._state, reward, self.__is_done(), {}

    def reset(self) -> np.array:
        """This method is used to reset the environment, including the lawn mower and the garden."""
        self._garden.reset()
        self._lawn_mower.reset(self._garden.starting_point.x, self._garden.starting_point.y)
        garden_array = utils.garden_to_array(self._garden, self._lawn_mower)
        self._ep_ct += 1
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
            # plt.draw()
            # plt.pause(0.00000001)
            # plt.savefig('res/out/' + str(self._ep_ct) + '_mowerpath.png') # TODO SAVEFIG

        """
        NOT WORKING PROPERLY

        Renders using matplotlib opengl 
        * unable to solve with triangulation due to being extremely slow with a large mowed path
        """
        # TODO fix opengl rendering if possible
        if mode == 'opengl':
            screen_width = 600
            screen_height = 600
            scale_x = screen_width / self._garden_width
            scale_y = screen_height / self._garden_height

            objects_to_render = []

            if self.viewer is None:
                from gym.envs.classic_control import rendering
                self.viewer = rendering.Viewer(screen_width, screen_height)

            # render grass
            grass = utils.make_scaled_polygon(self._garden.grass, scale_x, scale_y,
                                              self._garden.minimum_x, self._garden.minimum_y, (0, 0.5, 0))
            objects_to_render.extend(grass)

            # render obstacles
            obstacles = [utils.make_scaled_polygon(obstacle, scale_x, scale_y, self._garden.minimum_x,
                                                   self._garden.minimum_y, (1, 0, 0)) for obstacle in
                         list(self._garden.obstacles)]
            for obstacle in obstacles:
                objects_to_render.extend(obstacle)

            # render mowed path
            if self._garden.mowed_path is not None:
                mowed_path = utils.make_scaled_polygon(self._garden.mowed_path, scale_x, scale_y,
                                                       self._garden.minimum_x,
                                                       self._garden.minimum_y, (1, 1, 1))
                objects_to_render.extend(mowed_path)

                for interior in self._garden.mowed_path.interiors:
                    self.viewer.add_geom(utils.make_scaled_polygon(interior, scale_x, scale_y,
                                                                   self._garden.minimum_x,
                                                                   self._garden.minimum_y, (0, 0.5, 0)))

            # render starting point
            starting_point = utils.make_positioned_circle(
                utils.calculate_scaled_radius(self._lawn_mower.position.y, self._lawn_mower.radius) * scale_y,
                (self._garden.starting_point.x - self._garden.minimum_x) * scale_x,
                (self._garden.starting_point.y - self._garden.minimum_y) * scale_y, rgb_color=(0, 0, 1))
            objects_to_render.extend(starting_point)

            # render compost heap
            if self._garden.compost_heap is not None:
                compost_heap = utils.make_positioned_circle(
                    utils.calculate_scaled_radius(self._lawn_mower.position.y, self._lawn_mower.radius) * scale_y,
                    (self._garden.compost_heap.x - self._garden.minimum_x) * scale_x,
                    (self._garden.compost_heap.y - self._garden.minimum_y) * scale_y, rgb_color=(0.5, 0.2, 0))
                objects_to_render.extend(compost_heap)

            # render mower
            mower = utils.make_positioned_circle(
                utils.calculate_scaled_radius(self._lawn_mower.position.y, self._lawn_mower.radius) * scale_y,
                (self._lawn_mower.position.x - self._garden.minimum_x) * scale_x,
                (self._lawn_mower.position.y - self._garden.minimum_y) * scale_y, rgb_color=(1, 0, 0))
            objects_to_render.extend(mower)

            for object in objects_to_render:
                self.viewer.add_geom(object)

            self.viewer.render()

    # TODO: this needs to be refined!
    def __calculate_reward(self, distance: float) -> float:
        """This method is used to calculate the reward."""
        return (utils.calculate_polygon_area(self._garden.mowed_path) *
                self._garden.grass_height) - self._lawn_mower.current_volume - distance

    # TODO: this needs to be refined!
    def __is_done(self) -> bool:
        """This method is used to check whether the garden is fully/enough mowed."""
        current_mowable_area = utils.calculate_polygon_area(self._garden.grass.boundary
                                                            .buffer(self._lawn_mower.radius)
                                                            .difference(self._garden.grass))
        for obstacle in self._garden.obstacles:
            current_mowable_area -= utils.calculate_polygon_area(obstacle.union(obstacle.boundary
                                                                                .buffer(self._lawn_mower.radius)))

        current_mowable_area -= utils.calculate_polygon_area(self._garden.mowed_path)
        return math.isclose(current_mowable_area, 0)

    def get_mower_location(self) -> Point:
        return self._lawn_mower.position
