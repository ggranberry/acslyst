import matplotlib.pyplot as plt

# data = {
#     "eva": {'requires': 511, 'ensures': 374, 'loop invariant': 172, 'assigns': 151, 'loop assigns': 137, 'assert': 100, 'loop variant': 92, 'assumes': 42, 'behavior': 35, 'ghost': 11, 'complete behaviors': 7, 'disjoint behaviors': 7, 'logic': 1},
#     "pc": {'requires': 515, 'ensures': 397, 'loop invariant': 162, 'loop assigns': 115, 'assigns': 110, 'behavior': 101, 'assumes': 99, 'loop variant': 87, 'assert': 62, 'complete behaviors': 23, 'disjoint behaviors': 23, 'invariant': 13, 'predicate': 3, 'ghost': 1},
#     "plain": {'requires': 539, 'ensures': 508, 'assigns': 267, 'loop invariant': 208, 'assumes': 161, 'behavior': 160, 'loop assigns': 143, 'loop variant': 132, 'assert': 94, 'complete behaviors': 32, 'disjoint behaviors': 32, 'ghost': 23, 'predicate': 19, 'invariant': 2}
# }

data = {
        "plain": {'requires': 504, 'ensures': 447, 'assigns': 268, 'loop invariant': 204, 'assert': 161, 'behavior': 142, 'assumes': 140, 'loop assigns': 139, 'loop variant': 130, 'complete behaviors': 30, 'disjoint behaviors': 30, 'predicate': 17, 'ghost': 7, 'logic': 1},
        "pc": {'requires': 459, 'ensures': 387, 'loop invariant': 160, 'assigns': 113, 'loop assigns': 111, 'behavior': 100, 'assumes': 100, 'assert': 92, 'loop variant': 87, 'invariant': 35, 'complete behaviors': 22, 'disjoint behaviors': 22, 'predicate': 3, 'ghost': 1},
        "eva": {'requires': 489, 'ensures': 335, 'loop invariant': 172, 'assert': 155, 'assigns': 149, 'loop assigns': 138, 'loop variant': 91, 'assumes': 40, 'behavior': 36, 'complete behaviors': 7, 'disjoint behaviors': 7, 'ghost': 6, 'predicate': 1}
        }

# Extracting all annotation types and their values for each set
annotation_types = list(set().union(data['eva'], data['pc'], data['plain']))
sets = ['eva', 'pc', 'plain']

# Preparing the values matrix for each annotation type across different sets
values = [[data[set].get(annotation, 0) for annotation in annotation_types] for set in sets]

# Creating the bar graph for all annotation types
fig, ax = plt.subplots(figsize=(14, 8)) # Adjusted for better display of all annotation types
bar_width = 0.25
index = range(len(annotation_types))

bars = []
for i, set_values in enumerate(values):
    bars.append(ax.bar([x + bar_width*i for x in index], set_values, bar_width, label=sets[i]))

ax.set_xlabel('Annotation Type')
ax.set_ylabel('Number of Annotations')
ax.set_title('Comparison of Annotation Types between Eva, PC, and Plain')
ax.set_xticks([i + bar_width for i in range(len(annotation_types))])
ax.set_xticklabels(annotation_types, rotation=45, ha="right")
ax.legend()

plt.savefig('annotation_count_bar_graph.png')
plt.tight_layout()
plt.show()

