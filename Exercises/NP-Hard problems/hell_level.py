import pylab as pl
import numpy as np
from jax import jit
import jax.numpy as jnp
from numba import njit
from copy import deepcopy


@njit()
def encoding_to_direction(encoding):
    if encoding == 0:
        return np.array([0, 1], dtype=np.int8)
    if encoding == 1:
        return np.array([1, 0], dtype=np.int8)
    if encoding == 2:
        return np.array([0, -1], dtype=np.int8)
    if encoding == 3:
        return np.array([-1, 0], dtype=np.int8)


class Laser:
    def __init__(self, location, direction):
        self.location = location
        self.direction = direction


class Level:
    """The level is represented as a integer matrix
        0: Empty cell
        1: Movable obstacle
        2: Unmovable obstacle
        3: LASER source
        4: LASER beam
        5: Target to break
        10: Player
    """

    def __init__(self, size, start) -> None:
        self.size = np.array(size, dtype=np.int8)
        self.targets = 0
        self.lasers = set()
        self.current_pos = np.array(start, dtype=np.int8)
        self.level_matrix = np.zeros(tuple(self.size), dtype=np.int8)

        self.level_matrix[tuple(self.current_pos)] = 10

    def step(self, encoding):
        if self.targets == 0:
            return 0

        direction = encoding_to_direction(encoding)
        destination = self.current_pos + direction

        if self.is_empty(destination):
            self.update_pos(destination)

        elif self.is_movable(destination, direction):
            self.update_obstacle(destination, direction)

        elif self.is_target(destination):
            self.targets -= 1
            self.add_unmovable_obstacle(destination)

        return -1

    def is_valid_cell(self, cell):
        return cell[0] < self.size[0] and cell[1] < self.size[1] \
            and cell[0] >= 0 and cell[1] >= 0

    def is_empty(self, cell):
        if self.is_valid_cell(cell):
            return self.level_matrix[tuple(cell)] == 0

        return False

    def is_movable(self, cell, direction):
        if not self.is_valid_cell(cell):
            return False

        if self.level_matrix[tuple(cell)] != 1:
            return False

        destination = cell+direction
        return self.is_empty(destination) or self.is_laser_beam(destination)

    def is_target(self, cell):
        return self.is_valid_cell(cell) and self.level_matrix[tuple(cell)] == 5

    def is_laser_beam(self, cell):
        if self.is_valid_cell(cell):
            return self.level_matrix[tuple(cell)] == 4
        return False

    def add_obstacle(self, location):
        self.level_matrix[tuple(location)] = 1
        self.recompute_laser_beams()

    def remove_obstacle(self, location):
        self.level_matrix[location] = 0
        self.recompute_laser_beams()

    def add_unmovable_obstacle(self, location):
        self.level_matrix[tuple(location)] = 2
        self.recompute_laser_beams()

    def add_laser(self, location, direction):
        location = np.array(location, dtype=np.int8)
        direction = np.array(direction, dtype=np.int8)
        self.lasers.add(Laser(location, direction))

        self.level_matrix[tuple(location)] = 3
        self.recompute_laser_beams()
        
    def add_target(self, location):
        self.level_matrix[tuple(location)] = 5
        self.targets += 1

        self.recompute_laser_beams()

    def update_pos(self, destination):
        self.level_matrix[tuple(self.current_pos)] = 0
        self.level_matrix[tuple(destination)] = 10
        self.current_pos = destination.copy()

    def update_obstacle(self, destination, direction):
        self.level_matrix[tuple(destination)] = 0
        self.level_matrix[tuple(destination+direction)] = 1
        self.recompute_laser_beams()

    def recompute_laser_beams(self):
        self.level_matrix[self.level_matrix == 4] = 0
        for laser in self.lasers:
            location, direction = laser.location.copy(), laser.direction.copy()
            location += direction

            while self.is_empty(location) or self.is_laser_beam(location):
                self.level_matrix[tuple(location)] = 4
                location += direction
        
    def display_level(self):
        pl.imshow(self.level_matrix, origin="lower")
        pl.show()