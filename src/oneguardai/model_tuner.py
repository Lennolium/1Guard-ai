#!/usr/bin/env python3

"""
model_with_tuner.py: Hyperparameter tuning using Keras Tuner.

This script demonstrates how to use Keras Tuner to find the optimal
hyperparameters
for a neural network model on a binary classification task.

"""

# Header.
__author__ = "Lennart Haack"
__email__ = "lennart-haack@mail.de"
__license__ = "GNU GPLv3"
__version__ = "0.0.1"
__date__ = "2023-11-24"
__status__ = "Development"

import sys
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping
from keras_tuner.tuners import RandomSearch
from keras_tuner.engine.hyperparameters import HyperParameters

from oneguardai import const

# Load dataset.
df = pd.read_csv("data/output_modified.csv")

# PREPROCESSING:
# Convert iso-2 country codes to numbers (e.g. "US" -> 229).
df["WHOIS_COUNTRY"] = df["WHOIS_COUNTRY"].replace(const.COUNTRY_MAP)

# Convert NaN values to -1 (or maybe 0.5?).
df = df.fillna(0.5)

# Convert True/False values to 1/0 (already done while scraping).
df.replace(True, 1, inplace=True)
df.replace(False, 0, inplace=True)
df.replace("True", 1, inplace=True)
df.replace("False", 0, inplace=True)
df.replace("None", -1, inplace=True)
df.replace("NaN", -1, inplace=True)
df.replace(np.nan, -1, inplace=True)

# Drop the first column (domains).
df = df.iloc[:, 1:]

df[["UV_DETECTIONS"]] = df[["UV_DETECTIONS"]].apply(pd.to_numeric)

for col in df["UV_DETECTIONS"]:
    print(type(col))

# print(df.head())
print("------" * 10)
print(df[["UV_DETECTIONS"]])

df = df.drop("SA_WEBSITE_SPEED", axis=1)
df = df.drop("WHOIS_COUNTRY", axis=1)

# exit(0)

# CORRELATION MATRIX:
# numerical_df = df.select_dtypes(include=[np.number])
# correlation_matrix = numerical_df.corr()
df = df.apply(pd.to_numeric)

correlation_matrix = df.corr()

print("MEDIAN:", correlation_matrix["TRUST"].sort_values(
        ascending=False
        )
      )

plt.figure(figsize=(14, 12))
plt.imshow(correlation_matrix, cmap="viridis", interpolation="none",
           aspect="auto"
           )
plt.colorbar()
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
plt.xticks(range(len(correlation_matrix)), correlation_matrix.columns,
           rotation=90
           )
plt.yticks(range(len(correlation_matrix)), correlation_matrix.columns)
plt.title("Correlation Matrix")
plt.tight_layout()
plt.show()

exit(0)

# Impute missing values (NaN) with the mean value of the column.
# TODO: unsure if needed or maybe better to use 0.5 / -1 (see above)?
imputer = SimpleImputer(strategy="mean")
df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

# Define features (X) and labels (y) -> input and output.
X = df_imputed.drop("TRUST", axis=1)
y = df_imputed["TRUST"]

# Split the data into training and testing sets.
# Using 80% of data for training and a shuffle seed of 42.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                    random_state=42
                                                    )

# Standardize and normalize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# Define the hyperparameter search space
def build_model(hp):
    model = Sequential()
    model.add(Dense(
            units=hp.Int('units_input', min_value=32, max_value=512, step=32),
            activation=hp.Choice('activation_input',
                                 values=['relu', 'sigmoid']
                                 ),
            input_dim=X_train.shape[1]
            )
            )

    for i in range(hp.Int('num_layers', 1, 5)):
        model.add(Dense(
                units=hp.Int(f'units_{i}', min_value=32, max_value=512,
                             step=32
                             ),
                activation=hp.Choice(f'activation_{i}',
                                     values=['relu', 'sigmoid']
                                     )
                )
                )

    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='adam', loss='binary_crossentropy',
                  metrics=['accuracy']
                  )
    return model


# Define the tuner
tuner = RandomSearch(
        build_model,
        objective='val_accuracy',
        max_trials=5,  # Adjust as needed
        directory='tuner_dir',  # Directory to save the tuner results
        project_name='trust_scam_tuning'
        )

# Perform hyperparameter tuning
tuner.search(X_train_scaled, y_train, epochs=10, validation_split=0.2)

# Get the best hyperparameters
best_hp = tuner.get_best_hyperparameters(num_trials=1)[0]

# Build the final model with the best hyperparameters
final_model = tuner.hypermodel.build(best_hp)

# Train the final model
final_model.fit(X_train_scaled, y_train, epochs=10, batch_size=32,
                validation_split=0.2, callbacks=[EarlyStopping(patience=3)]
                )

# Evaluate the final model on the test set
test_loss, test_acc = final_model.evaluate(X_test_scaled, y_test)
print(f"Test Accuracy: {test_acc}")

# Make predictions on the test set
predictions = final_model.predict(X_test_scaled)
confidence = predictions.flatten()  # Adjust as needed

# Plot confidence distribution
plt.hist(confidence, bins=20, color='blue', alpha=0.7)
plt.xlabel('Confidence')
plt.ylabel('Frequency')
plt.title('Confidence Distribution')
plt.show()
