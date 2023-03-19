import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(suppress=True)
class Point:
    x = None
    y = None
    z = None

    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return '[' + str(self.x) + ',' + str(self.y) + ',' + str(self.z) + ']'
    
    def __repr__(self) -> str:
        return '[' + str(self.x) + ',' + str(self.y) + ',' + str(self.z) + ']'

    def numpy(self):
        return np.array((self.x, self.y, self.z))

    def distance(self, p):
        return np.linalg.norm(self.numpy() - p.numpy())
    
    def norm3d(self):
        return np.linalg.norm(self.numpy())
    
    def norm2d(self):
        return np.linalg.norm(self.numpy()[1:])

class Cylinder:
    r = None
    m = None
    x1 = None
    x2 = None
    l = None

    """
    r - radius
    m - middle
    x - start on x axis
    l - lenght on x axis
    """
    def __init__(self, r, m, x, l) -> None:
        self.r = r
        self.m = m
        self.x1 = x
        self.x2 = x + l
        self.l = l

    def pointWithin(self, p):
        if callable(self.r):
            return p.norm2d() <= self.r(p.x - self.x1)
        else:
            return p.norm2d() <= self.r

class randNumCylinderGenerator():
    m = None
    r = None
    x = None

    xs = None
    ys = None
    zs = None

    def __init__(self, m, r, x) -> None:
        self.m = m
        self.r = r
        self.x = x

    def plotGenerated(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.scatter(self.xs, self.ys, self.zs)

        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        plt.show()

    def generatePoints(self, n):
        self.xs = np.random.uniform(0, self.x, n)

        theta = np.linspace(0, 2*np.pi, n)
        r = np.random.uniform(0, self.r, n)
        self.ys = self.m + r*np.sin(theta)
        self.zs = self.m + r*np.cos(theta)

        return list( map(lambda x: Point(x[0], x[1], x[2]), np.column_stack((self.xs, self.ys, self.zs))) )

def f(x):
    return 10*(0.5 - 0.005*np.power(x,2)) + 20

def g(x):
    return 15 + x

def h(x):
    return 25 - x


cylinders = [Cylinder(g, 0, 0, 5),
             Cylinder(20, 0, 5, 35),
             Cylinder(30, 0, 40, 10),
             Cylinder(20, 0, 50, 20),
             Cylinder(f, 0, 70, 20),
             Cylinder(20, 0, 90, 10),
             Cylinder(40, 0, 100, 10),
             Cylinder(25, 0, 110, 30),
             Cylinder(h, 0, 130, 5)]

# bounding cylinder shape
m = 0
r = 40
x = 145

n = 10000
n_experiments = 10

experiment_acc = []
experiment_shape_mass = []

mass = np.pi*np.power(42.5,2)*150

for i in range(n_experiments):
    print(f'experiment {i}')

    generator = randNumCylinderGenerator(m, r, x)

    points = generator.generatePoints(n)
    # generator.plotGenerated()

    points_within = 0

    # at first check x coordinate to find the right part of the shape
    # after that compute the distance of the point on y,z axes and check if its less than the radius of that part
    for p in points:
        for c in cylinders:
            if p.x >= c.x1 and p.x <= c.x2:
                if c.pointWithin(p):
                    points_within += 1
                    break
                
    
    box_mass = np.pi*np.power(r,2)*x
    shape_mass = points_within * mass / n

    acc = points_within/n

    print(f'box mass: {box_mass}', f'box mass: {shape_mass}')
    print(f'residual mass: {mass - shape_mass}')
    print(f'hit ratio: {acc}')

    experiment_acc.append(acc)
    experiment_shape_mass.append(shape_mass)
    

print(f'hit ratio mean: {np.mean(experiment_acc)}')
print(f'shape mass mean: {np.mean(experiment_shape_mass)}')
print(f'residual mass over all experiments: {mass - np.mean(experiment_shape_mass)}')