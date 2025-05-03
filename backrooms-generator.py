import random
import math

# Generate a maze using Prim's Algorithm
def generate_maze(width, height):
    maze = [
        [[x, y, CELL_SIZE, False] for x in range(0, width, CELL_SIZE)]
        for y in range(0, height, CELL_SIZE)
    ]
    visited_cells = set()

    for _ in range(NUM_MAZES):
        x, y = random.randint(0, NUM_COLS - 1), random.randint(0, NUM_ROWS - 1)
        visited_cells.add((x, y))
        frontier = [(x, y)]

        while len(visited_cells) / (NUM_COLS * NUM_ROWS) < MAZE_FILL_PERCENTAGE:
            if not frontier:
                break

            x, y = random.choice(frontier)
            visited_cells.add((x, y))
            frontier.remove((x, y))

            maze[y][x][3] = True

            neighbors = []
            if x > 1 and (x - 2, y) not in visited_cells:
                neighbors.append((x - 2, y))
            if x < NUM_COLS - 2 and (x + 2, y) not in visited_cells:
                neighbors.append((x + 2, y))
            if y > 1 and (x, y - 2) not in visited_cells:
                neighbors.append((x, y - 2))
            if y < NUM_ROWS - 2 and (x, y + 2) not in visited_cells:
                neighbors.append((x, y + 2))

            if neighbors:
                next_cell = random.choice(neighbors)
                nx, ny = next_cell

                # Check if the next cell collides with a previous maze
                if (
                    random.random() > STOP_COLLISION_PROBABILITY
                    or maze[(y + ny) // 2][(x + nx) // 2][3] == False
                ):
                    frontier.append((nx, ny))
                    maze[(y + ny) // 2][(x + nx) // 2][3] = True

    return maze


# Generate rooms on the maze
def generate_rooms(maze):
    for _ in range(NUM_ROOMS):
        room_width = random.randint(ROOM_WIDTH_RANGE[0], ROOM_WIDTH_RANGE[1])
        room_height = random.randint(ROOM_HEIGHT_RANGE[0], ROOM_HEIGHT_RANGE[1])
        x = random.randint(0, NUM_COLS - room_width)
        y = random.randint(0, NUM_ROWS - room_height)

        for row in range(y, y + room_height):
            for col in range(x, x + room_width):
                maze[row][col][3] = True


# Generate rooms with pillars on the maze
def generate_pillar_rooms(maze):
    for _ in range(NUM_PILLAR_ROOMS):
        room_width = random.randint(
            PILLAR_ROOM_WIDTH_RANGE[0], PILLAR_ROOM_WIDTH_RANGE[1]
        )
        room_height = random.randint(
            PILLAR_ROOM_HEIGHT_RANGE[0], PILLAR_ROOM_HEIGHT_RANGE[1]
        )
        x = random.randint(0, NUM_COLS - room_width)
        y = random.randint(0, NUM_ROWS - room_height)

        for row in range(y, y + room_height):
            for col in range(x, x + room_width):
                maze[row][col][3] = True

        # Add pillars
        pillar_spacing = random.randint(
            PILLAR_SPACING_RANGE[0], PILLAR_SPACING_RANGE[1]
        )
        for row in range(y, y + room_height, pillar_spacing):
            for col in range(x, x + room_width, pillar_spacing):
                maze[row][col][3] = False


# Function to check if a point is inside a custom-shaped room
def is_inside_custom_room(x, y, vertices):
    num_vertices = len(vertices)
    inside = False

    for i in range(num_vertices):
        j = (i + 1) % num_vertices

        if vertices[i][0] < vertices[j][0]:
            left_vertex = vertices[i]
            right_vertex = vertices[j]
        else:
            left_vertex = vertices[j]
            right_vertex = vertices[i]

        if (vertices[i][1] > y) != (vertices[j][1] > y) and x < (
            right_vertex[0] - left_vertex[0]
        ) * (y - left_vertex[1]) / (right_vertex[1] - left_vertex[1]) + left_vertex[0]:
            inside = not inside

    return inside


# Generate rooms with random shapes
def generate_custom_rooms(maze):
    for _ in range(NUM_CUSTOM_ROOMS):
        num_sides = random.randint(MIN_NUM_SIDES, MAX_NUM_SIDES)
        room_radius = random.randint(MIN_CUSTOM_ROOM_RADIUS, MAX_CUSTOM_ROOM_RADIUS)
        x = random.randint(
            room_radius * 2, NUM_COLS - room_radius * 2
        )  # Avoid rooms too close to the edge
        y = random.randint(room_radius * 2, NUM_ROWS - room_radius * 2)

        vertices = []
        angle_step = math.pi * 2 / num_sides
        for i in range(num_sides):
            angle = i * angle_step
            vertex_x = int(x + room_radius * math.cos(angle))
            vertex_y = int(y + room_radius * math.sin(angle))
            vertices.append((vertex_x, vertex_y))

        for row in range(y - room_radius, y + room_radius):
            for col in range(x - room_radius, x + room_radius):
                if is_inside_custom_room(col, row, vertices):
                    maze[row][col][3] = True

def backrooms(w,h):
    maze = generate_maze(SCREEN_WIDTH, SCREEN_HEIGHT)
    generate_rooms(maze)
    generate_pillar_rooms(maze)
    generate_custom_rooms(maze)
    return maze
