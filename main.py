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

def manyEllipses():
    stitches = [128, 2]  # 128 = escape_character , 2=Move
    stitches += [0, 0]  # followed by 8 bit displacement X,Y
    stitches += [206, 206]
    # Note: Displacements are in 0.1mm units. If number is greater than 128, then it represents
    # a negative distance calculated by subtracting the number from 256 and multiplying by 0.1mm

    #define width, height and angle of ellipse 1
    a = 60
    b = 20
    theta = 10

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
    for i in range(1, int(len(rot_x))):
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

    # define width, height and angle of ellipse 2
    a = 70
    b = 30
    theta = 40

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
    for i in range(1, int(len(rot_x))):
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
    stitchseq = manyEllipses()
    header = getJefHeader(len(stitchseq) // 2)
    data = bytes(header) + bytes(stitchseq)
    with open("manyellipses.jef", "wb") as f:
        f.write(data)


if __name__ == '__main__':
    main()
