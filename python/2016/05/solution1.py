import string
import hashlib

def printSolution(x):
    print(f"The solution is: {x}")

def main():
    seed = 'abbhdwsy'
    index = 0
    hashed = []
    while len(hashed) < 8:
        h = hashlib.md5()
        h.update(str.encode(seed+str(index)))
        out = str(h.hexdigest())
        if out[:5] == '00000':
            hashed.append(out[5])
            print(".",)
        index += 1
    
    printSolution(''.join(hashed))

if __name__ == "__main__":
    main()