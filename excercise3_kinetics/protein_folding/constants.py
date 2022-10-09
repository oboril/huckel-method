# This file contains only the constants given in handout

import numpy as np

variables = "kf_R15 ku_R15 kf_R16 ku_R16".split()
rate_const = {"kf_R15":26e3, "ku_R15":6.0e-2, "kf_R16":730, "ku_R16":7.5e-4}
urea_coeff = {"kf_R15":-1.68, "ku_R15":0.95, "kf_R16":-1.72, "ku_R16":1.20}