import string
import hashlib

def printSolution(x):
    print(f"The solution is: {x}")

def main():
    seed = 'abbhdwsy'
    index = 0
    hashed = ['_'] * 8
    while '_' in hashed:
        h = hashlib.md5()
        h.update(str.encode(seed+str(index)))
        out = str(h.hexdigest())
        if out[:5] == '00000':
            try:
                position = int(out[5])
                if position < 8 and hashed[position] == '_':
                    hashed[position] = out[6]
                print(".",)
            except ValueError:
                pass
        index += 1
    
    printSolution(''.join(hashed))

if __name__ == "__main__":
    main()