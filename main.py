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

def getFern():
    stitches = [128, 2]  # 128 = escape_character , 2=Move
    stitches += [0, 0]  # followed by 8 bit displacement X,Y
    # Note: Displacements are in 0.1mm units. If number is greater than 128, then it represents
    # a negative distance calculated by subtracting the number from 256 and multiplying by 0.1mm

    def leaf(x, y, a, b, theta):
        leaves = [] # create array for displacement data that will be added to stitches array
        pos_x = []  # create array for x position data
        pos_y = []  # create array for y position data
        x_pos = x # starting position
        y_pos = y # starting position

        # fill in leaf
        for i in range(-a, a, 2):
            y_pos = y + int(math.sqrt((-b ** 2 / a ** 2) * i ** 2 + b ** 2))
            x_pos = x + i
            pos_x += [x_pos]  # add x position data
            pos_x += [x_pos]  # add same x position data again (stitch top to bottom)
            pos_y += [y_pos]  # add y position data for top of ellipse
            pos_y += [-y_pos]  # add y position data for bottom of ellipse

        # return to starting position and draw leaf center line
        end_x = x_pos
        end_y = (y_pos - y_pos)/2
        for i in range(end_x + x, -end_x + x -20, -10):
            x_pos = i
            y_pos = end_y
            pos_x += [round(x_pos)]
            pos_y += [round(y_pos)]

        # rotate position data by multiplying by a rotation matrix
        rot_x = []
        rot_y = []
        for i in range(0, len(pos_x)-1):
            x1 = pos_x[i] * round(math.cos(theta)) - pos_y[i] * round(math.sin(theta))
            y1 = pos_x[i] * round(math.sin(theta)) + pos_y[i] * round(math.cos(theta))
            rot_x += [x1]
            rot_y += [y1]

        # translate position data to displacement data
        for i in range(1, int(len(rot_x))):
            x_disp = rot_x[i] - rot_x[i - 1]
            y_disp = rot_y[i] - rot_y[i - 1]
            y_disp = int(y_disp)
            if y_disp < 0:
                y_disp = 256 + y_disp
            x_disp = int(x_disp)
            if x_disp < 0:
                x_disp = 256 + x_disp
            leaves += [x_disp, y_disp]

        return leaves

    # define width, height and angle of leaf 1
    leaf1 = leaf(0, 0, 60, 20, 0)
    stitches += leaf1

    # Change thread
    stitches += [128, 1]  # 128 = escape_character -> 1 = Change to next thread in list

    for i in range (0, 60, 30):
        # define width, height and angle of leaf 2
        new_leaf = leaf(0, 0, 60, 20, i)
        stitches += new_leaf

    stitches += [128, 16]  # 128 = escape_character , 16=last_stitch
    return stitches


def test():
    stitches = [128, 2]  # 128 = escape_character , 2=Move
    stitches += [0, 0]  # followed by 8 bit displacement X,Y
    # Note: Displacements are in 0.1mm units. If number is greater than 128, then it represents
    # a negative distance calculated by subtracting the number from 256 and multiplying by 0.1mm

    stitches += [30, 20]
    stitches += [20, 30]
    stitches += [10, 20]
    stitches += [20, 10]

    stitches += [128, 16]  # 128 = escape_character , 16=last_stitch
    return stitches

def stem():
    stitches = [128, 2]  # 128 = escape_character , 2=Move
    stitches += [0, 0]  # followed by 8 bit displacement X,Y
    # Note: Displacements are in 0.1mm units. If number is greater than 128, then it represents
    # a negative distance calculated by subtracting the number from 256 and multiplying by 0.1mm

    def leaf(x, y, a, b, theta):
        leaves = [] # create array for displacement data that will be added to stitches array
        pos_x = []  # create array for x position data
        pos_y = []  # create array for y position data
        x_pos = x # starting position
        y_pos = y # starting position

        # fill in leaf
        for i in range(-a, a, 2):
            y_pos = y + int(math.sqrt((-b ** 2 / a ** 2) * i ** 2 + b ** 2))
            x_pos = x + i
            pos_x += [x_pos]  # add x position data
            pos_x += [x_pos]  # add same x position data again (stitch top to bottom)
            pos_y += [y_pos]  # add y position data for top of ellipse
            pos_y += [-y_pos]  # add y position data for bottom of ellipse

        # return to starting position and draw leaf center line
        end_x = x_pos
        end_y = (y_pos - y_pos)/2
        for i in range(end_x + x, -end_x + x -20, -10):
            x_pos = i
            y_pos = end_y
            pos_x += [round(x_pos)]
            pos_y += [round(y_pos)]

        # rotate position data by multiplying by a rotation matrix
        rot_x = []
        rot_y = []
        for i in range(0, len(pos_x)-1):
            x1 = pos_x[i] * round(math.cos(theta)) - pos_y[i] * round(math.sin(theta))
            y1 = pos_x[i] * round(math.sin(theta)) + pos_y[i] * round(math.cos(theta))
            rot_x += [x1]
            rot_y += [y1]

        # translate position data to displacement data
        for i in range(1, int(len(rot_x))):
            x_disp = rot_x[i] - rot_x[i - 1]
            y_disp = rot_y[i] - rot_y[i - 1]
            y_disp = int(y_disp)
            if y_disp < 0:
                y_disp = 256 + y_disp
            x_disp = int(x_disp)
            if x_disp < 0:
                x_disp = 256 + x_disp
            leaves += [x_disp, y_disp]

        return leaves

    pos_x = []
    pos_y = []
    x = 0
    y = 0
    length = 100
    stem_theta = 10
    branch_theta = 30
    # define stem length that reduces each iteration
    for i in range (length, 0, -10):
        # main stem
        start_x = x
        start_y = y
        for j in range (0, i+1, 10):
            x = start_x + j * math.cos(math.radians(stem_theta))
            y = start_y + j * math.sin(math.radians(stem_theta))
            pos_x += [x]
            pos_y += [y]
        # left branch
        start_x = x
        start_y = y
        for j in range (0, i+1, 10):
            x = start_x + j * math.cos(math.radians(stem_theta + branch_theta))
            y = start_y + j * math.sin(math.radians(stem_theta + branch_theta))
            pos_x += [x]
            pos_y += [y]
        # left leaf
        leaf_here = leaf(round(x), round(y), 60, 20, stem_theta + branch_theta)
        stitches += leaf_here
        # back along left branch to center
        for j in range (i+1, 0, -10):
            x = start_x + j * math.cos(math.radians(stem_theta + branch_theta))
            y = start_y + j * math.sin(math.radians(stem_theta + branch_theta))
            pos_x += [x]
            pos_y += [y]
        #main stem continued
        for j in range (0, i+1, 10):
            x = start_x + j * math.cos(math.radians(stem_theta))
            y = start_y + j * math.sin(math.radians(stem_theta))
            pos_x += [x]
            pos_y += [y]
        # right branch
        start_x = x
        start_y = y
        for j in range (0, i+1, 10):
            x = start_x + j * math.cos(math.radians(stem_theta - branch_theta))
            y = start_y + j * math.sin(math.radians(stem_theta - branch_theta))
            pos_x += [x]
            pos_y += [y]
        # back along left branch to center
        for j in range (i+1, 0, -10):
            x = start_x + j * math.cos(math.radians(stem_theta - branch_theta))
            y = start_y + j * math.sin(math.radians(stem_theta - branch_theta))
            pos_x += [x]
            pos_y += [y]

    # convert position to displacement
    for i in range(1, len(pos_x)):
        x_disp = pos_x[i] - pos_x[i - 1]
        y_disp = pos_y[i] - pos_y[i - 1]
        y_disp = round(y_disp)
        if y_disp < 0:
            y_disp = 256 + y_disp
        x_disp = round(x_disp)
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
                2, 0, 0, 0,  # Thread count nr. (nr of thread changes)
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
    stitchseq = stem()
    header = getJefHeader(len(stitchseq) // 2)
    data = bytes(header) + bytes(stitchseq)
    with open("stem.jef", "wb") as f:
        f.write(data)


if __name__ == '__main__':
    main()
