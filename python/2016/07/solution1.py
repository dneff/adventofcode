import re


def printSolution(x):
    print(f"The solution is: {x}")


def hasABBA(s):
    for i in range(1, len(s)-2):
        if s[i] == s[i+1] and s[i-1] == s[i+2]:
            if s[i] != s[i-1]:
                return True
    return False


def main():

    support_tls = []
    file = open("input.txt", "r")

    for line in file:
        hypernet = []
        for s in re.findall("(\[\w*\])", line):
            if s[0] == '[':
                hypernet.append(s.strip('[]'))
        
        if any([hasABBA(s) for s in hypernet]):
            continue

        ip = []
        for s in re.split("\[|\]", line.strip()):
            if s not in hypernet:
                ip.append(s)
        if any([hasABBA(s) for s in ip]):
            pass
        else:
            continue
        support_tls.append(line.strip())
    
    printSolution(len(support_tls))


if __name__ == "__main__":
    main()
