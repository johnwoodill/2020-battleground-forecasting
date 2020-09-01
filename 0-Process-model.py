import subprocess
import os

os.system("python 1-Data-step.py")
os.system("python 2-GP-Model-Fit.py")
os.system("Rscript 4-Figures.R")

