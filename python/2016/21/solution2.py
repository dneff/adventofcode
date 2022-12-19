from itertools import permutations

def printSolution(x):
    print(f"The solution is {x}")

class Scrambler():    
    def __init__(self, password):
        self.password = password
        self.data = []

    def load(self, filepath):
        fh = open(filepath, 'r')
        for l in fh:
            inst = l.strip().split(' ')
            if inst[0] in ['move', 'reverse']:
                method = inst[0]
            else:
                method = '_'.join([inst[0], inst[1]])
            method = method.replace('based', 'position')
            args = []
            for a in [inst[2], inst[-1]]:
                if len(a) == 1:
                    if a.isdigit():
                        args.append(int(a))
                    else:
                        args.append(a)
            self.data.append((method, args))

    def compile(self):
        for i in self.data:
            method, args = i
            step = getattr(self, method)
            step(*args)

    def swap_position(self, a, b):
        # letters at indexes X and Y (counting from 0) should be swapped
        x = min(a,b)
        y = max(a,b)
        x_letter = self.password[x]
        y_letter = self.password[y]
        self.password = self.password[:x] + y_letter + self.password[x+1:y] + x_letter + self.password[y+1:]


    def swap_letter(self, x, y):
        # the letters X and Y should be swapped
        self.password = self.password.replace(x, '_1_')
        self.password = self.password.replace(y, '_2_')
        self.password = self.password.replace('_1_', y)
        self.password = self.password.replace('_2_', x)


    def rotate_left(self, x):
        # the whole string should be rotated
        x = x % len(self.password)
        self.password = self.password[x:] + self.password[:x]


    def rotate_right(self, x):
        # the whole string should be rotated
        x = x % len(self.password)
        self.password = self.password[-x:] + self.password[:-x]


    def rotate_position(self, x):
        # the whole string should be rotated to the right 
        # based on the index of letter X (counting from 0) 
        # as determined before this instruction does any 
        # rotations. Once the index is determined, rotate 
        # the string to the right one time, plus a number 
        # of times equal to that index, plus one additional 
        # time if the index was at least 4.
        idx = self.password.find(x)
        if idx >= 4:
            idx += 1
        idx +=1
        self.rotate_right(idx)
        

    def reverse(self, a, b):
        # the span of letters at indexes X through Y 
        # (including the letters at X and Y) should be 
        # reversed in order.
        x, y = min(a, b), max(a, b)
        self.password = self.password[:x] + ''.join(list(reversed(self.password[x:y+1]))) + self.password[y+1:]


    def move(self, x, y):
        # the letter which is at index X should be 
        # removed from the string, then inserted such 
        # that it ends up at index Y.
        letter_x = self.password[x]
        self.password = self.password[:x] + self.password[x+1:]
        self.password = self.password[:y] + letter_x + self.password[y:]
    

def main():

    test = {
        'pwd': 'abcde',
        'file': 'test.txt'
    }

    puzzle = {
        'pwd': 'abcdefgh',
        'file': 'input.txt'
    }

    active = puzzle

    scram = Scrambler('')
    scram.load(active['file'])

    scrambled = 'fbgdceah'

    for pwd in permutations(scrambled):
        pwd = ''.join(pwd)
        scram.password = pwd
        scram.compile()

        if scram.password == scrambled:
            printSolution(pwd)
            break


if __name__ == "__main__":
    main()