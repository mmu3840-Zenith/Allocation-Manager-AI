class MetricsEngine:
    def __init__(self):
        self.completed = 0

    def update(self, items):
        self.completed = sum(1 for i in items if i.delivered)
        return self.completed
