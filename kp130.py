import math
import csv
import os

class DataLogger:
    def __init__(self, name):
        self.name = name
        self.data = {}

    def log(self, key, t, value):
        if key not in self.data:
            self.data[key] = []
        self.data[key].append((t, value))

    def export_csv(self, directory="data"):
        os.makedirs(directory, exist_ok=True)
        for key, values in self.data.items():
            path = os.path.join(directory, f"{self.name}_{key}.csv")
            with open(path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["time", key])
                writer.writerows(values)

class Experiment:
    name = "base"
    duration = 1.0
    timestep = 0.1

    def __init__(self):
        self.t = 0.0
        self.logger = DataLogger(self.name)

    def setup(self):
        pass

    def step(self, t):
        pass

    def analyze(self):
        pass

    def run(self):
        self.setup()
        steps = int(self.duration / self.timestep)
        for _ in range(steps):
            self.step(self.t)
            self.t += self.timestep
        self.analyze()
        self.logger.export_csv()

class PhysicsEngine:
    @staticmethod
    def motion(x, v, a, dt):
        v = v + a * dt
        x = x + v * dt
        return x, v

class BiologyEngine:
    @staticmethod
    def neuron(potential, stimulus, decay):
        return potential * decay + stimulus

class SignalEngine:
    @staticmethod
    def sine(freq, t, amp=1.0):
        return amp * math.sin(2 * math.pi * freq * t)

class PopulationEngine:
    @staticmethod
    def logistic(p, r, k):
        return p + r * p * (1 - p / k)

class SimpleMotionExperiment(Experiment):
    name = "motion"
    duration = 5.0
    timestep = 0.05

    def setup(self):
        self.x = 0.0
        self.v = 0.0
        self.a = 1.0

    def step(self, t):
        self.x, self.v = PhysicsEngine.motion(self.x, self.v, self.a, self.timestep)
        self.logger.log("position", t, self.x)
        self.logger.log("velocity", t, self.v)

class NeuronExperiment(Experiment):
    name = "neuron"
    duration = 3.0
    timestep = 0.02

    def setup(self):
        self.potential = 0.0

    def step(self, t):
        stimulus = SignalEngine.sine(5, t)
        self.potential = BiologyEngine.neuron(self.potential, stimulus, 0.95)
        self.logger.log("potential", t, self.potential)

class PopulationExperiment(Experiment):
    name = "population"
    duration = 10.0
    timestep = 0.1

    def setup(self):
        self.population = 10.0

    def step(self, t):
        self.population = PopulationEngine.logistic(self.population, 0.2, 100.0)
        self.logger.log("population", t, self.population)

class Kp130CLI:
    experiments = {
        "motion": SimpleMotionExperiment,
        "neuron": NeuronExperiment,
        "population": PopulationExperiment
    }

    @staticmethod
    def run(name):
        if name not in Kp130CLI.experiments:
            raise ValueError("Experiment not found")
        exp = Kp130CLI.experiments[name]()
        exp.run()

if __name__ == "__main__":
    import sys
    print("Hello from Ayaan Dhalait")
    if len(sys.argv) < 2:
        print("Available experiments:", ", ".join(Kp130CLI.experiments.keys()))
    else:
        Kp130CLI.run(sys.argv[1])
