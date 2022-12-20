import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import random


class Particles:
    def __init__(self, initialValue):
        self.position = []
        self.speed = []
        self.individual_best = []
        self.error_of_best = -1
        self.individual_approach = -1

        for i in range(number_of_dimensions):
            self.speed.append(random.uniform(-1, 1))
            self.position.append(initialValue[i])

    # calculate fittness costfuntion
    def calculate_fitness(self, costfuntion):
        self.approach = costfuntion(self.position)

        # Check if your current position is your individual best...
        if self.approach > self.error_of_best or self.error_of_best == -1:
            self.individual_best = self.position
            self.error_of_best = self.approach

    #  Update new particle rate...
    def speed_update(self, group_best_position):
        w = 0.99  # The coefficient of the desire to maintain the previous velocity of the particle.
        c1 = 1.99  # The coefficient of the desire to protect one's own best.
        c2 = 1.99  # Coefficient of willingness to get the best Boxes_value of the herd.

        for i in range(number_of_dimensions):
            r1 = random.random()
            r2 = random.random()

            cognitive_speed = c1 * r1 * (self.individual_best[i] - self.position[i])
            social_speed = c2 * r2 * (group_best_position[i] - self.position[i])
            self.speed[i] = w * self.speed[i] + cognitive_speed + social_speed

    # Calculating new positions based on newly updated particle velocity...
    def position_update(self, Bounds):
        for i in range(number_of_dimensions):
            maxVelocity = (Bounds[i][1] - Bounds[i][0])

            if self.speed[i] < -maxVelocity:
                self.speed[i] = -maxVelocity
            elif self.speed[i] > maxVelocity:
                self.speed[i] = maxVelocity

            self.position[i] += self.speed[i]

            if self.position[i] > Bounds[i][1]:
                # If position is above the upper limit Boxes_value, pull to the upper limit Boxes_value
                self.position[i] = Bounds[i][1]
            elif self.position[i] < Bounds[i][0]:
                # If position is below the lower limit Boxes_value, pull to the lower limit Boxes_value
                self.position[i] = Bounds[i][0]
            else:
                self.position[i] = round(self.position[i])


class Particle_swarm_optimization:
    box_value = []
    box_names = []
    best_position_individual = []
    error_best = -1

    def __init__(self, function, Initial_Values, value, kg, names, Bounds_value, number_of_particles, particles,
                 max_iteration,
                 get_steps=True):  # Opt_function, initialValue, Bounds, number_of_particles=7, max_iteration=0.1
        global number_of_dimensions

        number_of_dimensions = len(Initial_Values)
        self.error_best = -1  # Best approach for group
        self.best_position_individual = []  # Best position for group
        self.names = names
        self.value = value
        self.kg = kg
        self.max_iteration = max_iteration
        fitness = []
        # Let's assign initial values to our version...
        herd = []
        for i in range(particles):
            herd.append(Particles(Initial_Values))

        # Optimization cycle start...
        counter = 0
        while counter < max_iteration:
            # Calculation of the suitability of the particles in the swarm for the costfuntion...
            for j in range(particles):
                herd[j].calculate_fitness(function)


                # Checking whether the current thread is the global best and making the necessary updates

                if herd[j].approach > self.error_best or self.error_best == -1:
                    self.best_position_individual = list(herd[j].position)
                    fitness = list(herd[j].position)
                    self.error_best = float(herd[j].approach)



            # Updating speeds and positions in the herd...
            for j in range(particles):
                herd[j].speed_update(self.best_position_individual)
                herd[j].position_update(Bounds_value)

            total_profit = 0
            totalKG = 0
            # loop swarm and update velocities and position
            for i in range(number_of_particles):
                total_profit += self.best_position_individual[i] * self.value[i]
                totalKG += self.best_position_individual[i] * self.kg[i]
            self.box_value.append(total_profit)
            self.box_names.append(totalKG)

            if get_steps:
                print(self.best_position_individual)
            counter += 1
        print("fitness",fitness)

    # Printing the results...
    def print_results(self):
        print('\n\nRESULTS:\n\n')
        totalProfit = 0
        totalKG = 0
        for i in range(len(self.best_position_individual)):
            print(self.names[i], ': ', self.best_position_individual[i], ' chosen', sep='')
            totalProfit += self.best_position_individual[i] * self.value[i]
            totalKG += self.best_position_individual[i] * self.kg[i]
        print('#' * 50, '\nProfit: ', totalProfit, ',\nKilogram: ', totalKG, sep='')

    # Plot the results to the screen [If we do not want to save the result image to the computer, the parameter named
    # 'fileName' must be empty!]...
    def plotGraph(self, filename=''):
        plt.plot(self.box_names, self.box_value)
        plt.xlabel('Kilogram (capacity)')
        plt.ylabel('Profit made')
        plt.title('Profit by Results - Kilogram Chart')
        plt.grid(True)

        if not (filename == ''):
            plt.savefig(filename)

        plt.show()
        plt.close()

    def plotGraphError(self, filename=''):
        plt.plot(self.max_iteration)
        plt.xlabel('Iteration')
        plt.ylabel('Error')
        plt.title('Error vs iteration')
        plt.grid(True)

        if not (filename == ''):
            plt.savefig(filename)

        plt.show()
        plt.close()
