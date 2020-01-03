

def processData(data, phases=1):
    
    base = [0, 1, 0, -1]
    
    result = []
    p_data = [int(x) for x in data]

    for _ in range(1, phases + 1):
        result = []
        for rounds in range(1, len(data) + 1):
            digit = 0
            for i, d in enumerate(p_data):
                base_pos = ((i + 1)//rounds) % len(base)
                digit +=  d * base[base_pos]
                #print(f"{d} * {base[base_pos]} = {d * base[base_pos]}")
            #print(f"digit: {digit} -> {abs(digit) % 10}")
            result.append(abs(digit) % 10)
        p_data = result[:]

    return "".join([str(x) for x in result])


def processDataP2(data, phases=100):
    full_data = data * 10000
    offset_idx = int(data[:7])
    trunc_data = full_data[offset_idx:]

    result = []
    p_data = [int(x) for x in trunc_data]

    for _ in range(1, phases + 1):
        result = [0] * len(p_data)
        result[-1] = p_data[-1]
        for idx in range(len(p_data) - 2, -1, -1):
            result[idx] = (p_data[idx] + result[idx+1]) % 10
        p_data = result[:]
    
    return "".join([str(x) for x in result])


def main():
    with open('input1.txt', 'r') as file:
        data = file.read().strip()

    #print(f"test: {processData('12345678', 4)} -> 01029498")
    #print(f"test: {processData('80871224585914546619083218645595', 100)[:8]} -> 24176176")
    #print(f"test: {processData('19617804207202209144916044189917', 100)[:8]} -> 73745418")
    #print(f"test: {processData('69317163492948606335995924319873', 100)[:8]} -> 52432133")
    print(f"Solution 1: The first eight digits of the final output list after 100 FFT phases is {processData(data, 100)[:8]}")

#Part 2 -=-=-

    # find 8 digits to transform
    # find base offset for those 8 digits
    # -=-=- key insight: final transform is 0....0, 1, penultimate is 0...1, 1, etc. work it backwards

    print(f"Solution 2: The eight-digit message is {processDataP2(data, 100)[:8]}")

if __name__ == "__main__":
    main()
