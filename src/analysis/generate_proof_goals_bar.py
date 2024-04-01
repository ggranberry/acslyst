import matplotlib.pyplot as plt

# Data
categories = ["Plain", "PC", "Eva"]
total_goals = [5631, 4671, 5032]
proven_goals = [4421, 3251, 3769]

loop_inv_goals = [424, 350, 364]
loop_inv_proven_goals = [321, 260, 289]

ensures_goals = [434, 420, 369]
ensures_proven = [308, 277, 290]

x = range(len(categories))  # the label locations

# Plotting
fig, ax = plt.subplots()
bar_width = 0.35  # the width of the bars
opacity = 0.8

rects1 = ax.bar(
    x,
    ensures_goals,
    bar_width,
    alpha=opacity,
    color="b",
    label="Total Goals",
)
rects2 = ax.bar(
    [p + bar_width for p in x],
    ensures_proven,
    bar_width,
    alpha=opacity,
    color="g",
    label="Proven Goals",
)

ax.set_xlabel("Analysis Type")
ax.set_ylabel("Number of Goals")
ax.set_title("WP Analysis Results Comparison for postconditions")
ax.set_xticks([p + bar_width / 2 for p in x])
ax.set_xticklabels(categories)
ax.legend()

# Adding counts above bars
for rect in rects1 + rects2:
    height = rect.get_height()
    ax.annotate(
        "{}".format(height),
        xy=(rect.get_x() + rect.get_width() / 2, height),
        xytext=(0, 3),  # 3 points vertical offset
        textcoords="offset points",
        ha="center",
        va="bottom",
    )

plt.tight_layout()
plt.show()
