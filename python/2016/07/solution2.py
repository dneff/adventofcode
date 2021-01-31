import re


def printSolution(x):
    print(f"The solution is: {x}")


def getABA(s):
    aba = []
    for i in range(1, len(s)-1):
        if s[i-1] == s[i+1] and s[i-1] != s[i]:
            aba.append(s[i-1:i+2])
    return aba


def invertABA(s):
    return s[1] + s[0] + s[1]


def main():

    support_ssl = []
    file = open("input.txt", "r")

    for line in file:
        hypernet = []
        for s in re.findall("(\[\w*\])", line):
            if s[0] == '[':
                hypernet.append(s.strip('[]'))
        
        abas  = []
        for h in hypernet:
            abas.extend(getABA(h))

        if len(abas) == 0:
            continue

        babs = [invertABA(x) for x in abas]

        ssl_match = []
        for s in re.split("\[|\]", line.strip()):
            if s in hypernet:
                continue
            if len(ssl_match) == 0:
                for bab in babs:
                    if bab in s:
                        ssl_match.append(s)
                        support_ssl.append(line.strip())
                        break
    
    printSolution(len(set(support_ssl)))
    

if __name__ == "__main__":
    main()
