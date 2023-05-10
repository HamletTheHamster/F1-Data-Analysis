import fastf1.plotting
import matplotlib.pyplot as plt
import datetime
import os
import sys

timestamp = datetime.datetime.now()

if len(sys.argv) > 0:
    note = sys.argv[1]

save = "Plots/" + timestamp.strftime("%Y-%b-%d") + "/" + timestamp.strftime("%X") + ": " + note + "/"
if not os.path.exists(save):
  os.makedirs(save)

fastf1.plotting.setup_mpl(misc_mpl_mods=False)

session = fastf1.get_session(2023, 5, 'R')
session.load(telemetry=False, weather=False)

fig, ax = plt.subplots(figsize=(8.0, 4.9))

for drv in session.drivers:
    drv_laps = session.laps.pick_driver(drv)

    abb = drv_laps['Driver'].iloc[0]
    color = fastf1.plotting.driver_color(abb)

    ax.plot(drv_laps['LapNumber'], drv_laps['Position'],
            label=abb, color=color)

plt.title(f"{session.event['EventName']} {session.event.year} Position Changes During {session.name}")
ax.set_ylim([20.5, 0.5])
ax.set_yticks([1, 5, 10, 15, 20])
ax.set_xlabel('Lap')
ax.set_ylabel('Position')

ax.legend(bbox_to_anchor=(1.0, 1.02))
plt.tight_layout()


plt.savefig(f"{save}{session.event['EventName']} {session.event.year} Position Changes During {session.name}.pdf", format="pdf")
plt.savefig(f"{save}{session.event['EventName']} {session.event.year} Position Changes During {session.name}.png", format="png")
