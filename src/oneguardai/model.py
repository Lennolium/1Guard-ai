#!/usr/bin/env python3

"""
model.py: TODO: Headline...

TODO: Description...
"""

# Header.
__author__ = "Lennart Haack"
__email__ = "lennart-haack@mail.de"
__license__ = "GNU GPLv3"
__version__ = "0.0.1"
__date__ = "2023-11-24"
__status__ = "Prototype/Development/Production"

import sys

# Imports.
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import matplotlib.pyplot as plt

# Generate synthetic data and create a DataFrame
# Replace this with your actual data loading and preprocessing
data = np.random.rand(1000, 10)
columns = [f"feature_{i}" for i in range(1, 11)]
df = pd.DataFrame(data, columns=columns)
df['label'] = np.random.randint(2, size=(1000,))  # Binary labels

print(df.head())

# Split the data into features (X) and labels (y)
X = df.drop('label', axis=1)
y = df['label']

print(X.head())
print(y.head())

sys.exit(0)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                    random_state=42
                                                    )

# Standardize and normalize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Build the neural network model
model = Sequential()
model.add(Dense(64, activation='relu', input_dim=X_train.shape[1]))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy',
              metrics=['accuracy']
              )

# Train the model
history = model.fit(X_train_scaled, y_train, epochs=10, batch_size=32,
                    validation_split=0.2
                    )

# Evaluate the model on the test set
test_loss, test_acc = model.evaluate(X_test_scaled, y_test)
print(f"Test Accuracy: {test_acc}")

# Plot training history
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()
