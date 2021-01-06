import json

def printSolution(x):
    print(f"The solution is: {x}")


def getValue(data):
    result = 0
    if isinstance(data, str) or isinstance(data, int):
        try:
            return int(data)
        except ValueError:
            pass
    elif isinstance(data, list):
        for d in data:
            result += getValue(d)
    elif isinstance(data, dict):
        for d in data.values():
            result += getValue(d)

    return result


def main():

    file = open("input.txt", "r")

    json_data = file.read()
    data = json.loads(json_data)

    printSolution(getValue(data))


if __name__ == "__main__":
    main()
