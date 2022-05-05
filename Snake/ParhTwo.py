import numpy as np
import pygame
import sys
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

pygame.init()


class MAIN:
    def __init__(self):
        self.matrix_path = Matrix
        self.matrix_collar = np.copy(Matrix)
        self.cell_size = cell_size
        self.cell_number = cell_number
        self.start = []
        self.end = []
        self.print_set = 1

    def draw_node(self):
        for col in range(self.cell_number):
            for row in range(self.cell_number):
                node = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                if self.matrix_collar[row, col] == 0:
                    pygame.draw.rect(screen, Black, node)
                if self.matrix_collar[row, col] == 1:
                    pygame.draw.rect(screen, Blue, node)
                if 20 < self.matrix_collar[row, col] < 30:
                    pygame.draw.rect(screen, Yellow, node)
                    text_surf = gui_font.render(str(int(self.matrix_collar[row, col]-20)), True, Black)
                    text_rect = text_surf.get_rect(center=node.center)
                    screen.blit(text_surf, text_rect)
                if 30 < self.matrix_collar[row, col] < 40:
                    pygame.draw.rect(screen, Green, node)
                    text_surf = gui_font.render(str(int(self.matrix_collar[row, col]-30)), True, Black)
                    text_rect = text_surf.get_rect(center=node.center)
                    screen.blit(text_surf, text_rect)
                if self.matrix_collar[row, col] == 4:
                    pygame.draw.rect(screen, Pink, node)
                if self.matrix_collar[row, col] == 99:
                    pygame.draw.rect(screen, Purple, node)
        self.draw_grid()

    def draw_grid(self):
        for col in range(self.cell_number-1):
            points = [((col+1)*self.cell_size, 0), ((col+1)*self.cell_size, self.cell_size*self.cell_number)]
            pygame.draw.lines(screen, Black, False, points, 1)
        for row in range(cell_number-1):
            points = [(0, (row+1)*self.cell_size), (self.cell_size*self.cell_number, (row+1)*self.cell_size)]
            pygame.draw.lines(screen, Black, False, points, 1)

    def mark_active_cell(self, button):
        mouse_pos = pygame.mouse.get_pos()
        row = mouse_pos[1]//cell_size
        col = mouse_pos[0]//cell_size
        if button == 1:
            self.matrix_collar[row][col] = 20+self.print_set
            point = [row, col]
            self.start.append(point)
        if button == 3:
            self.matrix_collar[row][col] = 30+self.print_set
            point = [row, col]
            self.end.append(point)
        if button == 2:
            self.matrix_collar[row][col] = 0
            self.matrix_path[col][row] = 0

    def point_check(self):
        return self.start, self.end

    def path_print(self, path):
        for i in range(len(path)-2):
            y = path[i+1][0]
            x = path[i+1][1]
            self.matrix_collar[y][x] = 4

    def path_clear(self):
        for col in range(cell_number):
            for row in range(cell_number):
                if self.matrix_collar[row][col] == 4:
                    self.matrix_collar[row][col] = 1

    def set_up(self):
        self.print_set += 1

    def set_check(self):
        return self.print_set

    def collision_marker(self, node):
        y = node[0]
        x = node[1]
        self.matrix_collar[y][x] = 99
        self.matrix_path[x][y] = 0



class Button:
    def __init__(self, text1, width, height, position1, text2, position2):
        self.top_rect1 = pygame.Rect(position1, (width, height))
        self.top_color = '#475F77'
        self.text_surf1 = gui_font.render(text1, True, '#FFFFFF')
        self.text_rect1 = self.text_surf1.get_rect(center=self.top_rect1.center)
        self.pressed1 = False
        self.top_rect2 = pygame.Rect(position2, (width, height))
        self.text_surf2 = gui_font.render(text2, True, '#FFFFFF')
        self.text_rect2 = self.text_surf2.get_rect(center=self.top_rect2.center)
        self.pressed2 = False

    def draw(self):
        pygame.draw.rect(screen, self.top_color, self.top_rect1, border_radius=3)
        screen.blit(self.text_surf1, self.text_rect1)
        pygame.draw.rect(screen, self.top_color, self.top_rect2, border_radius=3)
        screen.blit(self.text_surf2, self.text_rect2)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect1.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed1 = True
            elif self.pressed1:
                main_game.path_clear()
                start, end = main_game.point_check()
                pathfinder = Pathfinder(Matrix)
                pathfinder.create_path(start, end)
                self.pressed1 = False
        if self.top_rect2.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed2 = True
            elif self.pressed2:
                main_game.set_up()
                self.pressed2 = False


class Pathfinder:
    def __init__(self, matrix):
        self.matrix = matrix
        self.grid = Grid(matrix=matrix)
        self.path_list = []

    def empty_path(self):
        self.path_list = []

    def create_path(self, start_point, end_point):
        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        for i in range(main_game.set_check()):
            if i == 0:
                start = self.grid.node(start_point[i][0], start_point[i][1])
                end = self.grid.node(end_point[i][0], end_point[i][1])
                path, _ = finder.find_path(start, end, self.grid)
                self.path_list.append(path)
                self.grid.cleanup()
                main_game.path_print(self.path_list[i])
            if i > 0:
                check = 0
                while check == 0:
                    start = self.grid.node(start_point[i][0], start_point[i][1])
                    end = self.grid.node(end_point[i][0], end_point[i][1])
                    path, _ = finder.find_path(start, end, self.grid)
                    self.path_list.append(path)
                    self.grid.cleanup()
                    main_game.path_print(self.path_list[i])
                    check_list = list([])
                    for j in range(len(self.path_list)):
                        check_list.append(len(self.path_list[j]))
                    check_list.sort()
                    for j in range(check_list[0]):
                        if self.path_list[0][j] == self.path_list[1][j]:
                            main_game.collision_marker(self.path_list[0][j])
                    check = 1


Blue = (102, 102, 255)
Pink = (255, 102, 102)
Yellow = (255, 255, 000)
Green = (102, 255, 102)
White = (200, 200, 200)
Purple = (255, 102, 255)
Black = (0, 0, 0)

cell_size = 20     # min 3 max 158
cell_number = 790 // cell_size
Matrix = np.ones((cell_number, cell_number))
screen = pygame.display.set_mode((cell_number*cell_size+500, cell_number*cell_size))
background = pygame.Rect(0, 0, cell_number*cell_size+500, cell_number*cell_size)
pygame.draw.rect(screen, White, background)
clock = pygame.time.Clock()
gui_font = pygame.font.Font(None, 30)

button1 = Button('Start', 200, 40, (cell_number*cell_size + 150, 100), 'Set Up', (cell_number*cell_size + 150, 300))
main_game = MAIN()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if pos[0] <= int(cell_number*cell_size):
                main_game.mark_active_cell(event.button)

    main_game.draw_node()
    button1.draw()
    pygame.display.update()
    clock.tick(60)
