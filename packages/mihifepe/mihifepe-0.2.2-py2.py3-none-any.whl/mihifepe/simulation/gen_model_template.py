"""Script to load model from file"""

import pickle

from sympy.utilities.lambdify import lambdify

from mihifepe.simulation import model

# pylint: disable = invalid-name
config_filename = "GEN_MODEL_CONFIG_FILENAME_PLACEHOLDER"  # This string gets replaced by name of config file during simulation

with open(config_filename, "rb") as config_file:
    model_filename = pickle.load(config_file)
    noise_multiplier = pickle.load(config_file)
    noise_type = pickle.load(config_file)

with open(model_filename, "rb") as model_file:
    sym_vars = pickle.load(model_file)
    sym_features, sym_noise, sym_model_fn = sym_vars

model_fn = lambdify([sym_features, sym_noise], sym_model_fn, "numpy")
model = model.Model(model_fn, noise_multiplier, noise_type)
