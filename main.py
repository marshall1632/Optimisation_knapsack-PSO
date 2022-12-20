import sys

from PSDelivery import Particle_swarm_optimization
import math


Name = []
kg = []
value = []
maxKg = []


def run_assignment(filepath):
    try:
        with open(filepath) as file:
            temp = file.readline()
            while temp != '***\n':
                temp = file.readline()
            quota = int(file.readline())
            maxKg.append(quota)
            lines = file.readlines()
            count = 1
            for line in range(len(lines)):
                if lines[line] == "***\n":
                    print("\n*******************Problem number : ", count, "*******************\n")
                    solution(Name, kg, maxKg[0], value)
                    count += 1
                    continue
                s = lines[line].split()
                if len(s) == 3:
                    col = s[0].strip()
                    col2 = int(s[1].strip())
                    col3 = int(s[2].strip())
                    Name.append(col)
                    kg.append(col2)
                    value.append(col3)
            print("Names of boxes: ", Name)
            print("Boxes weight: ", kg)
            print("Boxes worth: ", value)
            print("Vehicle capacity: ", maxKg)
            print("\n*******************Problem number : ", count, "*******************\n")
            solution(Name, kg, maxKg[0], value)
    except FileNotFoundError:
        print("The file does not exist\n")
        input("Press enter to exit-- ")
        sys.exit()


# the cost_function we are trying to optimize (maximize)
def Opt_function(x):
    t = value_function(x)
    return t + kilogram_function(x, t)


# cost_function to maximize the values of the boxes
def value_function(x):
    total = 0
    for i in range(len(x)):
        total += x[i] * value[i]  # - * Boxes_value
    return total


# cost_function to maximize the weight of the boxes
def kilogram_function(x, rest_elements):
    total = 0
    for i in range(len(x)):
        total += x[i] * kg[i]

    if total <= maxKg[0]:
        if total <= rest_elements:
            return rest_elements - total
        else:
            return 0
    else:
        return -rest_elements


def solution(names, capacity, Vehicle_capacity, Boxes_value):
    # initializing the starting position
    print('[item_name: lower_bound - upper_bound]\n', sep='')
    initial_values = []
    Bounds_value = []
    for i in range(len(names)):
        initial_values.append(0)
        Bounds_value.append((initial_values[i], math.floor(Vehicle_capacity / capacity[i])))
        print(names[i], ': ', Bounds_value[i][0], ' - ', Bounds_value[i][1], sep='')
    print('\ntotal, including ', len(names), ' there is a variable...\n\n', sep='')

    pso = Particle_swarm_optimization(Opt_function, initial_values, Boxes_value, capacity, names, Bounds_value,
                                      number_of_particles=len(names), particles=100, max_iteration=50, get_steps=True)
    pso.print_results()
    pso.plotGraph(filename='test')
    pso.plotGraphError(filename='error')


if __name__ == '__main__':
    while True:
        file_name = input("Please enter file path and name : ")
        print()
        run_assignment(filepath=file_name)
        check = input("Do you want to continue (y|n) : ")
        if check != 'Y' and check != 'y':
            break
        print()
    input("Press enter to exit-- ")
