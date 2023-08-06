"""Main module."""

import itertools as it
import numpy as np


def read_data(filepath, sep=" "):
    """This function reads file containing Points Coordinates
    
    Arguments:
        filepath {[str]} -- Path to the file to be read
    
    Keyword Arguments:
        sep {str} -- Separator for columns in file (default: {" "})
    
    Returns:
        [list] -- List of points read from input file, in the format [x,y,z]
    """
    with open(filepath, "r") as file:

        raw_lines = file.readlines()

        points = []
        for raw_line in raw_lines:
            coordinates = raw_line.split(sep)[1:4]
            for i in range(3):
                coordinates[i] = float(coordinates[i])
            points.append(coordinates)

    return points


def rototranslation(points):
    """This function generates a rototranslator starting from three
    non-collinear points
    
    Arguments:
        points {[numpy.array]} -- Three non-collinear points in a 3x3
        numpy array [x,y,z]
    
    Returns:
        [numpy.array] -- Rototranslation matrix (4x4 numpy array)
    """

    origin = points[0, :]
    x = points[1, :] - points[0, :]
    x_versor = np.divide(x, np.linalg.norm(x))
    y_1 = points[1, :] - points[0, :]
    y_2 = points[2, :] - points[0, :]
    y = np.cross(y_1, y_2)
    y_versor = np.divide(y, np.linalg.norm(y))
    z_versor = np.cross(x_versor, y_versor)

    rototranslator = np.array(
        [
            np.append(x_versor, 0.0),
            np.append(y_versor, 0.0),
            np.append(z_versor, 0.0),
            np.append(origin, 1.0),
        ]
    ).T

    return rototranslator


def calibrate(world_points, robot_points):
    """This function performs the actual Robot to World Calibration.
    It computes every possibile combination between three non-collinear points,
    computes the correspoding rototranslator and then average the mean
    rototranslator. Everything is expressed in mm.

    Arguments:
        world_points {[numpy.array]} -- Points in World Coordinates
        robot_points {[numpy.array]} -- Points in Robot Coordinates
    
    Raises:
        Exception: Number of points in Robot and World Coordinates
        file is not correspoding.
    
    Returns:
        [dict] -- Dictionary containing the computed rototranslator
        and some informations about the error (mean and standard
        deviation).
    """

    # Import data and remove offset
    points_G = read_data(path_world_file, sep="\t")
    points_R = read_data(path_robot_file, sep=" ")

    if len(points_G) != len(points_R):
        raise Exception(
            """
Number of points must match in robot and world files!
Found {} points in World file and {} points in Robot file""".format(
                len(points_G), len(points_R)
            )
        )

    num_points = len(points_G)

    offset_G_x = -80  # coherence
    offset_G_y = 0  # No offset on y axis
    offset_G_z = 250  # coherence
    offset_G = [offset_G_x, offset_G_y, offset_G_z]

    offset_R_x = 80 - 80  # from TCP to SMR + coherence
    offset_R_y = 0  # No offset on y axis
    offset_R_z = 20 + 25 + 250  # pointer basement along z + SMR along z + coherence
    offset_R = [offset_R_x, offset_R_y, offset_R_z]

    # Remove offset
    points_G = np.array(points_G)
    points_R = np.array(points_R)

    points_G[:, :] = points_G[:, :] - offset_G
    points_R[:, :] = points_R[:, :] - offset_R

    # Generate creation dataset and control dataset
    creation_perc = 0.3
    num_creation_points = round(num_points * creation_perc)
    num_star_points = round(num_points * (1 - creation_perc))

    # At least three points are needed in creation set
    if num_creation_points <= 2:
        num_creation_points = 3
        num_star_points = num_points - num_creation_points
    if num_creation_points + num_star_points != num_points:
        num_star_points = num_star_points - 1

    index_creation = np.round(np.linspace(0, num_points - 1, num_creation_points))
    index_creation = [int(i) for i in index_creation]
    index_star = [i for i in range(num_points) if i not in index_creation]

    points_G_creation = points_G[index_creation, :]
    points_R_creation = points_R[index_creation, :]
    points_star_G_real = points_G[index_star, :]
    points_star_R = points_R[index_star, :]

    # Mean Rototranslation Method
    index_perm = list(
        it.permutations(range(num_creation_points), 3)
    )  # permutations without ripetitions

    creation_perm_G = np.zeros([len(index_perm), 9])
    creation_perm_R = np.zeros([len(index_perm), 9])

    for i in range(len(index_perm)):
        creation_perm_G[i, :3] = points_G_creation[index_perm[i][0], :3]
        creation_perm_G[i, 3:6] = points_G_creation[index_perm[i][1], :3]
        creation_perm_G[i, 6:] = points_G_creation[index_perm[i][2], :3]

        creation_perm_R[i, :3] = points_R_creation[index_perm[i][0], :3]
        creation_perm_R[i, 3:6] = points_R_creation[index_perm[i][1], :3]
        creation_perm_R[i, 6:] = points_R_creation[index_perm[i][2], :3]

    LG_T = np.zeros([4, 4, len(index_perm)])
    LR_T = np.zeros([4, 4, len(index_perm)])
    RL_T = np.zeros([4, 4, len(index_perm)])
    RG_T_temp = np.zeros([4, 4, len(index_perm)])

    # for each permutation, generate the rototranslator
    for i in range(len(index_perm)):
        points_G_current = np.array(
            [creation_perm_G[i, :3], creation_perm_G[i, 3:6], creation_perm_G[i, 6:]]
        )

        points_R_current = np.array(
            [creation_perm_R[i, :3], creation_perm_R[i, 3:6], creation_perm_R[i, 6:]]
        )

        LG_T[:, :, i] = rototranslation(points_G_current)
        LR_T[:, :, i] = rototranslation(points_R_current)
        RL_T[:, :, i] = np.linalg.inv(LR_T[:, :, i])
        RG_T_temp[:, :, i] = np.matmul(LG_T[:, :, i], RL_T[:, :, i])

    RG_T = np.mean(RG_T_temp, axis=2)  # Mean rototranslator

    # Comparison between the three methods
    points_star_R = np.append(
        points_star_R, np.ones([len(points_star_R), 1]), axis=1
    )  # homogeneous

    points_star_G_real = np.append(
        points_star_G_real, np.ones([len(points_star_G_real), 1]), axis=1
    )  # homogeneous

    # estimation starting from T and robot data
    points_star_G_estimated = np.matmul(RG_T, points_star_R.T).T
    # comparison between real and estimated
    error = abs(points_star_G_real - points_star_G_estimated)
    error_mean = np.mean(error, axis=0)[:3]

    error_std_dev = np.std(error, axis=0)[:3]

    results = {
        "Rototranslator": RG_T,
        "Error Mean": error_mean,
        "Error Std Dev": error_std_dev,
    }

    return results
