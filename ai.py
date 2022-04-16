import numpy as np
from config import *
from dog import *
from sheep import *
import random


class Ai():
    def __init__(self, sheep, dog, screen):
        self.screen = screen
        self.dog = dog
        self.sheep = sheep
        self.fitness = 0

        self.vec_dog_sheep = self.sheep.position - self.dog.position
        self.vec_sheep_gate = TUNNEL_CENTRAL - self.sheep.position

        self.dist_dog_center = point_distance(self.dog.position, FENCE_CENTER)

        self.input = np.array(
            [[self.dog.direction.x, self.dog.direction.y, self.vec_dog_sheep.normalize().x,
              self.vec_dog_sheep.normalize().y, self.vec_sheep_gate.normalize().x,
              self.vec_sheep_gate.normalize().y, (self.dist_dog_center / (NORMALIZER / 2))]])
        self.weights1 = np.random.uniform(-0.5, 0.5, size=(NNET_HIDDEN, NNET_INPUTS))
        self.weights2 = np.random.uniform(-0.5, 0.5, size=(NNET_OUTPUTS, NNET_HIDDEN))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def get_outputs(self):
        inputs = self.input.T
        # print('inputy', inputs, sep='\n')
        hidden_inputs = np.dot(self.weights1, inputs)
        # print('hidden input', hidden_inputs, sep='\n')
        hidden_outputs = self.sigmoid(hidden_inputs)
        # print('hidden outputs', hidden_outputs, sep='\n')
        final_inputs = np.dot(self.weights2, hidden_outputs)
        # print('final inputs', final_inputs, sep='\n')
        final_outputs = self.sigmoid(final_inputs)
        # final_outputs = self.sigmoid(hidden_inputs)
        # print('final outputs', final_outputs, sep='\n')
        return final_outputs

    def get_max_output(self):
        outputs = self.get_outputs()
        return np.max(outputs)

    def get_max_output_index(self):
        outputs = self.get_outputs()
        return np.argmax(outputs)

    def move_dog1(self):
        outputs = self.get_outputs()

        if outputs[0] > 0.5:
            if self.dog.speed < 1.9:
                self.dog.speed += 0.2
        else:
            self.dog.speed = 0
        if outputs[1] > 0.6:
            self.dog.angle_speed = -4
        elif outputs[1] < 0.4:
            self.dog.angle_speed = 4

    def update(self):
        self.vec_dog_sheep = self.sheep.position - self.dog.position
        self.vec_sheep_gate = TUNNEL_CENTRAL - self.sheep.position

        self.input = np.array(
            [[self.dog.direction.x, self.dog.direction.y, self.vec_dog_sheep.normalize().x,
              self.vec_dog_sheep.normalize().y, self.vec_sheep_gate.normalize().x,
              self.vec_sheep_gate.normalize().y, (self.dist_dog_center / (NORMALIZER / 2))]])

    def modify_array(self, a):
        for x in np.nditer(a, op_flags=['readwrite']):
            if random.random() < MUTATION_WEIGHT_MODIFY_CHANCE:
                x[...] = np.random.random_sample() - 0.5

    def modify_array_slightly(self, a):
        for x in np.nditer(a, op_flags=['readwrite']):
            if random.random() < MUTATION_WEIGHT_MODIFY_CHANCE:
                if np.random.random_sample() - 0.5 > 0:
                    x[...] = x[...]*1.1
                if np.random.random_sample() - 0.5 < 0 or x[...] > 0.5:
                    x[...] = x[...]*0.9
            elif random.random() < MUTATION_WEIGHT_LOW_MODIFY_CHANCE:
                x[...] = np.random.random_sample() - 0.5

    def get_mix_from_arrays(self, ar1, ar2):
        total_entries = ar1.size
        num_rows = ar1.shape[0]
        num_cols = ar1.shape[1]

        num_to_take = total_entries - int(total_entries * MUTATION_ARRAY_MIX_PERC)
        idx = np.random.choice(np.arange(total_entries), num_to_take, replace=False)

        res = np.random.rand(num_rows, num_cols)

        for row in range(0, num_rows):
            for col in range(0, num_cols):
                index = row * num_cols + col
                if index in idx:
                    res[row][col] = ar1[row][col]
                else:
                    res[row][col] = ar2[row][col]

        return res

    def modify_weights(self):
        self.modify_array(self.weights1)
        self.modify_array(self.weights2)

    def modify_weights_slightly(self):
        self.modify_array_slightly(self.weights1)
        self.modify_array_slightly(self.weights2)

    def create_mixed_weights(self, net1, net2):
        self.weights1 = self.get_mix_from_arrays(net1.weights1, net2.weights1)
        self.weights2 = self.get_mix_from_arrays(net1.weights2, net2.weights2)

    @staticmethod
    def create_offspring(p1, p2, screen):
        sheep = Sheep(screen, FENCE_CENTER.x + 60, FENCE_CENTER.y + 40, [])
        dog = Dog(FENCE_CENTER)
        new_ai = Ai(sheep, dog, screen)
        new_ai.create_mixed_weights(p1, p2)
        return new_ai


class AiCollection():
    def __init__(self, dogs, sheeps, screen):
        self.screen = screen
        self.dogs = dogs
        self.sheeps = sheeps
        self.ais = []
        self.create_new_gen(dogs, sheeps)

    def create_new_gen(self, dogs, sheeps):
        self.ais = []
        for i in range(0, GEN_SIZE):
            self.ais.append(Ai(sheeps[i], dogs[i], self.screen))

    def evolve_population(self, dogs, sheeps):
        s_counter = 0
        d_counter = 0

        # for ai in self.ais:
            # print('fitness before:', ai.fitness)
        # print('-')
        for ai in self.ais:
            if ai.sheep.done:
                ai.fitness = NORMALIZER + NORMALIZER
            else:
                ai.fitness = NORMALIZER - math.sqrt((ai.vec_sheep_gate.x ** 2) + (ai.vec_sheep_gate.y ** 2))

        self.ais.sort(key=lambda x: x.fitness, reverse=True)

        cut_off = int(len(self.ais) * MUTATION_CUT_OFF)
        good_ais = self.ais[0:cut_off]
        bad_ais = self.ais[cut_off:]
        num_bad_to_take = int(len(self.ais) * MUTATION_BAD_TO_KEEP)

        for ai in bad_ais:
            ai.modify_weights()

        ais = []

        # good to stay
        for good_ai in good_ais:
            good_ai.dog = dogs[d_counter]
            good_ai.sheep = sheeps[s_counter]
            d_counter += 1
            s_counter += 1

        ais.extend(good_ais)

        # bad after modify to stay
        idx_bad_to_take = np.random.choice(np.arange(len(bad_ais)), num_bad_to_take, replace=False)
        for index in idx_bad_to_take:
            bad_ais[index].dog = dogs[d_counter]
            bad_ais[index].sheep = sheeps[s_counter]
            ais.append(bad_ais[index])
            d_counter += 1
            s_counter += 1

        # good after mutation to stay
        best_to_mutation = int(len(self.ais) * MUTATION_BEST_TO_MUTE_PERC)
        for i in range(int(best_to_mutation)):
            idx_to_mutation = np.random.choice(np.arange(len(good_ais)), 1, replace=False)
            new_ai = Ai.create_offspring(good_ais[idx_to_mutation[0]], good_ais[idx_to_mutation[0]], self.screen)
            new_ai.modify_weights_slightly()
            new_ai.dog = dogs[d_counter]
            new_ai.sheep = sheeps[s_counter]
            ais.append(new_ai)
            d_counter += 1
            s_counter += 1

        # offspring
        while len(ais) < len(self.ais):
            idx_to_breed = np.random.choice(np.arange(len(good_ais)), 2, replace=False)
            if idx_to_breed[0] != idx_to_breed[1]:
                new_ai = Ai.create_offspring(good_ais[idx_to_breed[0]], good_ais[idx_to_breed[1]], self.screen)
                if random.random() < MUTATION_MODIFY_CHANCE_LIMIT:
                    new_ai.modify_weights()
                new_ai.dog = dogs[d_counter]
                new_ai.sheep = sheeps[s_counter]
                ais.append(new_ai)
                d_counter += 1
                s_counter += 1

        for ai in ais:
            pass
            #print('fitness after:', ai.fitness)
        #print('-')
        #print('best weights1v1:', self.ais[0].weights1)
        #print('best weights2v1:', self.ais[0].weights2)
        #print('best weights1v2:', self.ais[1].weights1)
        #print('best weights2v2:', self.ais[1].weights2)
        #print('--------------')
        self.ais = ais
