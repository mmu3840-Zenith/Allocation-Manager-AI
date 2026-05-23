import imageio
import os

class GIFRecorder:
    def __init__(self, folder='gif_logs'):
        self.frames = []
        self.folder = folder

    def add_frame(self, surface):
        frame = surface.copy()
        self.frames.append(frame)

    def save(self, name='simulation.gif'):
        path = os.path.join(self.folder, name)
        imageio.mimsave(path, self.frames, fps=10)
        print(f'GIF saved to {path}')
