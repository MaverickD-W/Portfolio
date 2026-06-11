import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import Normalize
from model import green_line
import matplotlib
matplotlib.rcParams["animation.ffmpeg_path"] = "/opt/homebrew/bin/ffmpeg"
import ffmpeg

# Build the data
pivot = green_line.travel_by_stop_and_day   # rows=stations, cols=dates
stops = green_line.stops                     # geographic order (already applied to pivot)
dates = green_line.dates                     # sorted date strings

# Full data as numpy array: shape (n_stops, n_days)
data = pivot.values.astype(float)           # NaN where no data

n_stops, n_days = data.shape

vmin = np.nanpercentile(data, 10)
vmax = np.nanpercentile(data, 90)
norm = Normalize(vmin=vmin, vmax=vmax)

fig, ax = plt.subplots(figsize=(14, 9)) #20, 40
plt.subplots_adjust(left=0.15, right=0.88, top=0.97, bottom=0.04)

#new array
initial = np.full_like(data, np.nan)

im = ax.imshow(
    initial,
    aspect="auto",
    cmap="RdYlGn_r",
    norm=norm,
    interpolation="nearest",
)

# Colorbar
cbar = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
cbar.set_label("Mean Travel Time (seconds)", fontsize=14)

# 2. y-axis
station_labels = {
    "place-woodl": "Woodland",
    "place-sougr": "South St",
    "place-engav": "Englewood Ave",
    "place-kntst": "Kent St",
    "place-denrd": "Dean Rd",
    "place-cool": "Coolidge Corner",
    "place-clmnl": "Cleveland Circle",
    "place-hwsst": "Hawes St",
    "place-bndhl": "Bandhl",
    "place-fbkst": "Fairbanks St",
    "place-tapst": "Tappan St",
    "place-bcnwa": "Beacon/Washington",
    "place-sumav": "Summit Ave",
    "place-smary": "St. Mary's St",
    "place-stpul": "St. Paul St",
    "place-esomr": "East Somerville",
    "place-kencl": "Kenmore",
    "place-pktrm": "Park St",
    "place-wascm": "Washington/Comm",
    "place-fenwy": "Fenway",
    "place-chill": "Chiswick Rd",
    "place-sthld": "Sutherland Rd",
    "place-hymnl": "Hynes Convention",
    "place-longw": "Longwood",
    "place-chswk": "Chiswick",
    "place-grigg": "Griggs St",
    "place-lake": "Lake St",
    "place-alsgr": "Allston St",
    "place-harvd": "Harvard Ave",
    "place-wrnst": "Warren St",
    "place-brico": "Brico",
    "place-bland": "Blanford St",
    "place-brkhl": "Brookline Hills",
    "place-bucen": "Brookline Village",
    "place-boyls": "Boylston",
    "place-bvmnl": "Beaconsfield",
    "place-buest": "BU East",
    "place-babck": "Babcock St",
    "place-armnl": "Arlington",
    "place-coecl": "Copley",
    "place-amory": "Amory St",
    "place-bcnfd": "Beaconsfield",
    "place-waban": "Waban",
    "place-rsmnl": "Reservoir",
    "place-river": "Riverside",
    "place-balsq": "Ball Sq",
    "place-newtn": "Newton Centre",
    "place-eliot": "Eliot",
    "place-mgngl": "Magoun Sq",
    "place-gilmn": "Gilman Sq",
    "place-gover": "Government Center",
    "place-chhil": "Chestnut Hill Ave",
    "place-hsmnl": "Haseman",
    "place-newto": "Newton Highlands",
    "place-mdftf": "Medford/Tufts",
    "place-lngmd": "Longwood Med",
    "place-rvrwy": "Riverway",
    "place-lech": "Lechmere",
    "place-mispk": "Mission Park",
    "place-spmnl": "Science Park",
    "place-bckhl": "Chestnut Hill",
    "place-mfa": "Museum of Fine Arts",
    "place-nuniv": "Northeastern",
    "place-symcl": "Symphony",
    "place-haecl": "Haymarket",
    "place-unsqu": "Union Sq",
    "place-north": "North Station",
    "place-fenwd": "Fenwood Rd",
    "place-prmnl": "Prudential",
    "place-brmnl": "Brigham Circle",
}

readable_stops = [station_labels.get(s, s) for s in stops]

ax.set_yticks(range(n_stops))
ax.set_yticklabels(readable_stops, fontsize=9)

# 3. Bigger x-axis labels, rotated so they don't overlap
ax.set_xticks(range(n_days))
ax.set_xticklabels(
    [d[-2:] for d in dates],
    fontsize=10,
    rotation=0,
)

ax.set_xlabel("Day of February 2026", fontsize=11)
ax.set_ylabel("Station (geographic order)", fontsize=11)

title = ax.set_title("Green Line — Travel Time Heatmap", fontsize=15, pad=12)

# Animation Update
def update(frame):
    """Reveal columns 0..frame, leave the rest NaN."""
    revealed = np.full_like(data, np.nan)
    revealed[:, : frame + 1] = data[:, : frame + 1]
    im.set_array(revealed)
    title.set_text(
        f"Green Line — Travel Time Heatmap  |  Feb {dates[frame][-2:]} 2026"
    )
    return [im, title]

# Build and show
ani = animation.FuncAnimation(
    fig,
    update,
    frames=n_days,
    interval=400,       # ms per frame — adjust to taste
    blit=True,
    repeat=False,
)

plt.tight_layout()

def show(animation):
    plt.show(block=False)
    ani.save("mbta_greenline_animation_b.mp4", writer="ffmpeg", fps=28)
    print("Animation saved.")
    return

show(ani)


