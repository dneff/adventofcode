from itertools import permutations
from IntCode import IntCode, InputInterrupt, OutputInterrupt


def main():
    with open('input1.txt', 'r') as file:
        program = file.read().strip()


    max_thrust = 0
    phases = [x for x in range(5)]
    for phase_order in list(permutations(phases, len(phases))):
        thrust = 0
        for phase in phase_order:
            comp = IntCode(program)
            comp.push(phase)
            comp.push(thrust)
            try:
                comp.run()
            except(OutputInterrupt):
                pass

            thrust = comp.pop()

        max_thrust = max(max_thrust, thrust)
    
    print(f"SOLUTION 1: The max thrust is {max_thrust}")

    max_thrust = 0
    phases = [x for x in range(5, 10)]
    for phase_order in list(permutations(phases, len(phases))):
        computers = []
        for phase in phase_order:
            computers.append(IntCode(program))
            computers[-1].push(phase)
        computers[0].push(0)

        i = -1
        while True:
            i = (i+1) % 5
            while not computers[i].complete:
                try:
                    computers[i].run()
                except(OutputInterrupt):
                    computers[(i+1)%5].push(computers[i].pop())
                    continue
                except(InputInterrupt):
                    break
            
            if(all(map(lambda x: x.complete, computers))):
                break
    
        max_thrust = max(max_thrust, computers[0].input[-1])

    print(f"SOLUTION 2: The max thrust is {max_thrust}")

if __name__ == "__main__":
    main()
