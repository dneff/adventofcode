def printSolution(x):
    print(f"The solution is: {x}")


def handshake(subject_number, loop_size):
    result = subject_number
    modulus = 20201227
    for _ in range(loop_size):
        result = (result * subject_number) % modulus
    return result


def findLoopSize(seed, modulus, target):
    x = seed
    loop_count = 0
    while x != target:
        loop_count += 1
        x = (x * seed) % modulus
    return loop_count


def main():
    modulus = 20201227
    seed = 7

    file = open("input.txt", "r")

    door_pubkey = int(file.readline().strip())
    door_loopsize = findLoopSize(seed, modulus, door_pubkey)

    card_pubkey = int(file.readline().strip())
    card_loopsize = findLoopSize(seed, modulus, card_pubkey)

    assert handshake(card_pubkey, door_loopsize) == handshake(door_pubkey, card_loopsize)

    printSolution(handshake(card_pubkey, door_loopsize))


if __name__ == "__main__":
    main()
