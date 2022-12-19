from turtle import pos
import networkx


def print_solution(x):
    """formats input for printing"""
    print(f"The solution is: {x}")


def get_new_position(position, move):
    """ Finds new position based input of
    current position and direction.
    returns tuple"""

    direction = {'N': (0, 1), 'E': (-1, 0), 'S': (0, -1), 'W': (1, 0)}
    if move not in direction:
        raise ValueError(f"Invalid direction {move}")
    x = position[0] + direction[move][0]
    y = position[1] + direction[move][1]
    return (x, y)


def main():
    file = open('input.txt', 'r', encoding='utf-8')
    moves = file.readline().strip()
    moves = moves[1:-1]

    stack = []
    elf_map = networkx.Graph()
    start = (0, 0)
    position = {start}
    start_positions = {start}
    end_positions = set()

    for move in moves:
        if move == '|':
            end_positions.update(position)
            position = start_positions
        elif move in 'NSEW':
            elf_map.add_edges_from((p, get_new_position(p, move)) for p in position)
            position = {get_new_position(p, move) for p in position}
        elif move == '(':
            stack.append((start_positions, end_positions))
            start_positions, end_positions = position, set()
        elif move == ')':
            position.update(end_positions)
            start_positions, end_positions = stack.pop()

    lengths = networkx.algorithms.shortest_path_length(elf_map, (0,0))

    print_solution(max(lengths.values()))


if __name__ == "__main__":
    main()
