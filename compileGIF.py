import imageio
import os


dir = "/Users/nick/Documents/Code/PythonCode2/IsingModel/pics/"

totalFrames = len([f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))])
filenames = [f"pics/frame_{i}.png" for i in range(totalFrames)]

# for filename in filenames:
#     os.remove(filename)
# quit()

images = []
for filename in filenames:
    images.append(imageio.imread(filename))

imageio.mimsave("Ising.gif", images, fps=200)

