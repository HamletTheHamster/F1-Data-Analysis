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

session = fastf1.get_session(2023, 'Miami', 'Q')

session.load()
driver1 = 'LEC'
d1 = session.laps.pick_driver(driver1).pick_fastest()
#d1 = session.laps.pick_driver(driver1).pick_lap(19)
d1CarData = d1.get_car_data()
d1T = d1CarData['Time']
d1Speed = d1CarData['Speed']

driver2 = 'DEV'
d2 = session.laps.pick_driver(driver2).pick_fastest()
d2CarData = d2.get_car_data()
d2T = d2CarData['Time']
d2Speed = d2CarData['Speed']

# The rest is just plotting
fig, ax = plt.subplots()
ax.plot(d1T, d1Speed, label=driver1)
#ax.plot(d2T, d2Speed, label=driver2)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Speed (Km/h)')
ax.set_title(f"{session.event['EventName']} {session.event.year} {session.name}: Fastest Lap")
ax.legend()
plt.savefig(f"{save}{session.event['EventName']} {session.event.year} {session.name}: Fastest Lap.pdf", format="pdf")
plt.savefig(f"{save}{session.event['EventName']} {session.event.year} {session.name}: Fastest Lap.png", format="png")
