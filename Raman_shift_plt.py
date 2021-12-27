import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# read file
argv = sys.argv[1:]
if len(argv) == 0: argv = ["."]
filelist = list()
for path in argv:
    if os.path.isfile(path):
        if path[-4:] == ".asc":
            filelist.append(path)
    elif os.path.isdir(path):
        for dirpath, dirnames, filenames in os.walk(path):
            for file in filenames:
                if file[-4:] == ".asc":
                    filelist.append(os.path.join(dirpath, file))

# ndarray
A = np.stack([np.loadtxt(x, delimiter='\t') for x in filelist])
X, Y = A.transpose(2, 1, 0)
F = np.where(X < 50, 0, Y)
max = F.max(0)
min = F.min(0)
Y = (Y - min) / (max - min)

# plot
plt.rcParams['font.family'] = ['Microsoft JhengHei']
fig, ax = plt.subplots()
lines = ax.plot(X, Y, label=list(map(lambda x: x.removesuffix('.asc').rsplit('\\')[-1], filelist)))
ax.axis((0, X.max(), 0, 1))
ax.set_xlabel(r'$Raman\/shift\/(cm^{-1})$')
ax.grid(True)
leg = ax.legend(loc='center right', bbox_to_anchor=(-0.05, 0.5))

#legand picking
def on_pick(event):
    legline = event.artist
    origline = lined[legline]
    visible = not origline.get_visible()
    origline.set_visible(visible)
    legline.set_alpha(1.0 if visible else 0.2)
    fig.canvas.draw()


lined = {}
for legline, origline in zip(leg.get_lines(), lines):
    legline.set_picker(True)
    lined[legline] = origline
fig.canvas.mpl_connect('pick_event', on_pick)

plt.show()