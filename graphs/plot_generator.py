import matplotlib.pyplot as plt

class GraphGenerator:
    def plot(self, data, title, filename):
        plt.figure()
        plt.plot(data)
        plt.title(title)
        plt.xlabel('Steps')
        plt.ylabel('Performance')
        plt.savefig(f'graphs/{filename}')
        plt.close()
