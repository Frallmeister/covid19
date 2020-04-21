import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np

plt.ion()

def bayes(*args):
	"""
	P_H: 	Probablitily of hypothesis H
	P_EH:	Probability of event E given H 
	P_nH:	Probability of complement of H
	P_EnH:	Probability of E, given H is false
	"""
	args = args[0]
	P_H   = args[0]
	P_EH  = args[1]
	P_nH  = args[2]
	P_EnH = args[3]

	return P_H*P_EH/(P_H*P_EH+P_nH*P_EnH)


P_H   = 0.3
P_EH  = 0.05
P_nH  = 1-P_H
P_EnH = 0.9

P_var = np.arange(0,1,0.01)
probs = [[P_var, P_EH, P_nH, P_EnH],
		 [P_H, P_var, P_nH, P_EnH],
		 [P_H, P_EH, P_var, P_EnH],
		 [P_H, P_EH, P_nH, P_var]]

fig, ax = plt.subplots(2,2, figsize=(15,15))
figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()
axes = np.reshape(ax, -1)

p = ['P(H)', 'P(E|H)', 'P(-H)', 'P(E|-H)']
for i in range(4):
	P_HE = bayes(probs[i])
	axes[i].plot(P_var, P_HE, label=p[i])
	axes[i].set_xlabel(p[i], fontsize=15)
	axes[i].set_ylabel('P(H|E)', fontsize=15)
	axes[i].grid(True)
	axes[i].axis([0, 1, 0, 1])


x = np.linspace(0.1,1,100)
P_EH, P_EnH = np.meshgrid(x,x)
P_HE = bayes([P_H, P_EH, P_nH, P_EnH])

fig = plt.figure(constrained_layout=True)

figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()
ax = plt.axes(projection='3d')

# ax.contour(x,x,P_HE)
ax.plot_surface(P_EH, P_EnH, P_HE, cmap='viridis', edgecolor='none')
ax.set_xlabel('P_EH', fontsize=15)
ax.set_ylabel('P_EnH', fontsize=15)