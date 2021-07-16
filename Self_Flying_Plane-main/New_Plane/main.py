from App import app
from PlaneController import Controller
from multiprocessing import Process
import serial

App = app()
Controller = Controller()


def main():
    a = Process(target=App.loop)
    b = Process(target=Controller.startUp)
    a.start()
    b.start()
    a.join()
    if not a.is_alive():
        b.terminate()


if __name__ == '__main__':
    main()
