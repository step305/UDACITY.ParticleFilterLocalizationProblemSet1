# The function localize takes the following arguments:
#
# colors:
#        2D list, each entry either 'R' (for red cell) or 'G' (for green cell)
#
# measurements:
#        list of measurements taken by the robot, each entry either 'R' or 'G'
#
# motions:
#        list of actions taken by the robot, each entry of the form [dy,dx],
#        where dx refers to the change in the x-direction (positive meaning
#        movement to the right) and dy refers to the change in the y-direction
#        (positive meaning movement downward)
#        NOTE: the *first* coordinate is change in y; the *second* coordinate is
#              change in x
#
# sensor_right:
#        float between 0 and 1, giving the probability that any given
#        measurement is correct; the probability that the measurement is
#        incorrect is 1-sensor_right
#
# p_move:
#        float between 0 and 1, giving the probability that any given movement
#        command takes place; the probability that the movement command fails
#        (and the robot remains still) is 1-p_move; the robot will NOT overshoot
#        its destination in this exercise
#
# The function should RETURN (not just show or print) a 2D list (of the same
# dimensions as colors) that gives the probabilities that the robot occupies
# each cell in the world.
#
# Compute the probabilities by assuming the robot initially has a uniform
# probability of being in any cell.
#
# Also assume that at each step, the robot:
# 1) first makes a movement,
# 2) then takes a measurement.
#
# Motion:
#  [0,0] - stay
#  [0,1] - right
#  [0,-1] - left
#  [1,0] - down
#  [-1,0] - up


def create_map(orig_map, fill_value):
    q = [x[:] for x in orig_map]
    for y, row in enumerate(orig_map):
        for x, _ in enumerate(row):
            q[y][x] = fill_value
    return q


def localize(colors, measurements, motions, sensor_right, p_move):
    # initializes p to a uniform distribution over a grid of the same dimensions as colors
    pinit = 1.0 / float(len(colors)) / float(len(colors[0]))
    pl = create_map(colors, pinit)

    # >>> Insert your code here <<<

    for measurement, motion in zip(measurements, motions):
        pl = move(pl, motion[1], motion[0], p_move)
        pl = sense(pl, measurement, colors, sensor_right)
    return pl


def sense(pl, z, color_map, sensor_right):
    q = create_map(pl, 0.0)

    for y, row in enumerate(color_map):
        for x, elem in enumerate(row):
            if z == elem:
                q[y][x] = pl[y][x] * sensor_right
            else:
                q[y][x] = pl[y][x] * (1.0 - sensor_right)

    norm = sum([sum(row) for row in q])

    for y, row in enumerate(q):
        for x, elem in enumerate(row):
            q[y][x] = elem / norm
    return q


def move(pl, dx, dy, p_move):
    q = create_map(pl, 0.0)

    y_max = len(pl)
    x_max = len(pl[0])

    for y, row in enumerate(pl):
        for x, elem in enumerate(row):
            if abs(dx) > 0:
                x_neihbor = (x - dx)
                q[y][x] = (1 - p_move) * elem
                x_neihbor = x_neihbor % x_max
                q[y][x] += pl[y][x_neihbor] * p_move
            elif abs(dy) > 0:
                y_neihbor = y - dy
                q[y][x] = (1 - p_move) * elem
                y_neihbor = y_neihbor % y_max
                q[y][x] += pl[y_neihbor][x] * p_move
            else:
                q[y][x] = pl[y][x]
    return q


def show(p):
    rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x), r)) + ']' for r in p]
    print('[' + ',\n '.join(rows) + ']')


if __name__ == '__main__':
    #############################################################
    # For the following test case, your output should be
    # [[0.01105, 0.02464, 0.06799, 0.04472, 0.02465],
    #  [0.00715, 0.01017, 0.08696, 0.07988, 0.00935],
    #  [0.00739, 0.00894, 0.11272, 0.35350, 0.04065],
    #  [0.00910, 0.00715, 0.01434, 0.04313, 0.03642]]
    # (within a tolerance of +/- 0.001 for each entry)

    colors = [['R', 'G', 'G', 'R', 'R'],
              ['R', 'R', 'G', 'R', 'R'],
              ['R', 'R', 'G', 'G', 'R'],
              ['R', 'R', 'R', 'R', 'R']]
    measurements = ['G', 'G', 'G', 'G', 'G']
    motions = [[0, 0], [0, 1], [1, 0], [1, 0], [0, 1]]
    p = localize(colors, measurements, motions, sensor_right=0.7, p_move=0.8)
    show(p)  # displays your answer
