import math

# Function to create square stitch sequence
def getSquare():
    stitches = [128, 2]  # 128 = escape_character , 2=Move
    stitches += [0, 0]  # followed by 8 bit displacement X,Y
    stitches += [206, 206]  # followed by another 8 bit displacement X,Y
    # Note: Displacements are in 0.1mm units. If number is greater than 128, then it represents
    # a negative distance calculated by subtracting the number from 256 and multiplying by 0.1mm

    for i in range(0, 10):
        stitches += [10, 0, ]  # add ten 1mm stitches going right
    for i in range(0, 10):
        stitches += [0, 10, ]  # add ten 1mm stitches going up

    # Change thread
    stitches += [128, 1]  # 128 = escape_character -> 1 = Change to next thread in list

    for i in range(0, 10):
        stitches += [246, 0, ]  # add ten 1mm stitches going left
    for i in range(0, 10):
        stitches += [0, 246, ]  # add ten 1mm stitches going down

    stitches += [128, 16]  # 128 = escape_character , 16=last_stitch
    return stitches


# Function to create circle stitch sequence
def getCircle():
    stitches = [128, 2]  # 128 = escape_character , 2=Move
    stitches += [0, 0]  # followed by 8 bit displacement X,Y
    stitches += [206, 206]
    # Note: Displacements are in 0.1mm units. If number is greater than 128, then it represents
    # a negative distance calculated by subtracting the number from 256 and multiplying by 0.1mm

    r = 100
    for i in range(1, 19):
        y_disp = r * math.sin(math.radians(10 * i)) - r * math.sin(math.radians(10 * (i - 1)))
        x_disp = r * math.cos(math.radians(10 * i)) - r * math.cos(math.radians(10 * (i - 1)))
        y_disp = int(y_disp)
        if y_disp < 0:
            y_disp = 256 + y_disp
        x_disp = int(x_disp)
        if x_disp < 0:
            x_disp = 256 + x_disp
        stitches += [x_disp, y_disp]  # add 18 circular stitches

    # Change thread
    stitches += [128, 1]  # 128 = escape_character -> 1 = Change to next thread in list

    stitches += [0, 0]
    for i in range(19, 37):
        y_disp = r * math.sin(math.radians(10 * i)) - r * math.sin(math.radians(10 * (i - 1)))
        x_disp = r * math.cos(math.radians(10 * i)) - r * math.cos(math.radians(10 * (i - 1)))
        y_disp = int(y_disp)
        if y_disp < 0:
            y_disp = 256 + y_disp
        x_disp = int(x_disp)
        if x_disp < 0:
            x_disp = 256 + x_disp
        stitches += [x_disp, y_disp]  # add 18 circular stitches

    stitches += [128, 16]  # 128 = escape_character , 16=last_stitch
    return stitches


def getEllipse(a, b, theta):
    stitches = [128, 2]  # 128 = escape_character , 2=Move
    stitches += [0, 0]  # followed by 8 bit displacement X,Y
    stitches += [206, 206]
    # Note: Displacements are in 0.1mm units. If number is greater than 128, then it represents
    # a negative distance calculated by subtracting the number from 256 and multiplying by 0.1mm

    pos_x = []  # create array for x position data
    pos_y = []  # create array for y position data
    for i in range(-a, a, 2):
        y_pos = int(math.sqrt((-b ** 2 / a ** 2) * i ** 2 + b ** 2))
        x_pos = i
        pos_x += [x_pos]  # add x position data
        pos_x += [x_pos]  # add same x position data again (stitch top to bottom)
        pos_y += [y_pos]  # add y position data for top of ellipse
        pos_y += [-y_pos]  # add y position data for bottom of ellipse

    # rotate position data by multiplying by a rotation matrix
    rot_x = []
    rot_y = []
    for i in range(len(pos_x)):
        x1 = pos_x[i] * math.cos(theta) - pos_y[i] * math.sin(theta)
        y1 = pos_x[i] * math.sin(theta) + pos_y[i] * math.cos(theta)
        rot_x += [x1]
        rot_y += [y1]

    # translate position data to displacement data
    for i in range(1, int(len(rot_x) / 2)):
        x_disp = rot_x[i] - rot_x[i - 1]
        y_disp = rot_y[i] - rot_y[i - 1]
        y_disp = int(y_disp)
        if y_disp < 0:
            y_disp = 256 + y_disp
        x_disp = int(x_disp)
        if x_disp < 0:
            x_disp = 256 + x_disp
        stitches += [x_disp, y_disp]

    # Change thread
    stitches += [128, 1]  # 128 = escape_character -> 1 = Change to next thread in list

    for i in range(int(len(rot_x) / 2), len(rot_x)):
        x_disp = rot_x[i] - rot_x[i - 1]
        y_disp = rot_y[i] - rot_y[i - 1]
        y_disp = int(y_disp)
        if y_disp < 0:
            y_disp = 256 + y_disp
        x_disp = int(x_disp)
        if x_disp < 0:
            x_disp = 256 + x_disp
        stitches += [x_disp, y_disp]

    stitches += [128, 16]  # 128 = escape_character , 16=last_stitch
    return stitches

def leaf(x, y, a, b, theta):
    pos_x = []  # create array for x position data
    pos_y = []  # create array for y position data
    x_pos = 0 # starting position
    y_top = 0 # starting position
    y_bottom = 0

    # fill in leaf at origin
    for i in range(-a, a, 2):
        y_top = int(math.sqrt((-b ** 2 / a ** 2) * i ** 2 + b ** 2))
        y_bottom = -int(math.sqrt((-b ** 2 / a ** 2) * i ** 2 + b ** 2))
        x_pos = a + i
        pos_x += [x_pos]  # add x position data
        pos_x += [x_pos]  # add same x position data again (stitch top to bottom)
        pos_y += [y_top]  # add y position data for top of ellipse
        pos_y += [y_bottom]  # add y position data for bottom of ellipse

    # return to starting position and draw leaf center line
    end_x = x_pos
    end_y = (y_top + y_bottom)/2
    for i in range(2 * a, -20, -10):
        x_pos = i
        y_pos = end_y
        pos_x += [round(x_pos)]
        pos_y += [round(y_pos)]

    # rotate position data by multiplying by a rotation matrix
    rot_x = []
    rot_y = []
    for i in range(0, len(pos_x)-1):
        x1 = round(pos_x[i] * math.cos(theta) - pos_y[i] * math.sin(theta))
        y1 = round(pos_x[i] * math.sin(theta) + pos_y[i] * math.cos(theta))
        rot_x += [x1]
        rot_y += [y1]

    # translate leaf to given starting position
    trans_x = []
    trans_y = []
    for i in range(len(rot_x)):
        x1 = rot_x[i] + x
        y1 = rot_y[i] + y
        trans_x += [x1]
        trans_y += [y1]

    return trans_x, trans_y

def stem(x, y, length, stem_theta):

    pos_x = []
    pos_y = []
    move_x = x
    move_y = y
    x = 0
    y = 0
    branch_theta = 0.5
    # define stem length that reduces each iteration
    for i in range (length, 30, -20):
        # main stem
        start_x = x
        start_y = y
        for j in range (0, i+1, 10):
            x = start_x + j * math.cos(stem_theta)
            y = start_y + j * math.sin(stem_theta)
            pos_x += [x]
            pos_y += [y]
        # left branch
        start_x = x
        start_y = y
        for j in range (0, i+1, 10):
            x = start_x + j * math.cos(stem_theta + branch_theta)
            y = start_y + j * math.sin(stem_theta + branch_theta)
            pos_x += [x]
            pos_y += [y]
        # left leaf
        leaf_x, leaf_y = leaf(round(x), round(y), round(3*i/4), round(i/4), stem_theta + branch_theta)
        pos_x += leaf_x
        pos_y += leaf_y
        # back along left branch to center
        for j in range (i+1, 0, -10):
            x = start_x + j * math.cos(stem_theta + branch_theta)
            y = start_y + j * math.sin(stem_theta + branch_theta)
            pos_x += [x]
            pos_y += [y]
        #main stem continued
        for j in range (0, i+1, 10):
            x = start_x + j * math.cos(stem_theta)
            y = start_y + j * math.sin(stem_theta)
            pos_x += [x]
            pos_y += [y]
        # right branch
        start_x = x
        start_y = y
        for j in range (0, i, 10):
            x = start_x + j * math.cos(stem_theta - branch_theta)
            y = start_y + j * math.sin(stem_theta - branch_theta)
            pos_x += [x]
            pos_y += [y]
        # right leaf
        leaf_x, leaf_y = leaf(round(x), round(y), round(3*i/4), round(i/4), stem_theta - branch_theta)
        pos_x += leaf_x
        pos_y += leaf_y
        # back along right branch to center
        for j in range (i+1, 0, -10):
            x = start_x + j * math.cos(stem_theta - branch_theta)
            y = start_y + j * math.sin(stem_theta - branch_theta)
            pos_x += [x]
            pos_y += [y]
    #get back to start of stem
    end_x = x
    end_y = y
    length = round(math.sqrt(end_x**2 + end_y**2))
    for i in range(length, 0, -10):
        x_pos = i * math.cos(stem_theta)
        y_pos = i * math.sin(stem_theta)
        pos_x += [x_pos]
        pos_y += [y_pos]

    # translate stem to given starting position
    trans_x = []
    trans_y = []
    for i in range(len(pos_x)):
        x1 = pos_x[i] + move_x
        y1 = pos_y[i] + move_y
        trans_x += [x1]
        trans_y += [y1]

    return trans_x, trans_y

def branch():

    spiral_length = 29
    pos_x = []  # create array for x position data
    pos_y = []  # create array for y position data
    x_pos = 0
    y_pos = 0
    pos_x += [x_pos]
    pos_y += [y_pos]

    for i in range(spiral_length * 4, 0, -1):
        bend_angle = i / 32
        y_pos = 4 * i * math.sin(bend_angle)
        x_pos = 4 * i * math.cos(bend_angle)
        pos_x += [x_pos]  # add x position data
        pos_y += [y_pos]  # add y position data
        # add branch
        if i % 20 == 0:
            stem_theta = math.atan((pos_y[-1] - pos_y[-2])/(pos_x[-1] - pos_x[-2]))
            branchx, branchy = stem(round(x_pos), round(y_pos), i, stem_theta)
            pos_x += branchx
            pos_y += branchy
    end_x = x_pos
    end_y = y_pos

    #spiral back to start
    for i in range(0, spiral_length * 4, 1):
        bend_angle = i / 32
        y_pos = end_y + 4 * i * math.sin(bend_angle)
        x_pos = end_x + 4 * i * math.cos(bend_angle)
        pos_x += [x_pos]  # add x position data
        pos_y += [y_pos]  # add y position data

    pos_x += [0]
    pos_y += [0]

    return pos_x, pos_y

def wreath():
    stitches = [128, 2]  # 128 = escape_character , 2=Move
    stitches += [0, 0]  # followed by 8 bit displacement X,Y
    # Note: Displacements are in 0.1mm units. If number is greater than 128, then it represents
    # a negative distance calculated by subtracting the number from 256 and multiplying by 0.1mm

    spiral_length = 29
    pos_x = []  # create array for x position data
    pos_y = []  # create array for y position data
    x_pos = 0
    y_pos = 0

    # create branches at different angles
    rot_x = []
    rot_y = []
    for i in range (0, 360, 120):
        pos_x, pos_y = branch()
        # rotate position data by multiplying by a rotation matrix

        for j in range(0, len(pos_x)-1):
            x1 = round(pos_x[j] * math.cos(math.radians(i)) - pos_y[j] * math.sin(math.radians(i)))
            y1 = round(pos_x[j] * math.sin(math.radians(i)) + pos_y[j] * math.cos(math.radians(i)))
            rot_x += [x1]
            rot_y += [y1]

    # convert position to displacement
    for i in range(1, len(rot_x)):
        x_disp = rot_x[i] - rot_x[i - 1]
        y_disp = rot_y[i] - rot_y[i - 1]
        y_disp = round(y_disp)
        if y_disp >= 256:
            y_disp = 0
        if y_disp <= -256:
            y_disp = 0
        if y_disp < 0:
            y_disp = 256 + y_disp
        x_disp = round(x_disp)
        if x_disp >= 256:
            x_disp = 0
        if x_disp <= -256:
            x_disp = 0
        if x_disp < 0:
            x_disp = 256 + x_disp
        stitches += [x_disp, y_disp]

    stitches += [128, 16]  # 128 = escape_character , 16=last_stitch

    return stitches

def test():
    stitches = [128, 2]  # 128 = escape_character , 2=Move
    stitches += [0, 0]  # followed by 8 bit displacement X,Y
    # Note: Displacements are in 0.1mm units. If number is greater than 128, then it represents
    # a negative distance calculated by subtracting the number from 256 and multiplying by 0.1mm

    x_pos = 500
    y_pos = 500
    pos_x = []  # create array for x position data
    pos_y = []  # create array for y position data

    #create spiral
    spiral_length = 29
    x_pos = 0
    y_pos = 0
    for i in range(spiral_length * 4, 0, -1):
        bend_angle = i / 32
        y_pos = 4 * i * math.sin(bend_angle)
        x_pos = 4 * i * math.cos(bend_angle)
        pos_x += [x_pos]  # add x position data
        pos_y += [y_pos]  # add y position data

    end_x = x_pos
    end_y = y_pos
    #spiral back to start
    for i in range(0, spiral_length * 4, 1):
        bend_angle = i / 32
        y_pos = end_y + 4 * i * math.sin(bend_angle)
        x_pos = end_x + 4 * i * math.cos(bend_angle)
        pos_x += [x_pos]  # add x position data
        pos_y += [y_pos]  # add y position data

    """
    #create stem
    stem_x, stem_y = stem(90, 90, 120, 10)
    pos_x += stem_x
    pos_y += stem_y
    
    #create leaf left
    leaf_x, leaf_y = leaf(50, 50, 60, 20, 30)
    pos_x += leaf_x
    pos_y += leaf_y

    #create leaf right
    leaf_x, leaf_y = leaf(50, 50, 60, 20, 120)
    pos_x += leaf_x
    pos_y += leaf_y
    """

    # convert position to displacement
    for i in range(1, len(pos_x)):
        x_disp = pos_x[i] - pos_x[i - 1]
        y_disp = pos_y[i] - pos_y[i - 1]
        y_disp = round(y_disp)
        if y_disp >= 256:
            y_disp = 0
        if y_disp <= -256:
            y_disp = 0
        if y_disp < 0:
            y_disp = 256 + y_disp
        x_disp = round(x_disp)
        if x_disp >= 256:
            x_disp = 0
        if x_disp <= -256:
            x_disp = 0
        if x_disp < 0:
            x_disp = 256 + x_disp
        stitches += [x_disp, y_disp]

    stitches += [128, 16]  # 128 = escape_character , 16=last_stitch

    return stitches


# Function to create JEF file header
def getJefHeader(num_stitches):
    jefBytes = [128, 0, 0, 0,  # The byte offset of the first stitch
                10, 0, 0, 0,  # unknown command
                ord("2"), ord("0"), ord("2"), ord("1"),  # YYYY
                ord("0"), ord("2"), ord("2"), ord("4"),  # MMDD
                ord("1"), ord("5"), ord("2"), ord("1"),  # HHMM
                ord("0"), ord("0"), 99, 0,  # SS00
                1, 0, 0, 0,  # Thread count nr. (nr of thread changes)
                (num_stitches) & 0xff, (num_stitches) >> 8 & 0xff, 0, 0,  # Number of stitches
                3, 0, 0, 0,  # Sewing machine Hoop
                # Extent 1
                50, 0, 0, 0,  # Left boundary dist from center (in 0.1mm)
                50, 0, 0, 0,  # Top boundary dist from center (in 0.1mm)
                50, 0, 0, 0,  # Right boundary dist from center (in 0.1mm)
                50, 0, 0, 0,  # Bottom boundary dist from center (in 0.1mm)
                # Extent 2
                50, 0, 0, 0,  # Left boundary dist from center (in 0.1mm)
                50, 0, 0, 0,  # Top boundary dist from center (in 0.1mm)
                50, 0, 0, 0,  # Right boundary dist from center (in 0.1mm)
                50, 0, 0, 0,  # Bottom boundary dist from center (in 0.1mm)
                # Extent 3
                50, 0, 0, 0,  # Left boundary dist from center (in 0.1mm)
                50, 0, 0, 0,  # Top boundary dist from center (in 0.1mm)
                50, 0, 0, 0,  # Right boundary dist from center (in 0.1mm)
                50, 0, 0, 0,  # Bottom boundary dist from center (in 0.1mm)
                # Extent 4
                50, 0, 0, 0,  # Left boundary dist from center (in 0.1mm)
                50, 0, 0, 0,  # Top boundary dist from center (in 0.1mm)
                50, 0, 0, 0,  # Right boundary dist from center (in 0.1mm)
                50, 0, 0, 0,  # Bottom boundary dist from center (in 0.1mm)
                # Extent 5
                50, 0, 0, 0,  # Left boundary dist from center (in 0.1mm)
                50, 0, 0, 0,  # Top boundary dist from center (in 0.1mm)
                50, 0, 0, 0,  # Right boundary dist from center (in 0.1mm)
                50, 0, 0, 0,  # Bottom boundary dist from center (in 0.1mm)
                5, 0, 0, 0,  # Thread Color (white)
                2, 0, 0, 0,  # Thread Color (white)
                13, 0, 0, 0,  # Thread type (unknown)
                ]
    return jefBytes


# Main program combines headers and stitch sequence

def main():
    stitchseq = wreath()
    header = getJefHeader(len(stitchseq) // 2)
    data = bytes(header) + bytes(stitchseq)
    with open("wreath.jef", "wb") as f:
        f.write(data)


if __name__ == '__main__':
    main()
