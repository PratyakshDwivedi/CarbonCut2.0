from green_lib.scheduler import GridScheduler
from green_lib.governor import EROIGovernor
from green_lib.pruner import apply_pruning_and_save

# Simple ML model: Predict exam score from study hours

from sklearn.linear_model import LinearRegression
import numpy as np

# Training data (hours studied)
X = np.array([[1], [2], [3], [4], [5]])

# Corresponding exam scores
y = np.array([40, 50, 60, 70, 80])

# Create model
model = LinearRegression()

# Train model
GridScheduler(threshold=250).wait_for_green_window()
model.fit(callbacks=[EROIGovernor()], X, y)

# Predict score for a student studying 6 hours
prediction = model.predict([[6]])

print("Predicted Score:", prediction[0])

# Phase 3: Pruning
apply_pruning_and_save(model, filepath='my_heavy_model.h5')
