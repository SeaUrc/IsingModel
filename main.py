import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from compileGIF import compile
import os

def initializeRandom(N):
    lattice = np.random.choice([1, -1], size=(N, N))
    return lattice

def initializeUp(N):
    lattice = np.full((N, N), 1)
    return lattice

def initializeDown(N):
    lattice = np.full((N, N), -1)
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
    for _ in range(int(N*N/2)):  # single sweep
        i = np.random.randint(0, N)
        j = np.random.randint(0, N)
        spin = lattice[i, j]
        neighbors = (lattice[(i+1)%N, j] + lattice[i, (j+1)%N] +
                     lattice[(i-1)%N, j] + lattice[i, (j-1)%N])
        delta_E = 2 * spin * (J * neighbors + H)
        if delta_E < 0 or np.random.rand() < np.exp(-delta_E / T): # Boltzmann
            lattice[i, j] = -spin  # Accepted!
    return lattice

def nextFrame(lattice, T, steps, J=1.0, H=0.0):
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

# O(N^2*frames*stepsPerFrame)
# lattice size, [start, end), frames, number of metropolis steps per frame, whether to delete the individual .pngs after
def makeGIFOverT(N, startT, endT, frames, stepsPerframe, fps, deleteFiles, J=1.0, H=0.0):

    temperatures = [((i+1)*(endT-startT)/frames + startT) for i in range(frames)]

    lattice = initializeRandom(N)
    lattice = nextFrame(lattice, startT, 500, J, H)

    dir = '/Users/nick/Documents/Code/PythonCode2/IsingModel/picsOverT/'
    if not os.path.exists(dir):
        os.makedirs(dir)

    for i, T in enumerate(temperatures):
        lattice = nextFrame(lattice, T, stepsPerframe)
        plt.figure(figsize=(5, 5))
        plt.imshow(lattice, cmap='coolwarm', interpolation='nearest')
        plt.title(f"Ising Model with Temperature {startT:.2f}-{endT:.2f} Field {H:.2f}")
        plt.axis('off')
        plt.savefig(f"{dir}/frame_{i}.png", bbox_inches='tight')
        plt.close()
    
    compile(dir, fps, deleteFiles)

def makeGIFOverMetro(N, T, frames, stepsPerFrame, fps, deleteFiles, J=1.0, H=0.0):
    
    lattice = initializeDown(N)
    dir = '/Users/nick/Documents/Code/PythonCode2/IsingModel/picsOverMetro/'
    if not os.path.exists(dir):
        os.makedirs(dir)

    for i in range(frames):
        lattice = nextFrame(lattice, T, stepsPerFrame, J, H)
        plt.figure(figsize=(5, 5))
        plt.imshow(lattice, cmap='coolwarm', interpolation='nearest')
        plt.title(f"Ising Model with Temperature {T:.2f} and Field {H:.2f}; starting down")
        plt.axis('off')
        plt.savefig(f"{dir}/frame_{i}.png", bbox_inches='tight')
        plt.close()
    
    compile(dir, fps, deleteFiles)

def main():
    # n = 100
    # startT = 1.0
    # endT = 4.0
    # frames = 100
    # stepsPerFrame = 1
    # fps = 20
    # makeGIFOverT(n, startT, endT, frames, stepsPerFrame, fps, True, 1.0, 0)
    n = 256
    t = 1.5
    frames = 80
    stepsPerFrame = 1
    fps = 20
    makeGIFOverMetro(n, t, frames, stepsPerFrame, fps, True, 1.0, 1.0)

if __name__ == "__main__":
    main()