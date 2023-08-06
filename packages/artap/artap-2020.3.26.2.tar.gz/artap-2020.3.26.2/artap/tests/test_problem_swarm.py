import unittest
from artap.problem import Problem
from artap.algorithm_swarm import PSO, PSO_V1
from artap.results import Results

import optproblems as optp
import optproblems.cec2005 as cec2005


class CEC2005_TEST_Problems(Problem):
    """
    Template class to initialize the different test problems these problems working for 2, 10, 30 variables.

    There are 25 test problems, which were compiled for the Special Session on Real-Parameter Optimization at the
    Congress on Evolutionary Computation (CEC), Edinburgh, UK, 2-5 Sept. 2005. The mathematical definitions are given in
    [Suganthan2005]. Additionally, implementations in C, Java, and Matlab were provided for the participants.
    Artap uses the optproblems test library to run these test. This template class is made to invoke them.
    """

    def set(self):
        # two variables
        self.parameters = [{'name': 'x_1', 'bounds': [func.min_bounds[0], func.max_bounds[0]]},
                           {'name': 'x_2', 'bounds': [func.min_bounds[1], func.max_bounds[1]]}]

        self.costs = [{'name':'F_1'}]


    def evaluate(self, x):
        problem = optp.Problem(func, num_objectives=1)
        solutions = [optp.Individual(x.vector)]

        problem.batch_evaluate(solutions)

        return [solutions[0].objective_values]


class TestCEC2005(unittest.TestCase):
    """Tests from CEC2005 library"""

    def run_test_problem(self, nr_gen, function):
        try:
            global func
            func = function
            problem = CEC2005_TEST_Problems()
            algorithm = PSO(problem)
            algorithm.options['max_population_number'] = nr_gen
            algorithm.options['max_population_size'] = 100
            algorithm.run()

            b = Results(problem)
            optimum = b.find_minimum('F_1')  # Takes last cost function
            self.assertAlmostEqual(optimum.costs[0], func.bias, 0)
            del func
        except AssertionError:
            # try again with more populations
            max_pop = int(1.5 * nr_gen)
            # print("Try again with more populations: {}".format(max_pop))
            self.run_test_problem(max_pop, function)

    def test_shifted_sphere(self):
        self.run_test_problem(50, optp.cec2005.F1(2))

    #def test_shifted_double_sum(self):
    #    self.run_test_problem(500, optp.cec2005.F2(2))

    #def test_schwefel(self):  # !
    #    self.run_test_problem(400, optp.cec2005.F5(2))

    # the success rate is about 80% reference  Maurice Clerc - A method to improve PSO
    #def test_shifted_rosenbrock(self):
    #    self.run_test_problem(100, optp.cec2005.F6(2))

    # no bounds
    #def test_shifted_griewank(self):
    #    self.run_test_problem(50,  optp.cec2005.F7(2))

    # def test_shifted_ackley(self):
    #   self.run_test_problem(50,  optp.cec2005.F8(2))

    #def test_shifted_griewank(self):
    #   self.run_test_problem(50,  optp.cec2005.F7(2))

    #def test_shifted_rastrigin(self):
    #    self.run_test_problem(50,  optp.cec2005.F9(2))

    def test_shifted_rot_weierstrass(self):
        self.run_test_problem(50, optp.cec2005.F11(2))

    def test_fletcherpowell(self):  # schwefel
        self.run_test_problem(50, optp.cec2005.F12(2))

    def test_f8f2(self):
        self.run_test_problem(50, optp.cec2005.F13(2))

    def test_expanded_f6(self):
        self.run_test_problem(50, optp.cec2005.F14(2))

    # def test_hybrid_composition(self):
    #     self.run_test_problem(50,  optp.cec2005.F15(2))

    # def test_rotated_f15(self):
    #     self.run_test_problem(50,  optp.cec2005.F16(2))

    # def test_f17_with_noise(self):
    #     self.run_test_problem(2000, optp.cec2005.F17(2))


class TestCEC2005_v1(unittest.TestCase):
    """Tests from CEC2005 library"""

    def run_test_problem(self, nr_gen, function):
        try:
            global func
            func = function
            problem = CEC2005_TEST_Problems()
            algorithm = PSO_V1(problem)
            algorithm.options['max_population_number'] = nr_gen
            algorithm.options['max_population_size'] = 100
            algorithm.run()

            b = Results(problem)
            optimum = b.find_minimum('F_1')  # Takes last cost function
            self.assertAlmostEqual(optimum.costs[0], func.bias, 0)
            del func
        except AssertionError:
            # try again with more populations
            max_pop = int(1.5 * nr_gen)
            # print("Try again with more populations: {}".format(max_pop))
            self.run_test_problem(max_pop, function)

    def test_shifted_sphere(self):
        self.run_test_problem(50, optp.cec2005.F1(2))


if __name__ == '__main__':
    unittest.main()
