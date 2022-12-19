def printSolution(x):
    print(f"The solution is: {x}")


class Reindeer:
    def __init__(self, fly_speed, fly_time, rest_time):
        self.fly_time = fly_time
        self.fly_speed = fly_speed
        self.rest_time = rest_time
        self.cycle = fly_time + rest_time
        self.distance = 0
        self.time = 0

    def advanceTime(self, seconds):
        while seconds:
            if self.time % self.cycle < self.fly_time:
                self.distance += self.fly_speed
            self.time += 1
            seconds -= 1

    def __repr__(self):
        return f"Reindeer: time: {self.time}, distance: {self.distance}"


def main():

    race_time = 2503

    file = open("input.txt", "r")

    max_distance = 0
    for line in file:
        fly_speed, fly_time, rest_time = [int(x) for x in line.split() if x.isdigit()]
        reindeer = Reindeer(fly_speed, fly_time, rest_time)
        reindeer.advanceTime(race_time)
        max_distance = max(max_distance, reindeer.distance)

    printSolution(max_distance)


if __name__ == "__main__":
    main()
