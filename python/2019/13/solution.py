from IntCode import IntCode, OutputInterrupt, InputInterrupt


def main():
    with open('input1.txt', 'r') as file:
        program = file.read().strip()

    comp1 = IntCode(program)

    screen = {}

    while not comp1.complete:
        try:
            comp1.run()
        except(OutputInterrupt):
            if len(comp1.output) == 3:
                x, y, id = comp1.output
                screen[(x, y)] = id

                comp1.output.clear()

    block_count = len([x for x in screen.values() if x == 2])        

    print(f"Solution 1: The block count on exit is: {block_count}")

#-=-=-- Part 2

    def joystickTilt(ball, paddle):
        j_tilt = 0
        if ball[0] < paddle[0]:
            j_tilt -= 1
        elif ball[0] > paddle[0]:
            j_tilt += 1
        return j_tilt
    
    ball = (0, 0)
    paddle = (0, 0)
    score = 0

    comp2 = IntCode(program)
    comp2.memory[0] = 2

    screen = {}

    while not comp2.complete:
        try:
            comp2.run()
        except(InputInterrupt):
            comp2.push(joystickTilt(ball, paddle))
        except(OutputInterrupt):
            if len(comp2.output) == 3:
                x, y, id = comp2.output

                if (x, y) == (-1, 0):
                    score = id
                elif id == 3:
                    paddle = (x, y)
                elif id == 4:
                    ball = (x, y)

                screen[(x, y)] = id

                comp2.output.clear()


    print(f"Solution 2: The final score is {score}") 

if __name__ == "__main__":
    main()