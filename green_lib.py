import random
import time

def wait_for_green_window():
    # Simulate fetching grid intensity
    intensity = random.randint(100, 450)
    print(f"Carbon Intensity Checked: {intensity}g/kWh")
    return intensity

class EROIGovernor:
    def __init__(self):
        self.model = None
    def on_epoch_end(self, epoch, logs=None):
        # Stop training if it's no longer 'green' (energy-efficient)
        if logs.get('accuracy', 0) > 0.90:
            self.model.stop_training = True