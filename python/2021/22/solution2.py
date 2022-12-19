import copy


def printSolution(x):
    print(f"The solution is {x}")


def shard(c1, cubes):
    shards = set()
    deletes = set()

    command1, x1, y1, z1 = c1[0], *c1[1]
    min_x1, max_x1, min_y1, max_y1, min_z1, max_z1 = *x1, *y1, *z1

    c2_added = False

    for c2 in cubes:
        # if c2 overlaps with c1, define new cubes to encompass remaining area
        # it's cubes all the way down

        command2, x2, y2, z2 = c2[0], *c2[1]
        min_x2, max_x2, min_y2, max_y2, min_z2, max_z2 = *x2, *y2, *z2

        if not (
            min_x2 <= max_x1 and min_x1 <= max_x2 and
            min_y2 <= max_y1 and min_y1 <= max_y2 and
            min_z2 <= max_z1 and min_z1 <= max_z2
        ):
            continue

        min_shared_x, max_shared_x = max(min_x2, min_x1), min(max_x2, max_x1)
        min_shared_y, max_shared_y = max(min_y2, min_y1), min(max_y2, max_y1)
        min_shared_z, max_shared_z = max(min_z2, min_z1), min(max_z2, max_z1)

        deletes.add(copy.deepcopy(c2))
        c2_added = True

        if min_x2 < min_shared_x:
            shards.add(
                (
                    command2,
                    (
                        (min_x2, min_shared_x - 1),
                        (min_y2, max_y2),
                        (min_z2, max_z2)
                    )
                )
            )

        if max_shared_x < max_x2:
            shards.add(
                (
                    command2,
                    (
                        (max_shared_x + 1, max_x2),
                        (min_y2, max_y2),
                        (min_z2, max_z2)
                    )
                )
            )

        if min_y2 < min_shared_y:
            shards.add(
                (
                    command2,
                    (
                        (min_shared_x, max_shared_x),
                        (min_y2, min_shared_y - 1),
                        (min_z2, max_z2)
                    )
                )
            )

        if max_shared_y < max_y2:
            shards.add(
                (
                    command2,
                    (
                        (min_shared_x, max_shared_x),
                        (max_shared_y + 1, max_y2),
                        (min_z2, max_z2)
                    )
                )
            )

        if min_z2 < min_shared_z:
            shards.add(
                (
                    command2,
                    (
                        (min_shared_x, max_shared_x),
                        (min_shared_y, max_shared_y),
                        (min_z2, min_shared_z - 1)
                    )
                )
            )

        if max_shared_z < max_z2:
            shards.add(
                (
                    command2,
                    (
                        (min_shared_x, max_shared_x),
                        (min_shared_y, max_shared_y),
                        (max_shared_z + 1, max_z2)
                    )
                )
            )

        shards.add(
            (
                command1,
                (
                    (min(min_shared_x, min_x1), max(max_shared_x, max_x1)),
                    (min(min_shared_y, min_y1), max(max_shared_y, max_y1)),
                    (min(min_shared_z, min_z1), max(max_shared_z, max_z1))
                )
            )
        )

    for cube_remove in deletes:
        cubes.remove(cube_remove)

    for cube_add in shards:
        cubes.add(cube_add)

    if not c2_added:
        cubes.add(c1)


def getVolume(cube):
    _, x, y, z = cube[0], *cube[1]
    min_x, max_x, min_y, max_y, min_z, max_z = *x, *y, *z
    return abs(max_x - min_x + 1) * abs(max_y - min_y + 1) * abs(max_z - min_z + 1)


def main():
    test = 'test.txt'
    puzzle = 'input.txt'

    file = open(puzzle, 'r')

    instructions = []
    cubes = set()
    for line in file.readlines():
        command, positions = line.strip().split()
        x, y, z = positions.split(',')
        x = [int(x) for x in x.split('=')[-1].split('..')]
        y = [int(y) for y in y.split('=')[-1].split('..')]
        z = [int(z) for z in z.split('=')[-1].split('..')]

        cube = tuple(x), tuple(y), tuple(z)
        instructions.append((command, cube))

    count = 1
    for cube in instructions:
        print(f"processing {count} of {len(instructions)}")
        count += 1
        shard(cube, cubes)

    on_count = 0
    for cube in cubes:
        if cube[0] == 'on':
            on_count += getVolume(cube)

    printSolution(on_count)


if __name__ == "__main__":
    main()
