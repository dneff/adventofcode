def printSolution(x):
    print(f"The solution is: {x}")


class Reindeer:
    def __init__(self, name, fly_speed, fly_time, rest_time):
        self.name = name
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
        return f"Reindeer: name: {self.name}, time: {self.time}, distance: {self.distance}"


def main():

    race_time = 2503

    file = open("input.txt", "r")

    racers = []
    scores = {}

    for line in file:
        fly_speed, fly_time, rest_time = [int(x) for x in line.split() if x.isdigit()]
        name = line.split()[0]
        racers.append(Reindeer(name, fly_speed, fly_time, rest_time))
        scores[name] = 0

    while race_time:
        for deer in racers:
            deer.advanceTime(1)
        distances = [r.distance for r in racers]
        farthest = max(distances)
        for idx, distance in enumerate(distances):
            if distance == farthest:
                scores[racers[idx].name] += 1
        race_time -= 1

    printSolution(max(scores.values()))


if __name__ == "__main__":
    main()
