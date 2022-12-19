import unittest
from IntCode import IntCode, OutputInterrupt

class IntCodeTests(unittest.TestCase):

    def test_output_func(self):
        t1 = "109, -1, 4, 1, 99" # outputs -1 
        comp = IntCode(t1)
        while not comp.complete:
            try:
                comp.run()
            except(OutputInterrupt):
                pass
        self.assertEqual(comp.pop(), -1)


        t2 = "109, -1, 104, 1, 99" # outputs 1
        comp = IntCode(t2)
        while not comp.complete:
            try:
                comp.run()
            except(OutputInterrupt):
                pass
        self.assertEqual(comp.pop(), 1)


        t3 = "109, -1, 204, 1, 99" # outputs 109
        comp = IntCode(t3)
        while not comp.complete:
            try:
                comp.run()
            except(OutputInterrupt):
                pass
        self.assertEqual(comp.pop(), 109)


    def test_base_adjust_func(self):
        t1 = "109, 1, 9, 2, 204, -6, 99" # outputs 204
        comp = IntCode(t1)
        while not comp.complete:
            try:
                comp.run()
            except(OutputInterrupt):
                pass
        self.assertEqual(comp.pop(), 204)

        t2 = "109, 1, 109, 9, 204, -6, 99" # outputs 204
        comp = IntCode(t2)
        while not comp.complete:
            try:
                comp.run()
            except(OutputInterrupt):
                pass
        self.assertEqual(comp.pop(), 204)

        t3 = "109, 1, 209, -1, 204, -106, 99" # outputs 204
        comp = IntCode(t3)
        while not comp.complete:
            try:
                comp.run()
            except(OutputInterrupt):
                pass
        self.assertEqual(comp.pop(), 204)

    def test_input_func(self):
        t1 = "109, 1, 3, 3, 204, 2, 99" # outputs input
        input = 999
        comp = IntCode(t1)
        comp.push(input)
        while not comp.complete:
            try:
                comp.run()
            except(OutputInterrupt):
                pass
        self.assertEqual(comp.pop(), input)

        t2 = "109, 1, 203, 2, 204, 2, 99" # outputs input
        input = 999
        comp = IntCode(t2)
        comp.push(input)
        while not comp.complete:
            try:
                comp.run()
            except(OutputInterrupt):
                pass
        self.assertEqual(comp.pop(), input)


if __name__ == "__main__":
    unittest.main(verbosity=2)