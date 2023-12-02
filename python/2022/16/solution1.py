from collections import deque
from itertools import permutations
from math import factorial


def print_solution(x):
    """
    prints input as solution
    """
    print(f"The solution is {x}")


def generate_rooms(file):
    """
    take input file and generate graph of rooms
    return dict of locations
    """
    graph = {}
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            room = line.split()[1]
            flow = line.split("=")[1].split(";")[0]
            flow = int(flow)
            tunnels = line.split("valve")[1].strip().strip("s ").split(", ")
            graph[room] = {"flow": flow, "tunnels": tunnels}

    return graph


def best_path(start, valve_cache, distance_cache, duration):
    """
    returns flow score for best path
    will time out after duration
    """
    best_score = 0
    best_time = 31
    queue = deque()

    # queue obj = ((path), remaining_time, flow, score)
    queue.append(((start,), duration, 0, 0))

    while queue:
        #print(len(queue))

        path, time, flow, score = queue.popleft()
        #if time > best_time and score < best_score:
        #   continue

        next_room = [x for x in valve_cache.keys() if x not in path]
        # end if no more rooms to visit
        if len(next_room) == 0:
            score += flow * time
            if best_score < score:
                best_score = score
                best_time = time
        for room in next_room:
            travel_time = distance_cache[(path[-1], room)]
            # end if out of time
            if time < travel_time:
                score += flow * time
                best_score = max(best_score, score)
                if score == 11703:
                    print(path)
                    
            else:
                next_path = path + (room,)
                next_time = time - travel_time
                next_flow = flow + valve_cache[room]
                next_score = score + (travel_time * flow)
                queue.append((next_path, next_time, next_flow, next_score))
                    
    return best_score

def breadth_search(start, end, rooms):
    """
    breadth_search: a BFS search, return length of shortest path
    """

    queue, seen = deque(), set()
    queue.append([start])

    while queue:
        path = queue.popleft()
        room = path[-1]

        if room not in seen:
            seen.add(room)
            if room == end:
                return len(path) - 1

            for location in rooms[room]["tunnels"]:
                new_path = path[:]
                new_path.append(location)
                queue.append(new_path)


def main():
    file = "../input/16.txt"
    rooms = generate_rooms(file)
    valve_rooms = [k for k, v in rooms.items() if v["flow"] > 0]

    start = "AA"

    duration = 30
    valve_cache = {}
    distance_cache = {}

    for room in valve_rooms:
        valve_cache[room] = rooms[room]["flow"]

    for pair in permutations(valve_rooms, 2):
        distance_cache[pair] = breadth_search(*pair, rooms) + 1
    for room in valve_rooms:
        distance_cache[("AA", room)] = breadth_search("AA", room, rooms) + 1

    best = best_path(start, valve_cache, distance_cache, duration)

    # 10874 high
    print_solution(best)


if __name__ == "__main__":
    main()
