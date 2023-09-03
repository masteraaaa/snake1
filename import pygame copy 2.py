import pygame
import sys
import random
from pygame.math import Vector2 as v2
import random


class Node:
    def __init__(self, position):
        self.position = position
        self.parent = None
        self.g = 0
        self.h = 0

class AStarPathfinder:
    def __init__(self, grid):
        self.grid = grid
        
    
    def find_path(self, start, end):
        open_list = []
        closed_list = []

        start_node = Node(start)
        start_node.g = 0
        start_node.h = self.calculate_h_score(start, end)
        open_list.append(start_node)

        while open_list:
            current_node = self.find_lowest_f_score_node(open_list)
            open_list.remove(current_node)
            closed_list.append(current_node)

            if current_node.position == end:
                return self.construct_path(current_node)

            neighbors = self.get_neighbors(current_node.position)
            for neighbor_pos in neighbors:
                if self.is_in_list(closed_list, neighbor_pos):
                    continue

                g_score = current_node.g + 1  # Assuming uniform cost
                h_score = self.calculate_h_score(neighbor_pos, end)
                

                neighbor_node = Node(neighbor_pos)
                if not self.is_in_list(open_list, neighbor_pos) or g_score < neighbor_node.g:
                    neighbor_node.g = g_score
                    neighbor_node.h = h_score
                    neighbor_node.parent = current_node

                    if neighbor_node not in open_list:
                        open_list.append(neighbor_node)

        return None  # No path found

    def find_lowest_f_score_node(self, open_list):
        lowest_f_score = float('inf')
        lowest_node = None
        for node in open_list:
            if node.g + node.h < lowest_f_score:
                lowest_f_score = node.g + node.h
                lowest_node = node
        return lowest_node

    def construct_path(self, node):
        path = []
        current = node
        while current is not None:
            path.insert(0, current.position)
            current = current.parent
        return path

    def calculate_h_score(self, pos, end):
        # Implement heuristic calculation (e.g., Manhattan distance)
        return abs(pos[0] - end[0]) + abs(pos[1] - end[1])

    def get_neighbors(self, pos):
        x, y = pos
        neighbors = []

        # Check adjacent positions (up, down, left, right)
        possible_neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

        for neighbor_pos in possible_neighbors:
            neighbor_x, neighbor_y = neighbor_pos
            neighbor_x = int(neighbor_x)  # Convert to integer
            neighbor_y = int(neighbor_y)  # Convert to integer
            if (
                0 <= neighbor_x < len(self.grid)
                and 0 <= neighbor_y < len(self.grid[0])
                and not self.grid[neighbor_y][neighbor_x]
                and not self.is_snake_body(neighbor_pos)
            ):
                neighbors.append(neighbor_pos)

        return neighbors
    
    def is_snake_body(self, pos):
        for segment in main_game.snake.body:
            if pos == (segment.x, segment.y):
                return True
        return False
    

    def is_in_list(self, node_list, pos):
        for node in node_list:
            if node.position == pos:
                return True
        return False
    
    def calculate_h_score(self, pos, end):
        x, y = pos
        target_x, target_y = end
        

        h_score = abs(x - target_x) + abs(y - target_y)
        
        
        
        
        return h_score
    def find_reverse_path(self, start, end):
        open_list = []
        closed_list = []

        start_node = Node(end)  # Start from the goal
        start_node.g = 0
        start_node.h = self.calculate_h_score(end, start)
        open_list.append(start_node)

        while open_list:
            current_node = self.find_lowest_f_score_node(open_list)
            open_list.remove(current_node)
            closed_list.append(current_node)

            if current_node.position == start:
                return self.construct_reverse_path(current_node)

            neighbors = self.get_neighbors(current_node.position)
            for neighbor_pos in neighbors:
                if self.is_in_list(closed_list, neighbor_pos):
                    continue

                g_score = current_node.g + 1  # Assuming uniform cost
                h_score = self.calculate_h_score(neighbor_pos, start)

                neighbor_node = Node(neighbor_pos)
                if not self.is_in_list(open_list, neighbor_pos) or g_score < neighbor_node.g:
                    neighbor_node.g = g_score
                    neighbor_node.h = h_score
                    neighbor_node.parent = current_node

                    if neighbor_node not in open_list:
                        open_list.append(neighbor_node)

        return None  # No reverse path found

    def construct_reverse_path(self, node):
        path = []
        current = node
        while current is not None:
            path.append(current.position)
            current = current.parent
        return path[::-1]  # Reverse the path to go from start to goal


class SNAKE:
    def __init__(self):
        self.body = [v2(7, 10), v2(6, 10), v2(5, 10)]
        self.direction = v2(1,0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (0, 0, 255), block_rect)

    def move_snake(self):
        
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0]+self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:

            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0]+self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block =True



class FRUIT:
    def __init__(self):
        self.randomise()
        self.snake = SNAKE()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.x * cell_size), int(self.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, (255, 166, 114), fruit_rect)

    def nofruitonsnake(self):
        if self.pos == self.snake.body:
            self.randomise()

    def randomise(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = v2(self.x, self.y) 
    def find_nearest_path(self):
        pathfinder = AStarPathfinder(main_game.grid)
        start = main_game.snake.body[0]
        end = self.pos
        return pathfinder.find_path(start, end)
    
    

class MAIN:
    def __init__(self):
        self.grid = [[0] * cell_number for _ in range(cell_number)]
        self.fruit = FRUIT()
        self.snake = SNAKE()
        self.score = 0
        self.moves = 0
        self.path = []
        

    def update(self):
        pathfinder = AStarPathfinder(self.grid)
        start = self.snake.body[0]
        end = self.fruit.pos
        
        
        if len(self.snake.body) > 100:
            nearest_path = self.fruit.find_nearest_path()
            if nearest_path:
                next_pos = nearest_path[1]
                direction = v2(next_pos[0] - start.x, next_pos[1] - start.y)
                
        else:
            self.path = pathfinder.find_path(start, end)
            if self.path is not None and len(self.path) > 1:
                next_pos = self.path[1]
                direction = v2(next_pos[0] - start.x, next_pos[1] - start.y)

                if not 0 <= next_pos[0] < cell_number or not 0 <= next_pos[1] < cell_number:
                    if self.snake.direction.x == 1:  
                        self.snake.direction = v2(0, -1)  
                    elif self.snake.direction.x == -1: 
                        self.snake.direction = v2(0, 1)  
                    elif self.snake.direction.y == 1:  
                        self.snake.direction = v2(-1, 0) 
                    elif self.snake.direction.y == -1:  
                        self.snake.direction = v2(1, 0)  
                else:
                    if direction == v2(1, 0):
                        self.snake.direction = v2(1, 0)
                    elif direction == v2(-1, 0):
                        self.snake.direction = v2(-1, 0)
                    elif direction == v2(0, 1):
                        self.snake.direction = v2(0, 1)
                    elif direction == v2(0, -1):
                        self.snake.direction = v2(0, -1)

    
        self.snake.move_snake()
    
        self.check_collision()
        self.check_fail()

    def draw_path(self):
        if self.path:
            for pos in self.path:
                center = (
                    int(pos[0] * cell_size) + cell_size // 2,
                    int(pos[1] * cell_size) + cell_size // 2,
                )
                pygame.draw.circle(screen, (255, 0, 0), center, cell_size // 8)


    def draw_element(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_path()
        pygame.display.update()

        if self.path:
            for pos in self.path:
                x_pos = int(pos[0] * cell_size) + cell_size // 2
                y_pos = int(pos[1] * cell_size) + cell_size // 2
                pygame.draw.circle(screen, (255, 0, 0), (x_pos, y_pos), cell_size // 4)

    
    def check_collision(self):
        
        if self.fruit.pos == self.snake.body[0]:
            self.score+=1
            self.fruit.randomise()
            self.snake.add_block()
            self.draw_path()
            


    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.score+=1
            print("lost")  
            print(self.score)
            pygame.quit()
            sys.exit()
            
            

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.score+=1
                print("lost")
                print(self.score)
                pygame.quit()
                sys.exit()
                

    
                

    def reset_snake(self):
        self.snake.body = [v2(7, 10), v2(6, 10), v2(5, 10)]
        self.snake.direction = v2(1, 0)
        self.path = []
                

    def game_over(self):
        pygame.quit()
        sys.exit()

    


pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()


fruit = FRUIT()
snake = SNAKE()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and main_game.snake.direction != v2(0,1):
                    main_game.snake.direction = v2(0,-1)
                if event.key == pygame.K_RIGHT and main_game.snake.direction != v2(-1,0):
                    main_game.snake.direction = v2(1,0) 
                if event.key == pygame.K_LEFT and main_game.snake.direction != v2(1,0):
                    main_game.snake.direction = v2(-1,0) 
                if event.key == pygame.K_DOWN and main_game.snake.direction != v2(0,-1):
                    main_game.snake.direction = v2(0,1)

    
    screen.fill((175, 215, 70))
    main_game.update()
    main_game.draw_element()
    pygame.display.update()
    clock.tick(60)