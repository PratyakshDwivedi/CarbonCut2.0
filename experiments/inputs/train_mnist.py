# experiments/inputs/train_mnist.py
import tensorflow as tf

# Load Data
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

# Build a Dirty Model (Too big, no checks)
model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(512, activation='relu'), # Heavy layer
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10)
])

loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

model.compile(optimizer='adam',
              loss=loss_fn,
              metrics=['accuracy'])

# DIRTY PART 1: Runs immediately (doesn't check grid)
# DIRTY PART 2: Runs for 5 epochs even if it learns in 1
model.fit(x_train, y_train, epochs=5)

# DIRTY PART 3: Saves full heavy model
model.save("my_heavy_model.h5")