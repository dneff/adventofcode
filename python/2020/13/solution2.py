from collections import defaultdict

def printSolution(x):
    print(f"The solution is: {x}")

# today I learned about Chinese Remainder Theorem
def CRT(mod_values):
    remainders = [x[0] for x in mod_values]
    modulus = [x[1] for x in mod_values]
    mod_product = 1
    for x in modulus:
        mod_product *= x

    N_mods = [int(mod_product/x) for x in modulus]

    N_inverse = []
    for i in range(len(N_mods)):
        N_inverse.append(pow(N_mods[i], -1, modulus[i]))

    products = 0
    # find inverse of N_mods * N_inverse * remainder
    for i in range(len(N_mods)):
        products += N_mods[i] * N_inverse[i] * remainders[i]
    return products % mod_product


def main():
    file = open("input.txt", "r")
    file.readline()

    schedule = [int(x) if x != "x" else 0 for x in file.readline().split(",")]

    offsets = {}
    for i, bus in enumerate(schedule):
        if bus == 0:
            continue
        # huh -- didn't expect this to be negative...
        offsets[-i] = bus

    buses = [x for x in schedule if x != 0]

    printSolution(CRT([(x, m) for x, m in offsets.items()]))


if __name__ == "__main__":
    main()