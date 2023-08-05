import math
import pyproj
import matplotlib.pyplot as plt

from functools import partial
from typing import List, Tuple

from gym_grasshoppers.lawn_mower.lawn_mower import LawnMower

from gym_grasshoppers.garden.garden import Garden
from shapely.ops import transform
from shapely.geometry import GeometryCollection, Point, Polygon
from shapely.ops import triangulate
import numpy as np

"""This module is used as a collection of helper methods."""

EARTH_RADIUS = 6372800


def calculate_distance(lat_long_coordinate_1: Tuple, lat_long_coordinate_2: Tuple) -> float:
    """This method is used to calculate the distance between two coordinates."""
    latitude_1, longitude_1 = lat_long_coordinate_1
    latitude_2, longitude_2 = lat_long_coordinate_2
    geod = pyproj.Geod(ellps='WGS84')
    # geod.inv returns forward [0] and backward [1] azimuths and distance [2]
    return geod.inv(longitude_1, latitude_1, longitude_2, latitude_2)[2]


def plot_points(points: GeometryCollection, color: str = 'red') -> None:
    """This method is used to show a collection of points."""
    for geometry in points.geoms:
        x, y = geometry.coords.xy
        plt.plot([x], [y], marker='o', markersize=3, color=color)


def get_polygon_max_dimensions(polygon: Polygon) -> List:
    """This method is used to calculate the dimensions of a polygon."""
    points = polygon.minimum_rotated_rectangle.bounds
    return points


def plot_polygon(polygon: Polygon, color: str = 'green') -> None:
    """This method is used to show a polygon."""
    x, y = polygon.exterior.xy
    plt.fill(x, y, color=color)
    for interior in polygon.interiors:
        x, y = interior.xy
        plt.fill(x, y, color='white')


def plot_point(point: Point, color: str = 'red') -> None:
    """This method is used to show a point."""
    x, y = point.coords.xy
    plt.plot([x], [y], marker='o', markersize=3, color=color)


def calculate_polygon_area(polygon: Polygon) -> float:
    """This method is used to calculate the area of a polygon."""
    polygon_aea = transform(
        partial(
            pyproj.transform,
            pyproj.Proj(init='EPSG:4326'),
            pyproj.Proj(
                proj='aea',
                lat_1=polygon.bounds[1],
                lat_2=polygon.bounds[3])),
        polygon)
    return polygon_aea.area


def calculate_scaled_radius(latitude: float, radius: float) -> float:
    """This method is used to scale the radius of the lawn mower to the scale of the garden."""
    latitude_radians = math.radians(latitude)
    new_latitude = math.degrees(
        math.asin(math.sin(latitude_radians) * math.cos(radius / EARTH_RADIUS) +
                  math.cos(latitude_radians) * math.sin(radius / EARTH_RADIUS) *
                  math.cos(0.0)))
    return abs(new_latitude - latitude)


def make_positioned_circle(radius, x, y, res=30, rgb_color=(1., 1., 1.)):
    from gym.envs.classic_control.rendering import FilledPolygon, PolyLine
    r, g, b = rgb_color
    points = []
    for i in range(res):
        ang = 2 * math.pi * i / res
        points.append((math.cos(ang) * radius + x, math.sin(ang) * radius + y))
    circle = FilledPolygon(points)
    circle.set_color(r, g, b)
    return [circle]


def make_scaled_polygon(polygon: Polygon, scale_x, scale_y, garden_min_x, garden_min_y, rgb_color=(1., 1., 1.)):
    from gym.envs.classic_control import rendering
    r, g, b = rgb_color
    # triangles = [triangle for triangle in triangulate(polygon) if triangle.within(polygon)]
    triangles_to_render = []
    unionized_triangles = np.empty(1, dtype=Polygon)
    triangles = triangulate(polygon)

    for triangle in triangles:
        unionized_triangles = np.concatenate((np.array(polygon.union(triangle)), unionized_triangles), axis=None)

    for triangle in list(unionized_triangles):
        if triangle is not None:
            triangle_geom = rendering.FilledPolygon([(
                scale_x * (point[0] - garden_min_x), scale_y * (
                        point[1] - garden_min_y))
                for point in list(triangle.exterior.coords)])
            triangle_geom.set_color(r, g, b)
            triangles_to_render.append(triangle_geom)
    return triangles_to_render


def plot_garden(garden: Garden, lawn_mower: LawnMower):
    plt.close()
    plt.clf()

    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    ax.axis('off')

    plot_polygon(garden.grass, 'green')
    if garden.mowed_path is not None:
        plot_polygon(garden.mowed_path, 'white')
        for interior in garden.mowed_path.interiors:
            plot_polygon(Polygon(interior), 'green')
    for obstacle in garden.obstacles:
        plot_polygon(obstacle, 'white')
    plot_point(lawn_mower.position, 'pink')
    plot_point(garden.starting_point, 'blue')
    if garden.compost_heap is not None:
        plot_point(garden.compost_heap, 'brown')


def garden_to_array(garden: Garden, lawn_mower: LawnMower):
    plot_garden(garden, lawn_mower)
    figure = plt.gcf()
    figure.set_size_inches(2, 2)
    figure.canvas.draw()
    rgba_buffer = np.array(figure.canvas.renderer.buffer_rgba())
    gray_buffer = np.dot(rgba_buffer[..., :3], [0.2125, 0.7154, 0.0721])
    # return gray_buffer.flatten()
    # return rgba_buffer.flatten()
    return rgba_buffer
