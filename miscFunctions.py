import math
from math import sin, cos, radians

def rotatePoint(point, angle, center_point=(0, 0)):
    """Rotates a point around center_point(origin by default)
    Angle is in degrees.
    Rotation is counter-clockwise
    """
    angle_rad = radians(angle % 360)
    # Shift the point so that center_point becomes the origin
    new_point = (point[0] - center_point[0], point[1] - center_point[1])
    new_point = (new_point[0] * cos(angle_rad) - new_point[1] * sin(angle_rad),
                 new_point[0] * sin(angle_rad) + new_point[1] * cos(angle_rad))
    # Reverse the shifting we have done
    new_point = (new_point[0] + center_point[0], new_point[1] + center_point[1])
    return new_point

def rotatePolygon(polygon, angle, center_point=(0, 0)):
    """Rotates the given polygon which consists of corners represented as (x,y)
    around center_point (origin by default)
    Rotation is counter-clockwise
    Angle is in degrees
    """
    rotated_polygon = []
    for corner in polygon:
        rotated_corner = rotatePoint(corner, angle, center_point)
        rotated_polygon.append(rotated_corner)
    return rotated_polygon

def constrainMin(value, minimum):
    """Constrains a value to a given min value
    """
    if value < minimum:
        return minimum
    else: return value

def constrainMax(value, maximum):
    """Constrains a value to a given max value
    """
    if value > maximum:
        return maximum
    else: return value

def mapVal(x, input_min, input_max, output_min, output_max):
    return (x - input_min) * (output_max - output_min) / (input_max - input_min) + output_min