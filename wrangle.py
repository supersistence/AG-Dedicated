import matplotlib.pyplot as plt

counts, bins, __not_important = plt.hist(heights, bins=11,
color=
"lightgray", edgecolor=
"black")
plt.ylabel("Count")
plt.show()