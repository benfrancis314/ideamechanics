""" Note to reader:
    Only adjust the parameters listed after the imports. 
    See Methods section for their interpretation. 
    Other than that, if you hit run this should output Figure 12. """



from matplotlib import pyplot as plt
from math import cos
import random
from random import random as r

random.seed(7)


""" Adjust these paramters"""

M = 0.9 # Memory coefficient (determines how much is "lost" for the dynamics to work on)
A = 0.99 # Attraction coefficient; in range (0,1). A=1 pure attraction, A=0 pure repulsion.
p = 50 # Period of cos wave
amp = 0.2 # Amplitude of cos wave
sleep_time = 0
wake_time = 1500
time = list(range(3000))
dynamic = True
c_thresh = 6

"""Do not adjust code below, or proceed with caution if so. """

class Idea:
    """Idea, as defined by needs of psychological organoid research in sleep dynamics paper"""
    def __init__(self, id, c_now=0):
        self.id = id
        self.c_now = c_now
        self.c_next = 0
        self.tot_dist = sum(adj[id])
        self.orig = c_now
        
    def update(self):
        self.c_now = self.c_next
        self.c_next = 0
    
    def calc_next(self, t=0):
        if dynamic == True:
            if (t > sleep_time) & (t < wake_time): 
                A_dyn = A+(amp*cos(t/p) - amp)
            else: 
                A_dyn = A
        else: 
            A_dyn = A
        c_retain = M*self.c_now
        c_gain = 0  # Calculate how much is gained
        
        for idea in IS:
            if self.id != idea.id:
                c_gain_prop_atr = self.c_now/adj[self.id][idea.id]
                c_gain_prop_rep = 1/(adj[self.id][idea.id] * self.c_now)
                c_lost_dist_atr = idea.c_lost_dist_atr()
                c_lost_dist_rep = idea.c_lost_dist_rep()
                gain = idea.c_lost() * ((A_dyn * c_gain_prop_atr / c_lost_dist_atr) + ((1-A_dyn)* c_gain_prop_rep / c_lost_dist_rep))
                c_gain += gain
    
        self.c_next = c_retain + c_gain
        return self.c_next
        
    def c_lost(self):
        c_lost = (1-M)*self.c_now
        return c_lost
    
    def c_lost_dist_atr(self):
        """The sum of each other ideas c value divided by dist to this idea; used in calculating how the c_lost is 
            distributed to the other ideas"""
        c_lost_dist_atr = 0
        for idea in IS: 
            if idea.id != self.id:  # For all other ideas in idea space
                c_lost_dist_atr += idea.c_now/adj[self.id][idea.id]
        return c_lost_dist_atr
    
    def c_lost_dist_rep(self):
        """The sum of each other ideas c value divided by dist to this idea; used in calculating how the c_lost is 
            distributed to the other ideas"""
        c_lost_dist_rep = 0
        for idea in IS: 
            if idea.id != self.id:  # For all other ideas in idea space
                c_lost_dist_rep += 1/(adj[self.id][idea.id] * idea.c_now)
        return c_lost_dist_rep
    
    def reset(self):
        self.c_now = self.orig
        self.c_next = 0

# Define adjacency matrix. Index by 
adj = [
    [0,1,2,2,3,4,3,4,5,6],
    [1,0,1,1,2,3,2,3,4,5],
    [2,1,0,2,1,2,3,2,3,4],
    [2,1,2,0,1,2,1,2,3,4],
    [3,2,1,1,0,1,2,1,2,3],
    [4,3,2,2,1,0,3,2,1,2],
    [3,2,3,1,2,3,0,1,2,3],
    [4,3,2,2,1,2,1,0,1,2],
    [5,4,3,3,2,1,2,1,0,1],
    [6,5,4,4,3,2,3,2,1,0]
]

# Define the ideas we will be working with
init_c = [r(), r(), r(), 10, 10, r(), 10, 10, r(), r()]  # Initialize each idea with a C value
I0, I1, I2, I3, I4, I5, I6, I7, I8, I9 = Idea(0, init_c[0]), Idea(1, init_c[1]), Idea(2, init_c[2]), Idea(3, init_c[3]), Idea(4, init_c[4]), Idea(5, init_c[5]), Idea(6, init_c[6]), Idea(7, init_c[7]), Idea(8, init_c[8]), Idea(9, init_c[9])
IS = [I0, I1, I2, I3, I4, I5, I6, I7, I8, I9] # Define the idea space as a list
IS_size = len(IS) # Set size of idea space
cons_ideas = [0] * len(time)
for i in IS: 
    i.reset()
results = [ [0] * len(time) for j in range(IS_size)]
for t in time: 
    for i in range(len(IS)): 
        results[i][t] = IS[i].calc_next(t)
        IS[i].update()
        if IS[i].c_now > c_thresh:
            cons_ideas[t] += 1

plt.xlabel("Time")
plt.ylabel("Consciousness Value")
dream = "#ffaaaa"
plt.axvline(x=220, ymin=0.45, ymax=1, color=dream)
plt.axvline(x=450, ymin=0.45, ymax=1, color=dream)
plt.axvline(x=sleep_time, color="#cccccc")
plt.axvline(x=wake_time, color="#cccccc")
plt.axhline(y=c_thresh)
if dynamic == True: 
    plt.axhline(y=c_thresh, color="k")
    plt.title("Evolution of Idea Space Consciousness Values: M = " + str(M) + ", A = " + str(A) + ", p = " + str(p) + ", amp = " + str(amp))
else: 
    plt.title("Evolution of Idea Space Consciousness Values: M = " + str(M) + ", A = " + str(A))
for i in range(IS_size):
    plt.plot(time,results[i], label="Idea "+str(IS[i].id))
    plt.legend(loc=(1.03,0.2))
plt.show()
