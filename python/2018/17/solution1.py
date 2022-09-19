
def print_solution(solution):
    """formats solution for printing"""
    print(f"The solution is: {solution}")


class Scan():
    def __init__(self):
        self.clay = {}
        self.water = {}
        self.previous_downs = []
        self.actions = []
        self.seen = set()
        self.drip = (500, 0)
        self.x_min, self.x_max = 0, 0
        self.y_min, self.y_max = 0, 0
        self.add_action(self.drip, 'down')

    def flow_down(self, position):
        """
            find all positions straight down until hitting clay or bottom
            return down positions
        """
        blocker_clay = [x for x in self.clay if (x[0] == position[0] and x[1] > position[1])]
        blocker_water = [x for x in self.water if (x[0] == position[0] and x[1] > position[1])]
        blocker = blocker_clay[:] + blocker_water[:]
        if len(blocker) == 0:
            end = self.y_max + 1
        else:
            end = min([x[1] for x in blocker])

        if (position[0], end) in blocker_water:
            self.add_action((position[0], end), 'across')
        elif (position[0], end) in blocker_clay:
            self.add_action((position[0], end-1), 'across')

        for y in range(position[1], end):
            self.water[(position[0], y)] = '|'


    def flow_across(self, position):
        """
            find all positions left and right until either:
                1. hitting water/clay
                2. not having water/clay underneath
            return across positions
        """
        # add self
        self.water[position] = '~'
        if position[1] == self.y_max:
            return

        right_bounded = True
        left_bounded = True

        # check right
        x, y = position
        flowing_right = True
        seen_clay = (x, y+1) in self.clay
        while flowing_right:
            x += 1
            over_water = (x, y+1) in self.water and self.water[(x, y+1)] == '~'
            over_clay = (x, y+1) in self.clay
            seen_clay = over_clay or seen_clay
            flowing_right = (over_clay or over_water) and (x, y) not in self.clay and x <= self.x_max
            if flowing_right:
                self.water[(x, y)] = '~'
            else:
                if (x, y) not in self.clay:
                    self.add_action((x, y), 'down')
                    right_bounded = False

        # check left
        x, y = position
        flowing_left = True
        seen_clay = (x, y+1) in self.clay
        while flowing_left:
            x -= 1
            over_water = (x, y+1) in self.water and self.water[(x, y+1)] == '~'
            over_clay = (x, y+1) in self.clay
            seen_clay = over_clay or seen_clay
            flowing_left = (over_clay or over_water) and (x, y) not in self.clay and x >= self.x_min
            if flowing_left:
                self.water[(x, y)] = '~'
            else:
                if (x, y) not in self.clay:
                    self.add_action((x, y), 'down')
                    left_bounded = False

        if right_bounded and left_bounded:
            self.add_action((position[0], position[1] - 1), 'across')


    def add_action(self, position, direction):
        if direction in ['down', 'across']:
            action = ((position), direction)
            if action not in self.seen:
                self.seen.add(action)
                self.actions.append(((position), direction))
        else:
            raise ValueError(f"Not a valid direction: {direction}")


    def process_action(self):
        if len(self.actions) == 0:
            return False
        position, direction = self.actions.pop(0)
        if direction == 'across':
            self.flow_across(position)
        elif direction == 'down':
            self.flow_down(position)
        else:
            raise ValueError(f"direction is invalid: {direction}")
        return True

    def __repr__(self):
        output = []
        for y in range(self.y_min - 1, self.y_max + 2):
            row = ''
            for x in range(self.x_min - 1, self.x_max + 1):
                if (x, y) in self.clay and (x, y) in self.water:
                    row = row + '&'
                elif (x, y) in self.clay:
                    row = row + self.clay[(x, y)]
                elif (x, y) in self.water:
                    row = row + self.water[(x, y)]
                else:
                    row = row + ' '
            output.append(row)
        return '\n'.join(output[0:100])


def main():
    file = open('input.txt', 'r', encoding='utf-8')

    scan = Scan()

    # add clay positions
    for line in file.readlines():
        part_a, part_b = line.strip().split(', ')
        a = int(part_a.split('=')[-1])
        b_min, b_max = [int(x) for x in part_b.split('=')[-1].split('..')]
        for b in range(b_min, b_max + 1):
            if part_a[0] == 'x':
                scan.clay[(a, b)] = '#'
            else:
                scan.clay[(b, a)] = '#'
    # add boundries
    x_all = [x[0] for x in scan.clay]
    y_all = [x[1] for x in scan.clay]
    scan.x_min, scan.x_max = min(x_all), max(x_all)
    scan.y_min, scan.y_max = min(y_all), max(y_all)

    cycles = 0
    while scan.process_action():
        cycles += 1

    valid_water = [w for w in scan.water.keys() if w[1] >= scan.y_min]
    print_solution(len(valid_water))


if __name__ == "__main__":
    main()
