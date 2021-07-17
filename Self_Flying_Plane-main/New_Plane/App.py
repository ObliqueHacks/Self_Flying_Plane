# Import statements
import math
import pygame
import json
import os
import time
import serial
from stats import stat_list
from arduino import Arduino

# Constants and Global variables
PI = math.pi

ob = Arduino()


class app:

    def loop(self):

        def background():
            screen.fill((1, 31, 75))

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

        def calcDist(lat1, long1, lat2, lon2):
            # This portion converts the current and destination GPS coords from decDegrees to Radians String
            lonR1 = long1 * (PI / 180)
            lonR2 = lon2 * (PI / 180)
            latR1 = lat1 * (PI / 180)
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
            y = math.cos(latR1) * math.sin(latR2) - math.sin(latR1) * math.cos(latR2) * math.cos(
                lonR2 - lonR1)  # calculate y
            brRad = math.atan2(x, y)  # return atan2 result for bearing. Result at this point is in Radians
            reqBear = toDegrees * brRad  # convert to degrees

            return x * scale_graph, y * scale_graph, round(reqBear, 2), round(m, 2)

        pygame.init()

        # images and caption
        screen = pygame.display.set_mode((1150, 575))

        # These file paths will vary depeneding on where the images are downloaded

        pygame.display.set_caption("Plane Visualizer")
        icon = pygame.image.load('images/globe.png')
        pygame.display.set_icon(icon)

        logo = pygame.image.load('images/logo.png')
        logo = pygame.transform.scale(logo, (140, 120))

        b2 = pygame.image.load('images/b2.png')
        b2 = pygame.transform.scale(b2, (600, 600))

        plane_art = pygame.image.load('images/plane.png')
        plane_art = pygame.transform.scale(plane_art, (30, 30))

        aurora = pygame.image.load('images/aurora.png')
        aurora = pygame.transform.scale(aurora, (100, 75))

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

        ob.gps()

        # initialize stat list
        stat_tracker = stat_list(screen, 625, 785, 20, 30, 70)
        stat_tracker.add_stat("Time Elapsed")
        stat_tracker.add_stat("Average Velocity")
        stat_tracker.add_stat("Distance Tracker")
        stat_tracker.add_stat("Time Remaining")

        # radar distance
        radar_distance = 0

        # game_loop
        runner = True
        while runner:
            if ob.app_version:
                values = recieve_input(string)

                entry = calcDist(ob.lat1, ob.lon1, values[0], values[1])  # putx,y values and dest x y values

                x_pos = entry[0]
                y_pos = entry[1]
                bearing = entry[2]
                dis_remain = entry[3]

            t1 = time.time()
            time_elapsed = t1 - t0
            background()
            c1 = time_elapsed % 50
            # pygame.draw.circle(screen, (c1*4, 60+(c1*3), 250-(c1*5)), (630,410), 100)

            radar_distance += 2
            pygame.draw.rect(screen, 'blue', (0, 0, 590, 600))
            pygame.draw.circle(screen, (13, 152, 186), (280, 280), int(radar_distance), 2)

            if radar_distance >= 275:
                radar_distance = 0

            pygame.draw.rect(screen, (179, 205, 224), (615, 25, 500, 60))
            pygame.draw.rect(screen, (90, 188, 216), (620, 30, 490, 50))

            rect = (10, 17, 600, 500)
            screen.blit(b2, (0, 0))
            screen.blit(aurora, (1000, 15))

            pygame.draw.rect(screen, (179, 205, 224), (590, 0, 10, 600))

            pygame.draw.line(screen, 'red', (270, 270), (290, 290), 5)
            pygame.draw.line(screen, 'red', (270, 290), (290, 270), 5)

            pygame.draw.line(screen, 'black', (0, 280), (590, 280), 3)
            pygame.draw.line(screen, 'black', (280, 0), (280, 600), 3)

            sinx = int(math.sin(time_elapsed) * 250)
            cosx = int(math.cos(time_elapsed) * 250)

            # rotating_green_ting
            # pygame.draw.line(screen, 'green', (280, 280), (280 + cosx, 280 + sinx), 1)

            # for x in range(11):
            #     pygame.draw.line(screen, 'black', (10 + (50 * x), 260), (10 + (50 * x), 274), 2)
            #     pygame.draw.line(screen, 'black', (253, 17 + (50 * x)), (267, 17 + (50 * x)), 2)

            # pygame.draw.line(screen, 'black', (10, 267), (510, 267), 2)

            if ob.app_version:
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
            stat_tracker.display_stats()
            stat_tracker.display_stat("BOREALIS TRACKER", 630, 40, 35, (1, 31, 75))

            # prints trajectory. Stores coordinates for trajectory on line 135

            # change in position
            # temp = recieve_input(string)  # last values of long and lat in the file
            # temp_list = position(temp[0], temp[1])

            # if int(t1 - t0) == checker:
            #     checker += 3
            #     temp = [int(x_pos), int(y_pos)]
            #     trajectory.append(temp)

            pygame.display.update()

