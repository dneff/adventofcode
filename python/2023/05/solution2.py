"""solves advent of code 2023 day 5 part 1"""

def print_solution(x):
    """prints solution"""
    print(f"The solution for 05.1: {x}")

def get_mapping(seed, mappings):
    """
    mapping is three number sets: destination start, source start, range length
    seed is a number
    if the seed is in the destination start range, return the corresponding destination value
    else return the seed
    """
    for mapping in mappings:
        dest_start, source_start, length = mapping
        if source_start <= seed <= source_start + length:
            offset = seed - source_start
            return dest_start + offset
    return seed

def get_seed_location(seed, almanac):
    """returns the location of the seed"""
    soil = get_mapping(seed, almanac['seed-to-soil map'])
    fertilizer = get_mapping(soil, almanac['soil-to-fertilizer map'])
    water = get_mapping(fertilizer, almanac['fertilizer-to-water map'])
    light = get_mapping(water, almanac['water-to-light map'])
    temperature = get_mapping(light, almanac['light-to-temperature map'])
    humidity = get_mapping(temperature, almanac['temperature-to-humidity map'])
    location = get_mapping(humidity, almanac['humidity-to-location map'])

    return location

def main():
    """main function"""
    filename = "./python/2023/input/05.txt"
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    seed_ranges = [int(x) for x in lines[0].split(":")[1].strip().split()]

    almanac = {}
    key = ''
    for line in lines[1:]:
        if line == '':
            continue
        if line[0].isalpha():
            key = line.split(":")[0]
            almanac[key] = []
        else:
            almanac[key].append([int(x) for x in line.strip().split()])

    lowest_location = get_seed_location(seed_ranges[0], almanac)

    print(f"seed range count: {len(seed_ranges)//2}")
    for i in range(0, len(seed_ranges), 2):
        print(f"seed range: {seed_ranges[i]} to {seed_ranges[i] + seed_ranges[i+1]}")
        start, offset = seed_ranges[i], seed_ranges[i+1]
        for seed in range(start, start + offset):
            location = get_seed_location(seed, almanac)
            lowest_location = min(location, lowest_location)

    # solution is lowest location
    print_solution(lowest_location)

if __name__ == "__main__":
    main()
