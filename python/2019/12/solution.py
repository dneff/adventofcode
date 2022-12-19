from Point import Point

def lcm(x, y):
    from math import gcd
    return x * y // gcd(x, y)

x = Point(0,0,0)

def main():

    initial_objects = []
    with open('input1.txt', 'r') as file:
        for data in file.readlines():
            pos = [int(x.split('=')[-1]) for x in data.strip().replace('<','').replace('>','').split(', ')]
            initial_objects.append(Point(*pos))

    objects = initial_objects[:]

    steps = 1000
    for _ in range(steps):
        for i in range(len(objects)):
            for j in range(len(objects)):
                if i != j:
                    objects[i].updateVelocity(objects[j])

        for o in objects:
            o.updatePosition()

    solution = sum([x.getEnergy() for x in objects])

    print(f"Solution 1: The total system energy after {steps} steps is: {solution}")


# -=-=-=- Part 2
    x_steps = 0 
    y_steps = 0 
    z_steps = 0 
    total_steps = 0

    objects = initial_objects[:]
    init_x = [(o.pos_x, o.vel_x) for o in objects]
    init_y = [(o.pos_y, o.vel_y) for o in objects]
    init_z = [(o.pos_z, o.vel_z) for o in objects]
    init_x.sort()
    init_y.sort()
    init_z.sort()

    while x_steps == 0 or y_steps == 0 or z_steps == 0:
        total_steps += 1
        for i in range(len(objects)):
            for j in range(len(objects)):
                if i != j:
                    objects[i].updateVelocity(objects[j])

        for o in objects:
            o.updatePosition()

        if x_steps == 0:
            latest_x = [(o.pos_x, o.vel_x) for o in objects]
            latest_x.sort()

            if init_x == latest_x:
                x_steps = total_steps
        if y_steps == 0:
            latest_y = [(o.pos_y, o.vel_y) for o in objects]
            latest_y.sort()

            if init_y == latest_y:
                y_steps = total_steps

        if z_steps == 0:
            latest_z = [(o.pos_z, o.vel_z) for o in objects]
            latest_z.sort()

            if init_z == latest_z:
                z_steps = total_steps               
        

    print(f"Solution 2: The universe repeats after {lcm(x_steps, lcm(y_steps, z_steps))}")


if __name__ == "__main__":
    main()