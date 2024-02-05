import matplotlib.pyplot as plt

# Data
categories = ['PC Analysis', 'Plain Analysis']
total_goals = [4098, 5817]
proven_goals = [2873, 4517]
no_assigns_goals = [3303, 4084]
no_assigns_proven = [2982, 4084]

x = range(len(categories))  # the label locations

# Plotting
fig, ax = plt.subplots()
bar_width = 0.35  # the width of the bars
opacity = 0.8

rects1 = ax.bar(x, no_assigns_goals, bar_width, alpha=opacity, color='b', label='Total Goals without assigns clasuses')
rects2 = ax.bar([p + bar_width for p in x], no_assigns_proven, bar_width, alpha=opacity, color='g', label='Proven Goals without assigns clauses')

ax.set_xlabel('Analysis Type')
ax.set_ylabel('Number of Goals')
ax.set_title('WP Analysis Results Comparison')
ax.set_xticks([p + bar_width / 2 for p in x])
ax.set_xticklabels(categories)
ax.legend()

# Adding counts above bars
for rect in rects1 + rects2:
    height = rect.get_height()
    ax.annotate('{}'.format(height),
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom')

plt.tight_layout()
plt.show()

