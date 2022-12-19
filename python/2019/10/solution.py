import math

def getAngle(base, asteroid):
    #return r, theta(degrees)
    x = asteroid[0] - base[0]
    y = asteroid[1] - base[1] 
    r = (x ** 2 + y**2) ** .5
    theta = (math.degrees(math.atan2(y, x)) + 90) % 360
    #theta = (360 - theta) % 360

    return round(r, 3), round(theta, 3)

def main():
    with open('input1.txt', 'r') as file:
        data = file.readlines()

    map = []
    for r, line in enumerate(data):
        for c, val in enumerate(line):
            if val == '#':
                map.append((c,r))
    max_base = (0,0)
    max_sight = 0

    for base in map:
        angles = {}
        for a in map:
            if base == a:
                continue
            r,d = getAngle(base, a)
            angles[d] = a
        if len(angles.keys()) > max_sight:
            max_base = base
            max_sight = len(angles.keys())
    print(f"Solution 1:\nBase {max_base} can see {max_sight} asteroids.")

    sited = {}
    for a in map:
        if max_base == a:
            continue
        r,d = getAngle(max_base, a)
        if d not in sited.keys():
            sited[d] = (a[0], a[1], r)
        else:
            if abs(r) < abs(sited[d][2]):
                sited[d] = (a[0], a[1], r)

    shoot_order = list(sited.keys())    
    shoot_order.sort()
    result = sited[shoot_order[199]]
    print("Solution 2:")
    print(f"The 200th asteroid destroyed is {result}\n\t at angle {shoot_order[199]}\n\t with code value of {result[0] * 100 + result[1]}")

if __name__ == "__main__":
    main()
