import numpy as np
from scipy.integrate import solve_ivp
from matplotlib import pyplot as plt
from datetime import datetime

import oregonator_equations_log as oreg

T_MAX = 120
STEPS = 1000

print("Solving equations...")
start = datetime.now()
solution = solve_ivp(oreg.conc_changes, (0,T_MAX), oreg.initial_concs, t_eval=np.linspace(0,T_MAX,STEPS), method='BDF', vectorized=True, rtol=1e-2, atol=0.001)
print("Finished in", datetime.now()-start)
print("Solved!")
print(solution.message)



for i in range(len(solution.y)):
    plt.plot(solution.t, solution.y[i], label=oreg.variables[i])

plt.ylim([-30,0])
plt.legend()
plt.show()