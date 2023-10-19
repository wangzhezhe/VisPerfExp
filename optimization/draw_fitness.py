import pygad
import numpy
from random import randint
from time import sleep
import time
import matplotlib.pyplot as plt
import shutil
import os

# Saving the GA instance.
filename = 'genetic' # The filename to which the instance is saved. The name is without extension.

# Loading the saved GA instance.
loaded_ga_instance = pygad.load(filename=filename)
loaded_ga_instance.plot_fitness()
print(loaded_ga_instance)