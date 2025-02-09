import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def initialize_lattice(N):
    lattice = np.random.choice([1, -1], size=(N, N))
    return lattice

def compute_energy(lattice, J=1.0, H=0.0):
    
    N = lattice.shape[0]
    energy = 0.0
    for i in range(N):
        for j in range(N):
            spin = lattice[i, j] 
            neighbors = (lattice[(i+1)%N, j] + lattice[i, (j+1)%N] + 
                         lattice[(i-1)%N, j] + lattice[i, (j-1)%N]) # periodic 
            energy += -J * spin * neighbors - H * spin
    #pairs r double counted
    return energy / 2.0

def metropolis_step(lattice, T, J=1.0, H=0.0):
    N = lattice.shape[0]
    for _ in range(N * N):  # single sweep
        i = np.random.randint(0, N)
        j = np.random.randint(0, N)
        spin = lattice[i, j]
        neighbors = (lattice[(i+1)%N, j] + lattice[i, (j+1)%N] +
                     lattice[(i-1)%N, j] + lattice[i, (j-1)%N])
        delta_E = 2 * spin * (J * neighbors + H)
        if delta_E < 0 or np.random.rand() < np.exp(-delta_E / T): # Boltzmann
            lattice[i, j] = -spin  # Accepted!
    return lattice

def metroStep(lattice, T, steps, J=1.0, H=0.1):
    print(f"TEMP {T}")
    for step in range(steps):
        lattice = metropolis_step(lattice, T, J, H)
        # E = compute_energy(lattice, J, H)
        # M = np.sum(lattice)
        # energies.append(E)
        # magnetizations.append(M)
        # if step % (10) == 0:
            # print(f"TEMP {T}, Step {step}: E = {E:.2f}, M = {M}")
            # print(f"TEMP {T}, Step {step}")
    

    return lattice


N = 50     # Lattice size (NxN)
T = 1.0
steps = 70       
startT = 1.5
endT = 4.0
tot = 200

temperatures = [((i)*(endT-startT)/tot + startT) for i in range(tot+1)]

# lattices, energies, magnetizations = simulate_ising(N, temperatures, steps)

# fig, axes = plt.subplots(4, 10)
# axes = axes.flatten()

lattice = initialize_lattice(N)
# lattice = metroStep(lattice, temperatures[0], 500)

for i, T in enumerate(temperatures):
    lattice = metroStep(lattice, T, steps)
    plt.figure(figsize=(5, 5))
    plt.imshow(lattice, cmap='coolwarm', interpolation='nearest')
    plt.title(f"Temperature {T}")
    plt.axis('off')
    plt.savefig(f"pics/frame_{i}.png", bbox_inches='tight')
    plt.close()

