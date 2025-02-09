import imageio.v2 as imageio
import os

def compile(dir, fps, deleteAfter):
    # dir = "/Users/nick/Documents/Code/PythonCode2/IsingModel/pics/"
    totalFrames = len([f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))])
    print(totalFrames)
    filenames = [f"{dir}/frame_{i}.png" for i in range(totalFrames)]

    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))

    imageio.mimsave("Ising.gif", images, format='GIF', fps=fps)

    if deleteAfter:
        for filename in filenames:
            os.remove(filename)
        print(f"Deleted files in {dir}")


