"""
Graphics module for erdorbit.
"""

# third party imports
import numpy as np
from processing_py import *
from tqdm import tqdm


def resize_drawing_to_fit_canvas(positions, canvas_height, DRAWING_SIZE_FACTOR):
    """
    This function resizes the drawing to fit the canvas size
    Input:
        input_coords            [[float, float, float], ...]
            x, y, z, position in km
        canvas_height           float
        DRAWING_SIZE_FACTOR     float
    Output:
        output_coords           [[float, float, float], ...]
            x, y, z, position in canvas dimension
    """

    # assuming size of object to draw is 2 times largest value in positions array
    drawing_size = np.max(np.abs(np.asarray(positions))) * 2

    return np.asarray(positions) * canvas_height / drawing_size * DRAWING_SIZE_FACTOR


def planar_projection(input_array, alpha, beta):
    """
    Projecting an array of 3D coordinates on a plane
    Inputs:
        input_array     [[float, float, float], ...]
            3D position expressed as x, y, z
        alpha           float
            rotation of the projection plane around intersection of itself and Oxy plane (radians)
        beta            float
            rotation of the projection plane around Oz (radians)
    Outputs:
        output_array    [[float, float], ...]
            2D projection of input positions expressed as x, y
    """

    output_array = []
    for i in range(len(input_array)):
        output_array.append(
            [
                np.cos(beta) * input_array[i][0] - np.sin(beta) * input_array[i][1],
                -np.sin(beta) * np.sin(alpha) * input_array[i][0]
                - np.cos(beta) * np.sin(alpha) * input_array[i][1]
                + np.cos(alpha) * input_array[i][2],
            ]
        )

    return output_array


def rotate_coordinates(input_coords, delta):
    """
    This functions rotates 2D coordinates around the center of the reference
    frame from a 'delta' angle.
    Input:
        input_coords    [[float, float], ...]
            2D coordinates expressed as x, y
        delta           float
            rotation of the projected vector around the normal to the projection plane, in radians
    Output:
        output_coords   [[float, float], ...]
            2D coordinates expressed as x, y
    """

    output_coords = []

    for i in range(len(input_coords)):
        output_coords.append(
            [
                np.cos(delta) * input_coords[i][0] + np.sin(delta) * input_coords[i][1],
                np.cos(delta) * input_coords[i][1] - np.sin(delta) * input_coords[i][0],
            ]
        )

    return output_coords


def translate_coordinates(input_coords, dx, dy):
    """
    This function translates the positions in a 2D reference frame
    Inputs:
        input_coords    [[float, float], ...]
            2D coordinates expressed as x, y
        dx              float
            translation along x axis
        dy              float
            translation along y axis
    Output:
        output_coords   [[float, float, ], ...]
            2D coordinates expressed as x, y
    """

    output_coords = []

    for i in range(len(input_coords)):

        output_coords.append([input_coords[i][0] + dx, input_coords[i][1] + dy])

    return output_coords


def adapt_coordinates_to_canvas_frame(input_coords, canvas_width, canvas_height):
    """
    The reference frame of the canvas is centered in the upper left corner, with the X axis
    pointing to the right, and the Y axis pointing down.
    This function transforms 2D coordinates so that the drawing is centered at the center of the
    canvas, with the Y axis pointing up.
    Input:
        input_coords    [[float, float], ...]
            array of 2D coordinates expressed in a "classical" cartesian reference frame
        canvas_width    float
        canvas_height   float
    Output:
        output_coords   [[float, float], ...]
            array of 2D coordinates, adapted to the canvas' reference frame
    """

    output_coords = []

    for i in range(len(input_coords)):

        output_coords.append(
            [
                input_coords[i][0] + canvas_width / 2,
                -input_coords[i][1] + canvas_height / 2,
            ]
        )

    return output_coords


# drawing orbit
def draw_orbit(
    positions,
    alpha,
    beta,
    delta,
    x_translation,
    y_translation,
    canvas_width,
    canvas_height,
):
    """
    This function draws the trajectory of an orbiting object on the canvas
    This function calls several previously defined functions
    Input:
        pos             [[float, float, float], ...]
            array of 3D cartesian positions the orbiting object
        alpha           float
            projection plane angle
        beta            float
            projection plane angle
        delta           float
            drawing rotation angle
        x_translation   float
            drawing translation along x-axis
        y_translation   float
            drawing translation along y-axis
        canvas_width    float
        canvas_height   float
    """

    app = App(int(canvas_width), int(canvas_height))  # create window: width, height
    app.background(255, 255, 255)  # set white background
    app.stroke(0, 0, 0)  # set stroke color to black

    positions_2d = planar_projection(positions, alpha, beta)

    positions_2d = rotate_coordinates(positions_2d, delta)

    positions_2d = translate_coordinates(positions_2d, x_translation, y_translation)

    positions_2d = adapt_coordinates_to_canvas_frame(
        positions_2d, canvas_width, canvas_height
    )

    # drawing line
    for i in tqdm(range(len(positions_2d) - 1)):
        app.line(
            positions_2d[i][0],
            positions_2d[i][1],
            positions_2d[i + 1][0],
            positions_2d[i + 1][1],
        )

    app.redraw()  # refresh drawing
