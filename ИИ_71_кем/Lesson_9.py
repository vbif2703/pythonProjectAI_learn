#Задача на острова УЛЬТРА МЕГА СЛОЖНЫЙ УРОВЕНЬ !!!
# нужно генерировать карту островов на карте
# острова состоят из суши - * и полностю окружены водой - 0
# карта должна генерироваться рандомно
# правила генерации -
# 1 запрещается внутри острова генерить воду
# 2 остров должен быть полностью окружен водой
# 3 запрещается делать еденичный остров,  минимум 5 - *
# 4 край карты должен быть заполнен водой в 3 ряда
# пользователь выбирает количество и плотность расположение островов относительно центра карты
import random
from collections import deque


def generate_island_map(width=80, height=50, num_islands=5, density=0.5):
    """
    Генерирует карту островов.

    :param width:       ширина карты
    :param height:      высота карты
    :param num_islands: количество островов
    :param density:     0.0 — равномерно по карте, 1.0 — плотно у центра
    :return:            2D-список символов '0' и '*'
    """
    BORDER = 3
    MIN_SIZE = 5

    #Заполняем карту водой 
    grid = [['0'] * width for _ in range(height)]

    #Вспомогательные функции 

    def pick_center():
        """Стартовая точка острова с учётом плотности к центру."""
        cx, cy = width // 2, height // 2
        spread_x = max(1, int((width  / 2 - BORDER - 2) * (1 - density * 0.85)))
        spread_y = max(1, int((height / 2 - BORDER - 2) * (1 - density * 0.85)))
        x = random.randint(max(BORDER + 1, cx - spread_x),
                           min(width  - BORDER - 2, cx + spread_x))
        y = random.randint(max(BORDER + 1, cy - spread_y),
                           min(height - BORDER - 2, cy + spread_y))
        return x, y

    def can_place(x, y, own_cells):
        """Можно ли поставить '*' в (x, y): не граница, не чужой остров."""
        if not (BORDER <= x < width - BORDER and BORDER <= y < height - BORDER):
            return False
        if grid[y][x] == '*':
            return False
        # 8-связность: не касаемся чужих островов даже по диагонали
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    if grid[ny][nx] == '*' and (nx, ny) not in own_cells:
                        return False
        return True

    def has_holes(island_cells):
        """True, если внутри bounding-box острова есть замкнутая вода."""
        if not island_cells:
            return False
        island_set = set(island_cells)
        min_x = min(c[0] for c in island_set)
        max_x = max(c[0] for c in island_set)
        min_y = min(c[1] for c in island_set)
        max_y = max(c[1] for c in island_set)

        visited = set()
        for sy in range(min_y, max_y + 1):
            for sx in range(min_x, max_x + 1):
                if (sx, sy) in island_set or (sx, sy) in visited:
                    continue
                # BFS по воде внутри bounding-box
                queue = deque([(sx, sy)])
                visited.add((sx, sy))
                touches_border = False
                while queue:
                    cx, cy = queue.popleft()
                    if cx == min_x or cx == max_x or cy == min_y or cy == max_y:
                        touches_border = True
                    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                        nx, ny = cx + dx, cy + dy
                        if (min_x <= nx <= max_x and min_y <= ny <= max_y
                                and (nx, ny) not in island_set
                                and (nx, ny) not in visited):
                            visited.add((nx, ny))
                            queue.append((nx, ny))
                if not touches_border:
                    return True          
        return False

    def grow_island(target_size):
        """Выращивает один остров случайным ростом (4-связность)."""
        for _ in range(200):                       
            sx, sy = pick_center()
            if grid[sy][sx] != '0':
                continue

            island = {(sx, sy)}
            frontier = [(sx + dx, sy + dy)
                        for dx, dy in ((-1,0),(1,0),(0,-1),(0,1))]

            ok = True
            while len(island) < target_size:
                random.shuffle(frontier)
                placed = False
                for i, (fx, fy) in enumerate(frontier):
                    if (fx, fy) not in island and can_place(fx, fy, island):
                        island.add((fx, fy))
                        frontier.pop(i)
                        for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                            nc = (fx + dx, fy + dy)
                            if nc not in island and nc not in frontier:
                                frontier.append(nc)
                        placed = True
                        break
                if not placed:
                    ok = False
                    break

            if ok and len(island) >= MIN_SIZE and not has_holes(island):
                return island
        return None

    #Генерация островов 
    placed_count = 0
    for _ in range(num_islands * 3):                
        if placed_count >= num_islands:
            break
        target = random.randint(MIN_SIZE, MIN_SIZE + 20)
        island = grow_island(target)
        if island:
            for x, y in island:
                grid[y][x] = '*'
            placed_count += 1

    if placed_count < num_islands:
        print(f" Удалось разместить только {placed_count} из {num_islands} островов.")

    return grid


def print_map(grid):
    """Красивый вывод карты."""
    print()
    for row in grid:
        line = ''
        for ch in row:
            if ch == '*':
                line += '\033[32m██\033[0m'   # зелёная суша
            else:
                line += '\033[34m~~\033[0m'   # синяя вода
        print(line)
    print()

#Главный блок

if __name__ == '__main__':
    print(" Генератор карты островов\n")

    try:
        w = int(input("Ширина карты  (60–120, Enter=80): ") or 80)
        h = int(input("Высота карты  (30–80,  Enter=50): ") or 50)
        n = int(input("Количество островов (1–20): "))
        d = float(input("Плотность к центру (0.0 — равномерно, 1.0 — у центра): "))
    except ValueError:
        print("Некорректный ввод — используем значения по умолчанию.")
        w, h, n, d = 80, 50, 5, 0.5

    d = max(0.0, min(1.0, d))
    n = max(1, min(30, n))

    grid = generate_island_map(w, h, n, d)
    print_map(grid)



# я заколебался !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
