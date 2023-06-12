# system configurations - only needed for CARLA
CARLA_ROOT = "C:/Users/Saad/Desktop/CARLA_Latest/WindowsNoEditor/PythonAPI/carla"

# model configurations
SMATO_MODEL = "trusty/models/smato_mobilenet_v2m"

# algorithm configurations
fluctuation_sensitvity = 0.25

# beta for momentum in trust - beta corresponds to proportion of history to take
beta_smato = 0.45
beta_fluc = 0.75

# trust based on eye contact detection is monotonically increasing, with the rate as follows
eye_rate = 0.12

# trust aggregation - must add to 1
alpha_trust = {
    "smato": 0.4,
    "eye":  0.4,
    "fluc": 0.2
}