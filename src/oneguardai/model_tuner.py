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

import platform
import sys
import pandas as pd
import numpy as np
# from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping
from keras_tuner.tuners import RandomSearch
from keras_tuner.engine.hyperparameters import HyperParameters

from oneguardai import const

# Platform and package information.
print(f"Python Platform: {platform.platform()}")
print(f"Python {sys.version}")
print(f"NumPy Version: {np.__version__}")
print(f"Tensor Flow Version: {tf.__version__}")
# print(f"Keras Version: {keras.__version__}")
print(f"Pandas {pd.__version__}")
gpu = len(tf.config.list_physical_devices('GPU')) > 0
print(f"GPU '{tf.config.list_physical_devices('GPU')}' is",
      "available" if gpu else "NOT AVAILABLE"
      )


# Check if GPU is accelerated.
def test_gpu():
    cifar = tf.keras.datasets.cifar100
    (x_train, y_train), (x_test, y_test) = cifar.load_data()
    model = tf.keras.applications.ResNet50(
            include_top=True,
            weights=None,
            input_shape=(32, 32, 3),
            classes=100, )

    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False)
    model.compile(optimizer="adam", loss=loss_fn, metrics=["accuracy"])
    model.fit(x_train, y_train, epochs=5, batch_size=64)


# test_gpu()

# Load dataset.
df = pd.read_csv("data/csv/features_good03.csv")

# PREPROCESSING:
# Convert iso-2 country codes to numbers (e.g. "US" -> 229).
df["WHOIS_COUNTRY"] = df["WHOIS_COUNTRY"].replace(const.COUNTRY_MAP)

# Drop the first column (domains).
df = df.iloc[:, 1:]

# Convert NaN values to -1 (or maybe 0.5?).
df = df.fillna(0)
# df = df.fillna(df.mean())  # Fill with mean value of the column.

# If in a row more than 75% of the values are missing, drop the row.
threshold = df.shape[1] * 0.75

# Drop rows with less than `threshold` non-NA values
df = df.dropna(thresh=threshold)

# Drop columns with only one unique value, as we cannot learn from them.
unique_counts = df.nunique()
# print("UNIQUE:", unique_counts)
df = df.loc[:, df.nunique() != 1]

# df = df.drop("SA_WEBSITE_SPEED", axis=1)
# df = df.drop("WHOIS_COUNTRY", axis=1)

# df["WHOIS_COUNTRY"] = df["WHOIS_COUNTRY"].astype(int)
df = df.apply(pd.to_numeric)
df = pd.DataFrame(df)

# Check if all values are numeric
is_all_numeric = df.applymap(np.isreal).all().all()
if is_all_numeric:
    print("Good: All values are numeric.")
else:
    print("Bad: Not all values are numeric.")

corr = df.corr()

# Generate a mask for the upper triangle
mask = np.triu(np.ones_like(corr, dtype=bool))

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(230, 20, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5}
            )

plt.show()

# CORRELATION MATRIX:
df = df.apply(pd.to_numeric)
numerical_df = df.select_dtypes(include=[np.number])

# Standardize the data (scale)
scaler = StandardScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(numerical_df),
                         columns=numerical_df.columns
                         )

correlation_matrix = df_scaled.corr()
# correlation_matrix = df.corr()
# print("MEDIAN:", correlation_matrix["TRUST"].sort_values(
#         ascending=False
#         )
#       )

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

sys.exit(0)

# Impute missing values (NaN) with the mean value of the column.
# TODO: unsure if needed or maybe better to use 0.5 / -1 (see above)?
# imputer = SimpleImputer(strategy="mean")
# df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

# Define features (X) and labels (y) -> input and output.
X = df.drop("TRUST", axis=1)
y = df["TRUST"]

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
        max_trials=5,
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

# Save the final model.
final_model.save('models/oneguardai_hdf.h5')
final_model.save('models/oneguardai_SavedModel', save_format='tf')

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
