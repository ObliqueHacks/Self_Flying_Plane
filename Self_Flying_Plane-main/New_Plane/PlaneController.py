import pygame
import os
import json
# from App import A


class Controller:
    # Initializing

    def __init__(self):

        self.joysticks = []
        self.button_keys = {}
        self.analog_keys = {}
        self.HLA = ""
        self.VLA = ""
        self.HRA = ""
        self.RT = ""
        self.value = ""

    # Game Loop
    def startUp(self):

        pygame.init()

        # Initialize Controller
        for i in range(pygame.joystick.get_count()):
            self.joysticks.append(pygame.joystick.Joystick(i))
        for joystick in self.joysticks:
            joystick.init()

        # Reading in PS4 buttons
        with open(os.path.join("ps4keys.json"), "r+") as file:
            self.button_keys = json.load(file)

        # 0: Left-analog Horz 1: Left-analog Vertical 2: Right-analog Horz
        # 3: Right-analog Vertical 4: Left Trigger 5: Right Trigger
        self.analog_keys = {0: 0, 1: 0, 2: 0, 3: 0, 4: -1, 5: -1}

        running = True
        check = False
        while running:

            pygame.time.delay(100)
            # RGB - Red, Green, Blue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == self.button_keys['triangle']:
                        pass
                        check = True

                    if event.button == self.button_keys['square']:
                        pass

                    if event.button == self.button_keys['circle']:
                        pass
                        # servo_off()
                        # print("two")
                    if event.button == self.button_keys['x']:
                        check = False
                    if event.button == self.button_keys['L1']:
                        running = False
                if check:
                    pass
                else:
                    if event.type == pygame.JOYAXISMOTION:

                        self.HLA = "00"
                        self.VLA = "00"
                        self.HRA = "00"
                        self.RT = "09"

                        self.analog_keys[event.axis] = event.value

                        # Horizontal Left Analog - Ailerons
                        if (abs(self.analog_keys[0])) > 0:
                            if self.analog_keys[0] < -.1:
                                self.HLA = int(round(self.analog_keys[0], 2) * -10)
                                if self.HLA > 9:
                                    self.HLA = 9
                                self.HLA = "0" + str(self.HLA)
                            if self.analog_keys[0] > 0.1:
                                self.HLA = int(round(self.analog_keys[0], 2) * 10) + 10
                                if self.HLA > 19:
                                    self.HLA = 19
                                self.HLA = str(self.HLA)

                        # Vertical Left Analog - Elevator
                        if (abs(self.analog_keys[1])) > 0.1:
                            if self.analog_keys[1] < -.1:
                                self.VLA = int(round(self.analog_keys[1], 2) * -10)
                                if self.VLA > 9:
                                    self.VLA = 9
                                self.VLA = "0" + str(self.VLA)
                            if self.analog_keys[1] > 0.1:
                                self.VLA = int(round(self.analog_keys[1], 2) * 10) + 10
                                if self.VLA > 19:
                                    self.VLA = 19
                                self.VLA = str(self.VLA)
                        # Horz Right Analog - Rutter
                        if (abs(self.analog_keys[2])) > 0.1:
                            if self.analog_keys[2] < -.1:
                                self.HRA = int(round(self.analog_keys[2], 2) * -10)
                                if self.HRA > 9:
                                    self.HRA = 9
                                self.HRA = "0" + str(self.HRA)
                            if self.analog_keys[2] > 0.1:
                                self.HRA = int(round(self.analog_keys[2], 2) * 10) + 10
                                if self.HRA > 19:
                                    self.HRA = 19
                                self.HRA = str(self.HRA)
                        # Right Trigger - DC Motor
                        if -1 <= self.analog_keys[4] < 0:
                            self.RT = int(round(self.analog_keys[4], 2) * -10)
                            if self.RT > 9:
                                self.RT = 9
                            self.RT = "0" + str(self.RT)

                        if 0 < self.analog_keys[4] <= 1:
                            self.RT = int(round(self.analog_keys[4], 2) * 10) + 10
                            if self.RT > 19:
                                self.RT = 19
                            self.RT = str(self.RT)

                        self.value = self.HLA + self.VLA + self.HRA + self.RT
                        print(self.value)
                        A.servo(self.value)




