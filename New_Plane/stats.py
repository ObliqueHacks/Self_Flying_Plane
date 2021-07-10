# a = 625
# b = 785
# a1 = 20
# b1 = 30
import pygame
class stat_list:
    def __init__(self, screen, a, b, a1, b1):
        self.info_list = {}
        self.a = a
        self.b = b
        self.a1 = a1
        self.b1 = b1
        self.temp_var = a1+b1
        self.screen = screen

    def display_stat(self, stat, pos_x, pos_y):
        font = pygame.font.Font('freesansbold.ttf', 15)
        display = font.render(str(stat), True,(90,188,216))
        return self.screen.blit(display, ((pos_x), (pos_y)))

    def add_stat(self, stat_name, stat_input = 0):
        self.info_list[stat_name] = stat_input

    def display_stats(self):
        count = 1
        for x in self.info_list:
            self.display_stat(x, self.a, self.temp_var * count)
            self.display_stat(self.info_list[x], self.b, self.temp_var * count)
            count+=1