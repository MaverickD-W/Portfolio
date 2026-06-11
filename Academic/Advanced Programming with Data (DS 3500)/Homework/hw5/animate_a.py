from model import green_line

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
matplotlib.rcParams["animation.ffmpeg_path"] = "/opt/homebrew/bin/ffmpeg"
import ffmpeg

sub = green_line                              # Define class
avg_actual = sub.daily_avg_travel             # Define dictionary of daily average for actual travel time
avg_sched = sub.daily_avg_scheduled           # Define dictionary of daily average for scheduled travel time


def update(frame,line,vals,x,y):
    """
    Takes frame, line, "vals" dictionary, x, and y
    Returns set up of values for line plot
    """
    x.append(frame)
    y.append(list(vals.values())[frame-1])      # Appends to y frame-1 from a list of values from the dictionary "vals"
    line.set_data(x,y)
    return line,


def animate(val1,val2):
    """
    Takes "val1" and "val2" dictionaries
    Creates animated line plots from the data in both dictionaries
    """
    fig, ax = plt.subplots(figsize=(10,6))          # Defines figure and axes, with figure size

    max_val1 = max(list(val1.values()))             # Defines the maximum value in list of "val1" dictionary
    max_val2 = max(list(val2.values()))             # Defines the maximum value in list of "val2" dictionary
    max_val = int(max([max_val1, max_val2]))             # Defines the maximum value from list of "max_val1" and "max_val2"
    ax.set_xlim(0, 30)
    ax.set_ylim(0, max_val+5)
    ax.fill_betweenx(y=range(max_val+6), x1=22, x2=24,
                     alpha=0.2, color="aqua")               # Creates a shaded region from February 22 to 24
    plt.xlabel("Days in February")
    plt.ylabel("Travel Time (seconds)")
    ax.set_xticks([a for a in range(1,29)],
                  [str(a) if a > 10 else ("0"+str(a)) for a in range(1,29)])    # Labels x-axis days in Feb with a 0 in front for single-digit numbers

    line, = ax.plot([],[], "limegreen", label="Actual Travel Time")       # Plots actual travel time
    x = []
    y = []
    ani1 = FuncAnimation(fig, update, frames=range(1,29), fargs=(line,val1,x,y),
                         repeat=False, interval=400)      # Animates and updates values in actual travel time
    line, = plt.plot([], [], "darkgreen", label="Scheduled Travel Time")        # Plots scheduled travel time
    ax.legend()
    x = []
    y = []
    ani2 = FuncAnimation(fig, update, frames=range(1,29), fargs=(line,val2,x,y),
                         repeat=False, interval=400)      # Animates and updates values in scheduled travel time
    plt.title("Actual vs. Scheduled Travel Time - Green Line")
    plt.show(block=False)
    ani1.save("mbta_greenline_animation_a.mp4", writer="ffmpeg", fps=28)


def main():
    """
    Executes animated plot of scheduled and actual travel time
    """
    animate(avg_actual,avg_sched)

if __name__ == "__main__":
    main()


