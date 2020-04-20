import time
import numpy as np
import matplotlib.pyplot as plt

class Individual:

    infectious_distance = 0.1
    dt = 0.01

    def __init__(self, box=[10,10], step_size=None, status='S', age=None, gender=None):

        
        def logistic_function(x, gender, x0=70, k=0.1):
            k = 1 if gender==1 else 0.9
            return k/(1+np.exp(-k*(x-x0))) + (1-k)

        # Set initial position of individual
        self.x = np.random.uniform(0, box[0])
        self.y = np.random.uniform(0, box[1])

        self.x_max = box[0]
        self.y_max = box[1]
        self.step_size = 0.01*max(self.x, self.y)
        
        self.age = np.random.randint(1,100)

        # Set gender (0=male, female=1)
        self.gender = np.random.choice([0,1])

        self.risk_value = logistic_function(self.age, self.gender)

        # Susceptible, infected or removed
        self.status=status.upper()

        self.time_infected = 0
        self.time_to_removal = np.random.randint(12,16)


    def update_position(self):
        x_step = self.x + np.random.choice([-self.step_size, 0, self.step_size])
        y_step = self.y + np.random.choice([-self.step_size, 0, self.step_size])

        if x_step < self.x_max and x_step > 0:
            self.x = x_step

        if y_step < self.y_max and y_step > 0:
            self.y = y_step

        # return (self.x, self.y)

    def time_step(self, people):

        self.time_infected += self.dt if self.status=='I' else 0
        self.update_position()

        if self.status=='S':
            for person in people:
                if person.status != 'I': continue

                distance = np.sqrt((self.x-person.x)**2 + (self.y-person.y)**2)
                if distance < self.infectious_distance and self.risk_value > np.random.uniform(0,1):
                    self.status = 'I'
                    break

        elif self.status=='I':
            if self.time_infected>self.time_to_removal:
                self.status='R'
                self.time_to_removal=None


def plot_update(people, ax, xlim=10, ylim=10):
    ax.clear()
    ax.axis([0, xlim, 0, ylim])
    c = {'S': 'b', 'I': 'r', 'R': 'gray'}

    for person in people:
        person.time_step(people)
        color = c[person.status]
        ax.plot(person.x, person.y, 'o', color=color)


def simulation(people, t_steps):

    s, i, r = [], [], []
    for t in range(t_steps):
        for person in people:
            person.time_step(people)

        s.append(len([i for i in people if i.status=='S']))
        i.append(len([i for i in people if i.status=='I']))
        r.append(len([i for i in people if i.status=='R']))

    return s,i,r


if __name__ == '__main__':
    plt.ion()

    xlim, ylim = 5, 5

    N = 200
    I0 = 10

    # Instantiate objects
    # people = [Individual(box=[xlim, ylim]) for _ in range(N-I0)]
    # people.extend([Individual(status='I') for _ in range(I0)])

    for L in range(3,10):
        xlim, ylim = L,L
        for n in [200]:
            print(f'\nL={L}, n={n}')

            # Instantiate objects
            people = [Individual(box=[xlim, ylim]) for _ in range(N-I0)]
            people.extend([Individual(status='I') for _ in range(I0)])

            # Run simulation
            t1 = time.time()
            t_max = 4000
            s,i,r = simulation(people, t_max)
            t2 = time.time()
            print(t2-t1)
            
        
            fig, ax = plt.subplots()
            ax.stackplot(np.linspace(0,t_max/100,len(s)), i,s,r, labels=['I', 'S', 'R'], colors=['r', 'b', 'gray'])
            ax.axis([0, t_max/100, 0, N])
            ax.set_title(f"N={n}, I0={I0}, xlim={xlim}, ylim={ylim}", fontsize=15)
            ax.legend()
