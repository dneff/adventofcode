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
        if seed in range(source_start, source_start + length):
            offset = seed - source_start
            return dest_start + offset
    return seed


def main():
    """main function"""
    filename = "./python/2023/input/05.txt"
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    seeds = {int(x): {} for x in lines[0].split(":")[1].strip().split()}

    almanac = {}
    key = ""
    for line in lines[1:]:
        if line == "":
            continue
        if line[0].isalpha():
            key = line.split(":")[0]
            almanac[key] = []
        else:
            almanac[key].append([int(x) for x in line.strip().split()])

    for seed in seeds:
        seeds[seed]["soil"] = get_mapping(seed, almanac["seed-to-soil map"])
        seeds[seed]["fertilizer"] = get_mapping(
            seeds[seed]["soil"], almanac["soil-to-fertilizer map"]
        )
        seeds[seed]["water"] = get_mapping(
            seeds[seed]["fertilizer"], almanac["fertilizer-to-water map"]
        )
        seeds[seed]["light"] = get_mapping(
            seeds[seed]["water"], almanac["water-to-light map"]
        )
        seeds[seed]["temperature"] = get_mapping(
            seeds[seed]["light"], almanac["light-to-temperature map"]
        )
        seeds[seed]["humidity"] = get_mapping(
            seeds[seed]["temperature"], almanac["temperature-to-humidity map"]
        )
        seeds[seed]["location"] = get_mapping(
            seeds[seed]["humidity"], almanac["humidity-to-location map"]
        )

    # solution is lowest location
    solution = min([seeds[seed]["location"] for seed in seeds])
    print_solution(solution)


if __name__ == "__main__":
    main()
