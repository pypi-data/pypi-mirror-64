#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Colisional Algorithm.

Developed by: E. S. Pereira.
e-mail: pereira.somoza@gmail.com


Copyright [2019] [E. S. Pereira]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import numpy as np
from numpy import array


class ShapeError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def normalize(v):
    norm = np.sqrt(v[:,0] ** 2 + v[:,1] ** 2)
    return v / norm.reshape(v.shape[0], 1)

def orthogonal(v):
    tmp = v.copy()
    tmp[:,0] = v[:,1]
    tmp[:,1] = - v[:,0]
    return tmp

def vertices_to_edges(vertices):
    edg = np.append(vertices, [vertices[0,:]], axis=0)
    edg  = edg[1:,:]- edg[0:-1,:]
    return edg

def project(vertices, axis):
    dots = vertices.dot(axis)
    return np.array([np.min(dots), np.max(dots)])

def contains(n, range_):
    a = range_[0]
    b = range_[1]
    if b < a:
        a = range_[1]
        b = range_[0]
    return (n >= a) and (n <= b);

def overlap(a, b):
    if contains(a[0], b):
        return True;
    if contains(a[1], b):
        return True;
    if contains(b[0], a):
        return True;
    if contains(b[1], a):
        return True;
    return False;

def separating_axis_theorem(vertices_a, vertices_b):
    edges_a = vertices_to_edges(vertices_a);
    edges_b = vertices_to_edges(vertices_b);

    edges = np.append(edges_a, edges_b, axis=0)

    axes = normalize(orthogonal(edges))

    for i in range(len(axes)):
        projection_a = project(vertices_a, axes[i])
        projection_b = project(vertices_b, axes[i])
        overlapping = overlap(projection_a, projection_b)
        if not overlapping:
            return False;
    return True

class BoundBox2D:
    """
    BoundBox2D:
    Parameters:
    :param array vertices: Numpy array representing the vertices of a rectangle.
    """

    def __init__(self, vertices):

        self._vertices = vertices
        if isinstance(self.vertices, np.ndarray) is False:
            self.vertices = array(self.vertices).astype(np.int)

        if self.vertices.shape[1] != 2:
            msg = "The vertices must be a numpy array with 2 colums"
            msg += "Input shape: {0}x{1}".format(*self.vertices.shape)
            raise ShapeError(msg)

    def get_vertices(self):
        return self._vertices

    def set_vertices(self, vertices):
        if isinstance(vertices, np.ndarray) is False:
            vertices = array(vertices).astype(np.int)

        if vertices.shape[1] != 2:
            msg = "The vertices must be a numpy array with 2 colums"
            msg += "Input shape: {0}x{1}".format(*vertices.shape)
            raise ShapeError(msg)

        self._vertices = vertices

    def collision(self, boundboux2d):
        return separating_axis_theorem(boundboux2d.vertices, self._vertices)

    # def plot_box(self, boundboux2d=None):
    #     import matplotlib.pyplot as plt
    #     fig = plt.figure(1, figsize=(5, 5), dpi=90)
    #     ax = fig.add_subplot(111)
    #
    #     vtmp = self.vertices.copy()
    #     vtmp = np.append(vtmp, [vtmp[0, :]], axis=0)
    #     ax.plot(vtmp[:, 0], vtmp[:, 1], color='blue', alpha=0.7,
    #             linewidth=3, solid_capstyle='round', zorder=2, label="1")
    #
    #     if boundboux2d is not None:
    #         vtmp = boundboux2d.vertices.copy()
    #         vtmp = np.append(vtmp, [vtmp[0, :]], axis=0)
    #         vtmp = array(vtmp)
    #         ax.plot(vtmp[:, 0], vtmp[:, 1], color='red', alpha=0.7,
    #                 linewidth=3, solid_capstyle='round', zorder=2, label="2")
    #
    #     plt.legend()
    #     plt.show()

    vertices = property(get_vertices, set_vertices)
