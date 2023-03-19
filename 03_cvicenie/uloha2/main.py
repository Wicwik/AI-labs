import pyddl
import sys
import simulator

class world:
    __map = {}
    __totalGold = 0
    __maxX = 0
    __maxY = 0
    __startX = 0
    __startY = 0

    def load(self, file):
        f = open(file, 'r')
        data = f.read().split('\n')
        f.close()
        self.__parse(data)

    def __parse(self, data):
        y = 0
        for line in data:
            self.__maxY = y
            x = 0
            for char in line:
                self.__maxX = max(self.__maxX, x)
                self.__map[(x,y)] = char
                if char == 'g':
                    self.__totalGold+=1
                if char == '@':
                    self.__startX = x
                    self.__startY = y
                x+=1
            y+=1


    def __getPositions(self):
        if self.__maxX > self.__maxY:
            return range(self.__maxX+1)

        return range(self.__maxY+1)
    
    def __getMoves(self):
        moves = list()
        for pos in self.__getPositions()[:-1]:
            moves.append(('inc', pos, pos+1))
            moves.append(('dec', pos+1, pos))

        return moves
    
    def __getMapInit(self):
        init = [
            ('at', self.__startX, self.__startY),
            ('=', ('goldbag',), 0),
            ('=', ('quiver',), 0)
        ]

        for pos, value in self.__map.items():
            # print(pos, value)
            if value == ' ':
                init.append(('empty', pos[0], pos[1]))
            elif value == 'g':
                init.append(('empty', pos[0], pos[1]))
                init.append(('gold', pos[0], pos[1]))
            elif value == 'A':
                init.append(('empty', pos[0], pos[1]))
                init.append(('arrow', pos[0], pos[1]))
            elif value == 'W':
                init.append(('wumpus', pos[0], pos[1]))
        
        return init


    def __getInit(self):
        init = self.__getMoves() + self.__getMapInit()

        # print(len(self.__getMoves()))

        return init
    
    def __getGoal(self):
        goal = [
            ('=', ('goldbag',), self.__totalGold),
            ('at', self.__startX, self.__startY)
        ]

        return goal

    def getProblem(self):
        init = self.__getInit()
        goal = self.__getGoal()
        positions = list(self.__getPositions())

        # print(init)
        # print(goal)
        # print(positions)

        domain = pyddl.Domain((
            pyddl.Action(
                'move-left',
                parameters=(
                    ('position', 'px'),
                    ('position', 'py'),
                    ('position', 'tx')
                ),
                preconditions=(
                    ('at', 'px', 'py'),
                    ('empty', 'tx', 'py'),
                    ('dec', 'px', 'tx')
                    ),
                effects=(
                    pyddl.neg(('at', 'px', 'py')),
                    pyddl.neg(('empty', 'tx', 'py')),
                    ('at', 'tx', 'py'),
                    ('empty', 'px', 'py')
                )
            ),
            pyddl.Action(
                'move-right',
                parameters=(
                    ('position', 'px'),
                    ('position', 'py'),
                    ('position', 'tx')
                ),
                preconditions=(
                    ('at', 'px', 'py'),
                    ('empty', 'tx', 'py'),
                    ('inc', 'px', 'tx')
                    ),
                effects=(
                    pyddl.neg(('at', 'px', 'py')),
                    pyddl.neg(('empty', 'tx', 'py')),
                    ('at', 'tx', 'py'),
                    ('empty', 'px', 'py')
                )
            ),
            pyddl.Action(
                'move-up',
                parameters=(
                    ('position', 'px'),
                    ('position', 'py'),
                    ('position', 'ty')
                ),
                preconditions=(
                    ('at', 'px', 'py'),
                    ('empty', 'px', 'ty'),
                    ('dec', 'py', 'ty')
                    ),
                effects=(
                    pyddl.neg(('at', 'px', 'py')),
                    pyddl.neg(('empty', 'px', 'ty')),
                    ('at', 'px', 'ty'),
                    ('empty', 'px', 'py')
                )
            ),
            pyddl.Action(
                'move-down',
                parameters=(
                    ('position', 'px'),
                    ('position', 'py'),
                    ('position', 'ty')
                ),
                preconditions=(
                    ('at', 'px', 'py'),
                    ('empty', 'px', 'ty'),
                    ('inc', 'py', 'ty')
                    ),
                effects=(
                    pyddl.neg(('at', 'px', 'py')),
                    pyddl.neg(('empty', 'px', 'ty')),
                    ('at', 'px', 'ty'),
                    ('empty', 'px', 'py')
                )
            ),
            pyddl.Action(
                'take-gold',
                parameters=(
                    ('position', 'gx'),
                    ('position', 'gy')
                ),
                preconditions=(
                    ('at', 'gx', 'gy'),
                    ('gold', 'gx', 'gy')
                ),
                effects=(
                    ('+=', ('goldbag',), 1),
                    pyddl.neg(('gold', 'gx', 'gy'))
                )
            ),
            pyddl.Action(
                'take-arrow',
                parameters=(
                    ('position', 'ax'),
                    ('position', 'ay')
                ),
                preconditions=(
                    ('at', 'ax', 'ay'),
                    ('arrow', 'ax', 'ay')
                ),
                effects=(
                    pyddl.neg(('arrow', 'ax', 'ay')),
                    ('+=', ('quiver',), 1)
                )
            ),
            pyddl.Action(
                'shoot-wumpus-right',
                parameters=(
                    ('position', 'px'),
                    ('position', 'py'),
                    ('position', 'wx')
                ),
                preconditions=(
                    ('at', 'px', 'py'),
                    ('wumpus', 'wx', 'py'),
                    ('inc', 'px', 'wx'),
                    ('>', ('quiver',), 0)
                ),
                effects=(
                    ('-=', ('quiver',), 1),
                    pyddl.neg(('wumpus', 'wx', 'py')),
                    ('empty', 'wx', 'py')
                )
            ),
            pyddl.Action(
                'shoot-wumpus-left',
                parameters=(
                    ('position', 'px'),
                    ('position', 'py'),
                    ('position', 'wx')
                ),
                preconditions=(
                    ('at', 'px', 'py'),
                    ('wumpus', 'wx', 'py'),
                    ('dec', 'px', 'wx'),
                    ('>', ('quiver',), 0)
                ),
                effects=(
                    ('-=', ('quiver',), 1),
                    pyddl.neg(('wumpus', 'wx', 'py')),
                    ('empty', 'wx', 'py')
                )
            ),
            pyddl.Action(
                'shoot-wumpus-up',
                parameters=(
                    ('position', 'px'),
                    ('position', 'py'),
                    ('position', 'wy')
                ),
                preconditions=(
                    ('at', 'px', 'py'),
                    ('wumpus', 'px', 'wy'),
                    ('dec', 'py', 'wy'),
                    ('>', ('quiver',), 0)
                ),
                effects=(
                    ('-=', ('quiver',), 1),
                    pyddl.neg(('wumpus', 'px', 'wy')),
                    ('empty', 'px', 'wy')
                )
            ),
            pyddl.Action(
                'shoot-wumpus-down',
                parameters=(
                    ('position', 'px'),
                    ('position', 'py'),
                    ('position', 'wy')
                ),
                preconditions=(
                    ('at', 'px', 'py'),
                    ('wumpus', 'px', 'wy'),
                    ('inc', 'py', 'wy'),
                    ('>', ('quiver',), 0)
                ),
                effects=(
                    ('-=', ('quiver',), 1),
                    pyddl.neg(('wumpus', 'px', 'wy')),
                    ('empty', 'px', 'wy')
                )
            ),
        ))

        problem = pyddl.Problem(
            domain,
            {
                'position': tuple(positions),
            },
            init=tuple(init),
            goal=tuple(goal),
        )
        return problem

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Map file need to be specified!")
        print("Example: python3 " + sys.argv[0] + " world1.txt")
        sys.exit(1)
    w = world()
    w.load(sys.argv[1])
    problem = w.getProblem()
    plan = pyddl.planner(problem, verbose=True)
    if plan is None:
        print('Hunter is not able to solve this world!')
    else:
        actions = [action.name for action in plan]
        print(", ".join(actions))
        f = open(sys.argv[1] + ".solution", "w")
        f.write("\n".join(actions))
        f.close()
        input()
        simulator.simulate(sys.argv[1], sys.argv[1] + ".solution")
