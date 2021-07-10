# Import statements
import math
import pygame
import json
import os
import time


# Constants and Global variables

PI = math.pi
# Change true to enable arduino for app
app_version = False
# Change true to enable arduino for controller
controller_version = False

if app_version or controller_version:
    import serial


def servo(servoValues):
    if controller_version:
        arduinoData.write(str.encode(servoValues))

def background():
    screen.fill((1,31,75))

def display_stat(stat, pos_x, pos_y):
    font = pygame.font.Font('freesansbold.ttf', 15)
    display = font.render(str(stat), True,(90,188,216))
    return screen.blit(display, ((pos_x), (pos_y)))

def format_time(to_format):
    return str(int(to_format // 60)) + "." + str(round(to_format % 60, 2))

def print_trajectory(emptyAlpha):
    font = pygame.font.Font('freesansbold.ttf', 20)
    for i in emptyAlpha:
        display = font.render(".", True, (255, 255, 0))
        screen.blit(display, (i[0] + 245, i[1] + 430))


def recieve_input(stringOutput):
    plane_lat = ""
    plane_lon = ""
    for x in range(len(stringOutput)):
        if stringOutput[x] == ',' or stringOutput[x] == ' ':
            for y in range(x + 1, len(stringOutput)):
                plane_lon += (stringOutput[y])
            break
        plane_lat += stringOutput[x]
    return float(plane_lat), float(plane_lon)


def meter(fill_till, pos_x, pos_y, surface):
    a = 120
    b = 25
    pygame.draw.rect(surface, 'blue', (pos_x, pos_y, a, b))
    pygame.draw.rect(surface, 'green', (pos_x + 5, pos_y + 5, a - 10, b - 10))
    pygame.draw.rect(surface, (255, 255 - fill_till * 2, 0), (pos_x + 5, pos_y + 5, fill_till, 15))


def plane_rotation(bearing_angle, rotation):
    if bearing_angle < 0:
        bearing_angle += 360.0
    bearing_angle = int(bearing_angle) % 360
    bearing_angle //= 15
    return rotation[rotate_180 - bearing_angle]


def calcDist(latit1, longit1, lat2, lon2):
    # This portion converts the current and destination GPS coords from decDegrees to Radians String
    lonR1 = longit1 * (PI / 180)
    lonR2 = lon2 * (PI / 180)
    latR1 = latit1 * (PI / 180)
    latR2 = lat2 * (PI / 180)

    # the differences lattitude and longitudes in Radians
    dlon = lonR2 - lonR1
    dlat = latR2 - latR1

    # Haversine Formula to calculate the distance between two latitude and longitude vales
    a = ((math.sin(dlat / 2)) ** 2) + math.cos(latR1) * math.cos(latR2) * ((math.sin(dlon / 2)) ** 2)
    e = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * e

    m = d * 1000  # convert to meters

    # Haversine Formula to find the bearing angle between the destination and current position
    x = math.cos(latR2) * math.sin(lonR2 - lonR1)  # calculate x
    y = math.cos(latR1) * math.sin(latR2) - math.sin(latR1) * math.cos(latR2) * math.cos(lonR2 - lonR1)  # calculate y
    brRad = math.atan2(x, y)  # return atan2 result for bearing. Result at this point is in Radians
    reqBear = toDegrees * brRad  # convert to degrees

    return x * scale_graph, y * scale_graph, round(reqBear, 2), round(m, 2)


pygame.init()

# images and caption
screen = pygame.display.set_mode((1150, 575))

# These file paths will vary depeneding on where the images are downloaded

pygame.display.set_caption("Plane Visualizer")
icon = pygame.image.load(
    r'C:\Users\hamza\OneDrive\Documents\RC-Autopilot-Plane-main\RC-Autopilot-Plane-main\PLANEAPP\globe.png')
pygame.display.set_icon(icon)

logo = pygame.image.load(
    r'C:\Users\hamza\OneDrive\Documents\RC-Autopilot-Plane-main\RC-Autopilot-Plane-main\PLANEAPP\logo.png')
logo = pygame.transform.scale(logo, (140, 120))

b2 = pygame.image.load(
    r'C:\Users\hamza\OneDrive\Documents\RC-Autopilot-Plane-main\RC-Autopilot-Plane-main\PLANEAPP\b2.png')
b2 = pygame.transform.scale(b2, (600, 600))

plane_art = pygame.image.load(
    r'C:\Users\hamza\OneDrive\Documents\RC-Autopilot-Plane-main\RC-Autopilot-Plane-main\PLANEAPP\plane.png')
plane_art = pygame.transform.scale(plane_art, (30, 30))

# trajectory_list
trajectory = []

rotation = []
rotate_180 = 12
for x in range(24):
    rotation.append(pygame.transform.rotate(plane_art, 15 * x))

R = 6371.00
toDegrees = 57.295779
scale_graph = 6333065.367

# scale to plot x and y positions
scale = .45

# centering
center_x = 233
center_y = 220

t0 = time.time()  # starts time
checker = 1  # time checker

velocity = 0.0
altitude = 0.0
time_from_destination = 0.0
time_elapsed = 0.0
distance_traveled = 0.0
battery_left = 1.0

# array (this does not have a function right now)
graph_length = 15
beta = []
alpha = []
for t in range(graph_length):
    beta.append('.')
for x in range(len(beta)):
    alpha.append(beta)

# before reading current location, get user input of destination
if app_version:
    lat1 = float(input("enter lat value"))
    lon1 = float(input("enter lon value"))

    # connecting serial to python
    ser = serial.Serial('COM3', baudrate=9600, timeout=1)

if controller_version:
    arduinoData = serial.Serial('com3', 9600)

# read serial output and store in variable

if app_version:
    arduinoData = ser.readline()
    string = arduinoData.decode()
    string = string.replace('\r', '')
    string = string.rstrip()

if app_version:
    while string == "":
        # find gps signal before runnning app
        print("waiting for gps signal")
        arduinoData = ser.readline()
        string = arduinoData.decode()
        string = string.replace('\r', '')
        string = string.rstrip()

# Initialising Controller values
HLA = "00"
VLA = "00"
HRA = "00"
RT = "00"

# game_loop
runner = True
while runner:
    if app_version:
        values = recieve_input(string)

        entry = calcDist(lat1, lon1, values[0], values[1])  # putx,y values and dest x y values

        x_pos = entry[0]
        y_pos = entry[1]
        bearing = entry[2]
        dis_remain = entry[3]

    t1 = time.time()
    time_elapsed = t1 - t0
    background()
    c1 = time_elapsed % 50
    # pygame.draw.circle(screen, (c1*4, 60+(c1*3), 250-(c1*5)), (630,410), 100)



    

    pygame.draw.circle(screen, 'green', (260, 267), 255)
    # pygame.draw.circle(screen, 'blue', (630,410), 100)
    pygame.draw.circle(screen, 'blue', (260, 267), 250)

    rect = (10, 17, 600, 500)
    screen.blit(b2, (0, 0))

    pygame.draw.rect(screen, (179,205,224), (580,0,20,600))

    pygame.draw.line(screen, 'red', (252, 259), (268, 275), 5)
    pygame.draw.line(screen, 'red', (252, 275), (268, 259), 5)

    pygame.draw.line(screen, 'black', (10, 267), (510, 267), 3)
    pygame.draw.line(screen, 'black', (260, 17), (260, 517), 3)

    sinx = int(math.sin(time_elapsed) * 250)
    cosx = int(math.cos(time_elapsed) * 250)

    pygame.draw.line(screen, 'green', (260, 267), (260 + cosx, 267 + sinx), 1)

    for x in range(11):
        pygame.draw.line(screen, 'black', (10 + (50 * x), 260), (10 + (50 * x), 274), 2)
        pygame.draw.line(screen, 'black', (253, 17 + (50 * x)), (267, 17 + (50 * x)), 2)

    pygame.draw.line(screen, 'black', (10, 267), (510, 267), 2)

    if app_version:
        plane_rot = plane_rotation(bearing, rotation)
        screen.blit(plane_rot, (center_x + (x_pos * scale), (center_y - (y_pos * scale))))

    # screen.blit(logo, (560,357))

    # add pos_x to 233 and pos_y to 430 for changes
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runner = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                checker = 0
                t0 = time.time()
                trajectory = []
                temp = recieve_input(string)
                original_x = temp[0]
                original_y = temp[1]

    # Changes_in_Stats

    time_elapsed = format_time(round(time_elapsed, 1))

    a = 625
    b = 785

    a1 = 20
    b1 = 30

    temp_var = a1 + b1

    display_stat("Time Elpased:", a, temp_var * 1)
    display_stat(time_elapsed, b, temp_var * 1)

    display_stat("Average Velocity:", a, temp_var * 2)
    display_stat(velocity, b, temp_var * 2)

    display_stat("Distance Traveled:", a, temp_var * 3)
    display_stat(distance_traveled, b, temp_var * 3)

    display_stat("Altitude:", a, temp_var * 4)
    display_stat(altitude, b, temp_var * 4)

    if app_version:
        display_stat("Distance Remaining:", a, 150)
        display_stat(dis_remain, b, 150)

        display_stat("Bearing Angle:", a, 230)
        display_stat(bearing, b, 230)

    # prints trajectory. Stores coordinates for trajectory on line 135
    print_trajectory(trajectory)

    # change in position
    # temp = recieve_input(string)  # last values of long and lat in the file
    # temp_list = position(temp[0], temp[1])

    # if int(t1 - t0) == checker:
    #     checker += 3
    #     temp = [int(x_pos), int(y_pos)]
    #     trajectory.append(temp)

    # Initializing Controller
    joysticks = []
    for i in range(pygame.joystick.get_count()):
        joysticks.append(pygame.joystick.Joystick(i))
    for joystick in joysticks:
        joystick.init()

    # Reading in PS4 buttons
    with open(os.path.join(r'C:\Users\hamza\OneDrive\Documents\RC-Autopilot-Plane-main\RC-Autopilot-Plane-main\Arduino_Code\ps4keys.JSON'), "r+") as file:
        button_keys = json.load(file)

    # 0: Left-analog Horz 1: Left-analog Vertical 2: Right-analog Horz
    # 3: Right-analog Vertical 4: Left Trigger 5: Right Trigger
    analog_keys = {0: 0, 1: 0, 2: 0, 3: 0, 4: -1, 5: 1}

    # Player
    playerImg = pygame.image.load(r'C:\Users\hamza\OneDrive\Documents\RC-Autopilot-Plane-main\RC-Autopilot-Plane-main\PLANEAPP\globe.png')
    playerX = 370
    playerY = 480
    playerX_change = 0
    playerY_change = 0



    # Gaining PS4 Controller access
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # PS4 Buttons
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == button_keys['x']:
                print("\nx")

        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == button_keys['circle']:
                print("\ncircle")

        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == button_keys['triangle']:
                print("\ntriangle")
        

        if event.type == pygame.JOYBUTTONUP:
            if event.button == button_keys['triangle']:
                pass
                # servo_off()
                # print("two")

        if event.type == pygame.JOYAXISMOTION:
            analog_keys[event.axis] = event.value

            # Horizontal Left Analog - Ailerons
            if (abs(analog_keys[0])) > 0:
                if analog_keys[0] < -.1:
                    HLA = int(round(analog_keys[0], 2) * -10)
                    if HLA > 9:
                        HLA = 9
                    HLA = "0" + str(HLA)
                if analog_keys[0] > 0.1:
                    HLA = int(round(analog_keys[0], 2) * 10) + 10
                    if HLA > 19:
                        HLA = 19
                    HLA = str(HLA)

            # Vertical Left Analog - Elevator
            if (abs(analog_keys[1])) > 0.1:
                if analog_keys[1] < -.1:
                    VLA = int(round(analog_keys[1], 2) * -10)
                    if VLA > 9:
                        VLA = 9
                    VLA = "0" + str(VLA)
                if analog_keys[1] > 0.1:
                    VLA = int(round(analog_keys[1], 2) * 10) + 10
                    if VLA > 19:
                        VLA = 19
                    VLA = str(VLA)

            # Horz Right Analog - Rutter`
            if (abs(analog_keys[2])) > 0.1:
                if analog_keys[2] < -.1:
                    HRA = int(round(analog_keys[2], 2) * -10)
                    if HRA > 9:
                        HRA = 9
                    HRA = "0" + str(HRA)
                if analog_keys[2] > 0.1:
                    HRA = int(round(analog_keys[2], 2) * 10) + 10
                    if HRA > 19:
                        HRA = 19
                    HRA = str(HRA)

            # Right Trigger - DC Motor

            # analog_keys[4] is left trigger for Windows and right trigger for the Mac
            if -1 <= analog_keys[4] < 0:
                RT = int(round(analog_keys[4], 2) * -10)
                if RT > 9:
                    RT = 9
                RT = "0" + str(RT)
            if 0 < analog_keys[4] <= 1:
                RT = int(round(analog_keys[4], 2) * 10) + 10
                if RT > 19:
                    RT = 19
                RT = str(RT)

                # Final output
            value = HLA + VLA + HRA + RT
            print(value)
            servo(value)

    #if (int(RT) <= 9):
        #meter((9 - int(RT)) * 6, 570, 300, b2)
    #else:
        #meter((int(RT)) * 6, 570, 300, b2)

    pygame.display.update()