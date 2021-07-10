import math
import time
PI = math.pi
import pygame
work_version = False



if (work_version == True):
    import serial

def int_finder(alpha, pos_x, pos_y):
    font = pygame.font.Font('freesansbold.ttf', 20)
    display = font.render(str(alpha[pos_x][pos_y]), True, (31, 28, 28))
    return screen.blit(display, ((pos_x * 30) + 35, (pos_y * 30) + 10))

def background():
    screen.fill((5, 14, 57))

def display_stat(stat, pos_x, pos_y):
    font = pygame.font.Font('freesansbold.ttf', 15)
    display = font.render(str(stat), True, 'white')
    return screen.blit(display, ((pos_x), (pos_y)))

def format_time(to_format):
    return str(int(to_format // 60)) + "." + str(round(to_format % 60, 2))

def print_trajectory(alpha):
    font = pygame.font.Font('freesansbold.ttf', 20)
    for i in alpha:
        display = font.render(".", True, (255, 255, 0))
        screen.blit(display, (i[0] + 245, i[1] + 430))

def recieve_input(string):
    plane_lat = ""
    plane_lon = ""
    for x in range(len(string)):
        if string[x] == ',' or string[x] == ' ':
            for y in range(x + 1, len(string)):
                plane_lon += (string[y])
            break
        plane_lat += string[x]
    return float(plane_lat), float(plane_lon)

def meter (fill_till, pos_x, pos_y, surface):
  a = 120
  b = 25
  pygame.draw.rect(surface, 'blue', (pos_x, pos_y, a,b))
  pygame.draw.rect(surface, 'green', (pos_x+5, pos_y+5, a-10, b-10))
  pygame.draw.rect(surface, (255,255-fill_till*2,0), (pos_x+5, pos_y+5, fill_till, 15))

def plane_rotation(bearing_angle, rotation):
  if bearing_angle < 0:
    bearing_angle+=360.0
  bearing_angle = int(bearing_angle)%360
  bearing_angle//=15
  return rotation[rotate_180 - bearing_angle]

def calcDist(lat1, lon1, lat2, lon2):

    # This portion converts the current and destination GPS coords from decDegrees to Radians String
    lonR1 = lon1 * (PI / 180)
    lonR2 = lon2 * (PI / 180)
    latR1 = lat1 * (PI / 180)
    latR2 = lat2 * (PI / 180)

    # the differences lattitude and longitudes in Radians
    dlon = lonR2 - lonR1
    dlat = latR2 - latR1

    # Haversine Formula to calculate the distance between two latitude and longitude vales
    a = ((math.sin(dlat / 2))**2) + math.cos(latR1) * math.cos(latR2) * ((math.sin(dlon / 2))**2)
    e = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * e

    m = d * 1000 # convert to meters

    # Haversine Formula to find the bearing angle between the destination and current position
    x = math.cos(latR2) * math.sin(lonR2 - lonR1) #calculate x
    y = math.cos(latR1) * math.sin(latR2) - math.sin(latR1) * math.cos(latR2) * math.cos(lonR2 - lonR1) # calculate y
    brRad = math.atan2(x, y) # return atan2 result for bearing. Result at this point is in Radians
    reqBear = toDegrees * brRad # convert to degrees

    return x * scale_graph, y * scale_graph, round(reqBear,2), round(m,2)

pygame.init()

# images and caption
screen = pygame.display.set_mode((760, 575))

pygame.display.set_caption("Plane Visualizer")
icon = pygame.image.load(r'C:\Users\hamza\OneDrive\Documents\RC-Autopilot-Plane-main\RC-Autopilot-Plane-main\PLANEAPP\globe.png')
pygame.display.set_icon(icon)

logo = pygame.image.load(r'C:\Users\hamza\OneDrive\Documents\RC-Autopilot-Plane-main\RC-Autopilot-Plane-main\PLANEAPP\logo.png')
logo = pygame.transform.scale(logo, (140,120))

b2 = pygame.image.load(r'C:\Users\hamza\OneDrive\Documents\RC-Autopilot-Plane-main\RC-Autopilot-Plane-main\PLANEAPP\b2.png')
b2 = pygame.transform.scale(b2, (760, 600))

plane_art = pygame.image.load(r'C:\Users\hamza\OneDrive\Documents\RC-Autopilot-Plane-main\RC-Autopilot-Plane-main\PLANEAPP\plane.png')
plane_art = pygame.transform.scale(plane_art, (30, 30))

# trajectory_list
trajectory = []

rotation = []
rotate_180 = 12
for x in range (24):
  rotation.append(pygame.transform.rotate(plane_art, 15*x))

R = 6371.00
toDegrees = 57.295779
scale_graph = 6333065.367

#scale to plot x and y positions
scale= .45

#centering
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

#before reading current location, get user input of destination
if work_version == True:
    lat1 = float(input("enter lat value"))
    lon1 = float(input("enter lon value"))

#connecting serial to python
    ser = serial.Serial('COM3', baudrate=9600, timeout=1)

# read serial output and store in variable

if (work_version == True):
    arduinoData = ser.readline()
    string = arduinoData.decode()
    string = string.replace('\r', '')
    string = string.rstrip()



if work_version == True:
    while string == "":

    # find gps signal before runnning app
        print("waiting for gps signal")
        arduinoData = ser.readline()
        string = arduinoData.decode()
        string = string.replace('\r', '')
        string = string.rstrip()

#game_loop
runner = True
while runner:
    if (work_version == True):
        values = recieve_input(string)

        entry = calcDist(lat1, lon1, values[0], values[1])#putx,y values and dest x y values

        x_pos = entry[0]
        y_pos = entry[1]
        bearing = entry[2]
        dis_remain = entry[3]

    t1 = time.time()
    time_elapsed = t1 - t0
    background()
    c1 = time_elapsed % 50
    # pygame.draw.circle(screen, (c1*4, 60+(c1*3), 250-(c1*5)), (630,410), 100)

    meter((int(velocity)), 570, 500, b2)

    pygame.draw.circle(screen, 'green', (260, 267), 255)
    # pygame.draw.circle(screen, 'blue', (630,410), 100)
    pygame.draw.circle(screen, 'blue', (260, 267), 250)

    rect = (10, 17, 600, 500)
    screen.blit(b2, (0, 0))

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

    if (work_version == True):
        plane_rot = plane_rotation(bearing, rotation)
        screen.blit(plane_rot, (center_x+(x_pos*scale), (center_y-(y_pos*scale))))

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

    a = 525
    b = 685

    a1 = 30
    b1 = 40

    display_stat("Time Elpased:", a, a1 + b1*0)
    display_stat(time_elapsed, b, a1 + b1*0)

    display_stat("Average Velocity:", a, 70)
    display_stat(velocity, b, 70)

    display_stat("Distance Traveled:", a, 110)
    display_stat(distance_traveled, b, 110)
    
    display_stat("Altitude:", a, 190)
    display_stat(altitude, b, 190)


    if work_version == True: 
        display_stat("Distance Remaining:", a, 150)
        display_stat(dis_remain, b, 150)

        display_stat("Bearing Angle:", a, 230)
        display_stat(bearing, b, 230)

    # prints trajectory. Stores coordinates for trajectory on line 135
    print_trajectory(trajectory)

    # change in position
    #temp = recieve_input(string)  # last values of long and lat in the file
    # temp_list = position(temp[0], temp[1])

    
    # if int(t1 - t0) == checker:
    #     checker += 3
    #     temp = [int(x_pos), int(y_pos)]
    #     trajectory.append(temp)

    pygame.display.update()
