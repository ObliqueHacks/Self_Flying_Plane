import serial

# Arduino class not working for now


class Arduino:

    # Setup serial
    def __init__(self):
        self.controller_version = False
        self.app_version = False
        self.contApp = None
        self.serApp = None

        if self.controller_version:
            self.contApp = serial.Serial('com3', 9600)

    # Send Values
    def servo(self, value):
        if self.controller_version:
            self.contApp.write(str.encode(value))

    def gps(self):
        # before reading current location, get user input of destination
        if self.app_version:
            # self.lat1 = input("Enter lat")
            # self.lon1 = input("Enter log")
            self.lat1 = 32
            self.lon1 = 43

        # read serial output and store in variable

        if self.app_version:
            arduinoData = self.serApp.readline()
            self.string = arduinoData.decode()
            self.string = self.string.replace('\r', '')
            self.string = self.string.rstrip()

        if self.app_version:
            while self.string == "":
                # find gps signal before runnning app
                print("waiting for gps signal")
                arduinoData = self.serApp.readline()
                self.string = arduinoData.decode()
                self.string = self.string.replace('\r', '')
                self.string = self.string.rstrip()
