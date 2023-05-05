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

session = fastf1.get_session(2023, 'Baku', 'Q')

session.load()
fast_leclerc = session.laps.pick_driver('LEC').pick_fastest()
lec_car_data = fast_leclerc.get_car_data()
t = lec_car_data['Time']
vCar = lec_car_data['Speed']

# The rest is just plotting
fig, ax = plt.subplots()
ax.plot(t, vCar, label='LEC')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Speed (Km/h)')
title = "Baku 2023 Quali: Fastest Lap"
ax.set_title(title)
ax.legend()
plt.savefig(save + title + ".pdf", format="pdf")
plt.savefig(save + title + ".png", format="png")
