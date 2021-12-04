from collections import defaultdict

def printSolution(x):
    print(f"The solution is {x}")

def getOxyRating(data, prefix = ''):
    if len(data) == 1:
        return data[0]

    prefix_size = len(prefix) + 1
    seperate = defaultdict(list)
    for d in data:
        seperate[str(d[:prefix_size])].append(d)

    kv_pairs = sorted(seperate.items(), key=lambda x: (len(x[1]), x[0]), reverse=True)
    return getOxyRating(kv_pairs[0][1], kv_pairs[0][0])


def getCO2Rating(data, prefix = ''):
    if len(data) == 1:
        return data[0]

    prefix_size = len(prefix) + 1
    seperate = defaultdict(list)
    for d in data:
        seperate[str(d[:prefix_size])].append(d)

    kv_pairs = sorted(seperate.items(), key=lambda x: (len(x[1]), x[0]))
    return getCO2Rating(kv_pairs[0][1], kv_pairs[0][0])

def main():
    file = open('input.txt', 'r')
    data = []
    for line in file.readlines():
        data.append(line.strip())

    oxy_rating = getOxyRating(data)
    co2_rating = getCO2Rating(data)

    #print(oxy_rating, co2_rating)
    printSolution(int(oxy_rating, 2) * int(co2_rating, 2))

if __name__ == "__main__":
    main()