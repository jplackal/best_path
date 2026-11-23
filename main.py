import asyncio
import pygame
import random
import sys

pygame.init()
random.seed()

WIDTH = 1300
HEIGHT = 750

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Best Path")
sys.setrecursionlimit(50000)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)
font2 = pygame.font.SysFont(None, 40)

text = font.render("", True, (255, 255, 255))
display = font2.render("", True, (255, 255, 255)).convert_alpha()
alpha = 255

points = []
start_id = -1
end_id = -1
path = []
drag_id = -1
link_id = -1
expanded = 1
groups = [[0,99], [90, 9], [20,0]]
all_paths = []

def setup_grid(columns, rows, grid_size):
    global points
    points = []
    offset_x = (WIDTH - grid_size*(columns-1))/2
    offset_y = (HEIGHT - grid_size*(rows-1))/2
    for i in range(columns):
        for i2 in range(rows):
            points.append([i*grid_size+offset_x, i2*grid_size+offset_y, [], []])
    for i, p in enumerate(points):
        for i2, p2 in enumerate(points):
            if p2 != p:
                dist = ((p[0]-p2[0])**2+(p[1]-p2[1])**2)
                if dist <= grid_size**2 and (i not in p2[2]) and (i2 not in p[2]):
                    p[2].append(i2)
                    p2[2].append(i)
                    n = random.randint(0,10)
                    p[3].append(n)
                    p2[3].append(n)
def contains(item, list):
    return_val = ""
    for i in list:
        if item == i[0]:
            if "start" not in return_val:
                if return_val == "end":
                    return_val = "start and end"
                else:
                    return_val = "start"
        if item == i[1]:
            if "end" not in return_val:
                if return_val == "start":
                    return_val = "start and end"
                else:
                    return_val = "end"
    if return_val != "":
        return return_val
    return None
def draw_path(path):
    if len(path) > 0:
        for i in range(len(path)-1):
            pygame.draw.line(screen, (200, 255, 200), (points[path[i]][0], points[path[i]][1]), (points[path[i+1]][0], points[path[i+1]][1]), 12)

def draw():
    global groups
    for i in all_paths:
        draw_path(i)
    for i2, p in enumerate(points):
        for i, l in enumerate(p[2]):
            pygame.draw.line(screen, (155, 155, 155), (p[0], p[1]), (points[l][0], points[l][1]), 5)
            text = font.render(f"{p[3][i]}",True,(155,155,155))
            text_rect = text.get_rect(midright=(round((p[0]+points[l][0])/2)-5, round((p[1]+points[l][1])/2)-10))
            screen.blit(text,text_rect)
    for i, p in enumerate(points):
        contain = contains(i, groups)
        if i == link_id:
            pygame.draw.circle(screen, (100,200,255), (p[0], p[1]), 15)
        if contain == "start":
            pygame.draw.circle(screen, (255,100,100), (p[0], p[1]), 15)
        if contain == "end":
            pygame.draw.circle(screen, (100,255,100), (p[0], p[1]), 15)
        if contain == "start and end":
            pygame.draw.circle(screen, (255,100,100), (p[0], p[1]), 15)
            pygame.draw.circle(screen, (100,255,100), (p[0], p[1]), 12.5)
        pygame.draw.circle(screen, (255,255,255), (p[0], p[1]), 10)

def recursive(path_list, end_id):
    global found_path, path, expanded
    points_done = [every_path[0]]
    temp_list = every_path
    for id, i in enumerate(path_list):
        temp_list = temp_list[i]
        if id%2 == 1:
            points_done.append(temp_list[0])
    temp_list[1] += 1
    for id in points[temp_list[0]][2]:
        if id not in taken_points:
            time_taken = points[temp_list[0]][3][points[temp_list[0]][2].index(id)]
            expanded = 1
            if temp_list[1] >= time_taken:
                taken_points.append(id)
                temp_list[2].append([id, (temp_list[1]-time_taken)-1, []])
                if id == end_id:
                    found_path = 1
                    path = path_list + [2, len(temp_list[2]) - 1]
                    return
    screen.fill((0,0,0))
    draw()

    if len(temp_list[2]) != 0:
        path_list.append(2)
        path_list.append(0)
        recursive(path_list, end_id)
    else:
        done = 0
        while done == 0:
            if path_list == []:
                return
            last_idx = path_list.pop(-1)
            path_list.pop(-1)
            temp_list = every_path
            for i in path_list:
                temp_list = temp_list[i]
            if len(temp_list[2]) - 1 > last_idx:
                path_list.append(2)
                path_list.append(last_idx + 1)
                done = 1
        recursive(path_list, end_id)

def refine_path(path):
    new_path = []
    temp_list = every_path
    for id, i in enumerate(path):
        temp_list = temp_list[i]
        if isinstance(temp_list[0], int):
            new_path.append(temp_list[0])
    return new_path

def shortest_path(start_id, end_id):
    global every_path, taken_points, found_path, path, expanded
    if start_id == -1 or end_id == -1:
        return
    found_path = 0
    limit = 1000
    time = 0
    every_path = [start_id, -1, []]
    taken_points = [start_id]
    expanded = 1
    while time < limit and found_path == 0 and expanded:
        expanded = 0
        recursive([], end_id)
        draw_current_path(every_path)
        pygame.display.flip()
        clock.tick(60)
        time += 1
    if found_path:
        path = refine_path(path)
        path.insert(0, start_id)
        all_paths.append(path)
    print(path)


def find_closest_start():
    global start_id
    if len(points) == 0:
        return
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dists = []
    for i in points:
        dist = ((mouse_x-i[0])**2+(mouse_y-i[1])**2)
        dists.append(dist)
    start_id = dists.index(min(dists))

def find_closest_end():
    global end_id
    if len(points) == 0:
        return
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dists = []
    for i in points:
        dist = ((mouse_x-i[0])**2+(mouse_y-i[1])**2)
        dists.append(dist)
    end_id = dists.index(min(dists))

def find_closest():
    if len(points) == 0:
        return -1
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dists = []
    for i in points:
        dist = ((mouse_x-i[0])**2+(mouse_y-i[1])**2)
        dists.append(dist)
    return dists.index(min(dists))

def find_hovered():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for idx, i in enumerate(points):
        if ((mouse_x-i[0])**2+(mouse_y-i[1])**2) <= 15**2:
            return idx
    return -1

setup_grid(10, 10, 75)

def drag(point):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    points[point][0] = mouse_x
    points[point][1] = mouse_y

def recursive_draw(path, every_path):
    temp_list = every_path
    for i in path:
        temp_list = temp_list[i]
    for i, child in enumerate(temp_list[2]):
        line_start = (points[temp_list[0]][0], points[temp_list[0]][1])
        line_end = (points[child[0]][0], points[child[0]][1])
        pygame.draw.line(screen, (200, 255, 200), line_start, line_end, 12)
        recursive_draw(path+[2,i], every_path)
    display = font2.render("Finding Path", True, (255, 255, 255)).convert_alpha()     
    display.set_alpha(255)
    screen.blit(display,(10,10))

def delete_point():
    global link_id, path, all_paths, groups
    point = find_closest()
    if point == -1:
        return
    for i, group in enumerate(groups):
        if point in group:
            groups.pop(i)
            all_paths = []
            return
    for i in points:
        if point in i[2]:
            idx = i[2].index(point)
            i[2].pop(idx)
            i[3].pop(idx)
    for i in points:
        for idx, connection in enumerate(i[2]):
            if connection > point:
                i[2][idx] -= 1
    for group in groups:
        for idx in range(2):
            if group[idx] > point:
                group[idx] -= 1
    if link_id == point:
        link_id = -1
    elif link_id > point:
        link_id -= 1
    points.pop(point)
    all_paths = []

def draw_current_path(every_path):
    recursive_draw([], every_path)

async def main():
    global alpha, display, all_paths, points, start_id, end_id, drag_id, link_id, groups
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c and drag_id == -1:
                    all_paths = []
                    if groups != []:
                        for i in groups:
                            shortest_path(i[0], i[1])
                        display = font2.render("Found Path/Paths", True, (255, 255, 255)).convert_alpha()
                    else:
                        display = font2.render("No Points", True, (255, 255, 255)).convert_alpha()     
                    alpha = 500
                elif event.key == pygame.K_d and drag_id == -1:
                    start_id = -1
                    end_id = -1
                    link_id = -1
                    setup_grid(10, 10, 75)
                    display = font2.render("", True, (255, 255, 255)).convert_alpha()
                    alpha = 500
                    groups = []
                    all_paths = []
                elif event.key == pygame.K_s and drag_id == -1:
                    find_closest_start()
                elif event.key == pygame.K_e and drag_id == -1:
                    find_closest_end()
                elif event.key == pygame.K_r and drag_id == -1:
                    start_id = -1
                    end_id = -1
                    link_id = -1
                    points = []
                    all_path = []
                    groups = []
                elif event.key == pygame.K_BACKSPACE:
                    delete_point()
                elif event.key == pygame.K_a and drag_id == -1:
                    hovered = find_hovered()
                    if hovered != -1:
                        if link_id == -1:
                            link_id = hovered
                        elif link_id != hovered and hovered not in points[link_id][2]:
                            dist = round((((points[link_id][0]-points[hovered][0])**2+(points[link_id][1]-points[hovered][1])**2)**0.5)/20)
                            points[link_id][2].append(hovered)
                            points[hovered][2].append(link_id)
                            points[link_id][3].append(dist)
                            points[hovered][3].append(dist)
                            link_id = -1
                        else:
                            link_id = -1
                    else:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        points.append([mouse_x, mouse_y, [], []])
                        link_id = -1
        screen.fill((0, 0, 0))
        left_down, middle_down, right_down = pygame.mouse.get_pressed()
        if left_down and len(points) > 0:
            if drag_id == -1:
                drag_id = find_closest()
            drag(drag_id)
        else:
            drag_id = -1
        draw()
        alpha -= 5
        display.set_alpha(alpha)
        screen.blit(display,(10,10))
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)
asyncio.run(main())