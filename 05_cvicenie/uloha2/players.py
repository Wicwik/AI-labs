import random
from games import TicTacToe, Gomoku
import numpy as np
import copy

################################### PLAYERS ###################################

class Player:
    def choose_move(self, game, state):
        raise NotImplementedError



class AskingPlayer(Player):
    def choose_move(self, game, state):
        # Asks user (human) which move to take. Useful for debug.
        actions = game.actions(state)
        print("Choose one of the following positions: {}".format(actions))
        game.display_state(state, True)
        return int(input('> '))



class RandomPlayer(Player):
    def choose_move(self, game, state):
        # Picks random move from list of possible ones.
        return random.choice(game.actions(state))

class Node:
    '''
    Structure to simplify the tree search
    '''

    def __init__(self, state, parent=None) -> None:
        self.state = state
        self.parent = parent
        self.children = []
        self.n = 0
        self.value = 0

    def __str__(self) -> str:
        return f'state:{self.state} visited: {self.n}, value: {self.value}'

    def add_child(self, child_node):
        self.children.append(child_node)

    def update(self, result):
        self.n += 1
        self.value += result

    def uct(self):
        # Constatnt c is 2 as recommended by slides
        return self.value / self.n + 2*np.sqrt(np.log(self.parent.n) / self.n) if self.n > 0 else np.inf

def mcts(game, state, max_iter=10):
    # This is the root node from which we are searching
    root = Node(state)

    for _ in range(max_iter):
        # In each iteration we start from the root node
        current_node = root

        # Selection
        # We want to expand a node with the highies uct, so we iterate over the nodes highiest uct until we found one that is not expanded 
        while not game.is_terminal(current_node.state) and current_node.children:
            current_node = max(current_node.children, key=lambda child: child.uct())

        # Expansion
        # Now we want to expand the selected node by generating its neighboring states from available actions
        # After that, we chose randomly (uniformly) from the generated child nodes
        if not game.is_terminal(current_node.state):
            actions = game.actions(current_node.state)

            for action in actions:
                child_state = game.state_after_move(current_node.state, action)
                child_node = Node(child_state, parent=current_node)
                current_node.add_child(child_node)

                # If we found terminal state child we can go right to the backpropagation
                if game.is_terminal(child_state):
                    break

            current_node = random.choice(current_node.children)

        # Simulation / Rollout
        # Now we want to randomly descend to the leaf of the tree
        current_state = current_node.state
        while not game.is_terminal(current_state):
            current_state = game.state_after_move(current_state, random.choice(game.actions(current_state)))

        # Backpropagation
        # When we are at the leaf of the tree we can propagate up to the root and update each node along the way value based on the result
        my_player = game.player_at_turn(state)
        result = game.utility(current_state, my_player)
        while current_node:
            current_node.update(result)
            current_node = current_node.parent
            result = result

    # When we are done searching we just return the child of root that was visited the most, which means that under this node is the winning state with higiest probablity
    return max(root.children, key=lambda child: child.n).state



class MCTSearchPlayer(Player):
    def choose_move(self, game, state):
        '''
        We start from the current state and compute mcts each time before we take any action
        The more iterations we take, the bigger the probability of choosing the optimal move
        100 iters had over 90% win rate against random player
        '''
        probably_next_best_state = mcts(game, state, max_iter=100)
        probably_best_action = None

        # once we got the state, we just need to find the right action
        for action in game.actions(state):
            if game.state_after_move(state, action) == probably_next_best_state:
                probably_best_action = action

        return probably_best_action



################################ MAIN PROGRAM #################################

if __name__ == '__main__':
    ## Print all moves of the game? Useful for debugging, annoying if it`s already working.
    show_moves = True

    # Testing/comparing the performances. Uncomment/

    # TicTacToe().play([RandomPlayer(), AskingPlayer()], show_moves=show_moves)
    # TicTacToe().play([MCTSearchPlayer(), AskingPlayer()], show_moves=show_moves)
    # TicTacToe().play([MCTSearchPlayer(), RandomPlayer()], show_moves=show_moves)

    TicTacToe().play_n_games([MCTSearchPlayer(), RandomPlayer()], n=100)
    TicTacToe().play_n_games([MCTSearchPlayer(), MCTSearchPlayer()], n=100)
