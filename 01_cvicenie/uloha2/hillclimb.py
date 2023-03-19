import random

dir_dict = {'U': (0, 1), 'D': (0, -1), 'L': (-1, 0), 'R': (1, 0)}

class HillClimb:
    def __init__(self, position, n_gold, golds):
        self.position = position
        self.n_gold = n_gold
        self.g_positions = golds
        self.n_steps = 10
        self.grid = 10
        self.directions = ['U', 'D', 'L', 'R']

    def eval_fitness(self, route):
        # TODO define the fitness function
        reward = 0
        g_collected = []

        cur_pos = self.position

        for dir in route:
            newx = (cur_pos[0] + dir_dict[dir][0]) % self.grid
            newy = (cur_pos[1] + dir_dict[dir][1]) % self.grid
            cur_pos = (newx, newy)

            # print(cur_pos, cur_pos in self.g_positions, not(cur_pos in g_collected))

            if (cur_pos in self.g_positions) and (cur_pos not in g_collected):
                reward += 1
                g_collected.append(cur_pos)

        # print(reward, self.g_positions)
        return reward

    def argmax(self, nb, max):
        max_reward = max
        ties = []

        for i in range(len(nb)):
            reward = self.eval_fitness(nb[i])

            if reward > max_reward:
                max_reward = reward
                ties = []
            
            if reward == max_reward:
                ties.append(i)
        
        # if everything is lower than current maximum
        if ties == []:
            return None

        return random.choice(ties)

    def neighbours(self, route):
        # TODO return all neighbours
        nb = []

        for i in range(self.n_steps):
            for new_dir in self.directions:
                new_route = route[:]
                if new_dir != new_route[i]:
                    new_route[i] = new_dir
                    nb.append(new_route)

        return nb

    def search(self, n_attempts):
        route = random.choices(self.directions, k = self.n_steps)
        # print(route)

        for att in range(n_attempts):
            # TODO implement hillclimb to search for the best route
            max_reward = 0

            while True:
                # print(route)
                
                nb = self.neighbours(route)

                max_idx = self.argmax(nb, max_reward)
                if max_idx == None:
                    print(f'Attempt {att+1}: Stucked at local maximum using route {route}, with reward {max_reward}')
                    break

                max_reward = self.eval_fitness(nb[max_idx])
                route = nb[max_idx]

                print(f'Attempt {att+1}: Best route is {route}, with reward {max_reward}')

                if self.eval_fitness(nb[max_idx]) == self.n_gold:
                    print(f'Foud global maximum at {att+1}. attempt.')
                    exit(0)


if __name__ == "__main__":
    f = open("data.txt", "r")

    data = f.readlines()
    data = [d.strip().split() for d in data]
    data = [[int(n) for n in d] for d in data]

    posit, num_g = tuple(data[0]), data[1][0]
    g_positions = list(map(tuple,data[2:]))

    print(posit, g_positions)

    HC = HillClimb(posit, num_g, g_positions)
    HC.search(10)
