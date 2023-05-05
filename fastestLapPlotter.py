from matplotlib import pyplot as plt
import fastf1
import fastf1.plotting
import datetime
import os
import sys

timestamp = datetime.datetime.now()

if len(sys.argv) > 0:
    note = sys.argv[1]

save = "Plots/" + timestamp.strftime("%Y-%b-%d") + "/" + timestamp.strftime("%X") + ": " + note + "/"
if not os.path.exists(save):
  os.makedirs(save)

fastf1.plotting.setup_mpl()

session = fastf1.get_session(2022, 'Miami', 'Q')

session.load()
ver = session.laps.pick_driver('VER').pick_fastest()
verCarData = ver.get_car_data()
verT = verCarData['Time']
verSpeed = verCarData['Speed']

per = session.laps.pick_driver('PER').pick_fastest()
perCarData = per.get_car_data()
perT = perCarData['Time']
perSpeed = perCarData['Speed']

# The rest is just plotting
fig, ax = plt.subplots()
ax.plot(verT, verSpeed, label='VER')
ax.plot(perT, perSpeed, label='PER')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Speed (Km/h)')
title = "Miami 2022 Quali: Fastest Lap"
ax.set_title(title)
ax.legend()
plt.savefig(save + title + ".pdf", format="pdf")
plt.savefig(save + title + ".png", format="png")
