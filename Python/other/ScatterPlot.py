import matplotlib.pyplot as plt


friends = [ 70, 65, 72, 63, 71, 64, 60, 64, 67]
minutes = [175,170,205,120,220,130,105,145,190]
labels = ['a','b','c','d','e','f','g','h','i']

plt.scatter(friends,minutes)

# the zip contains the pairs ('a', 70, 175), ('b', 65, 170)
for label, friend_count, minute_count, in zip(labels,friends,minutes):
    # editing the plot points, the arguments for plt.annotate are:
    # (text, xy points, xytext] {some text}, fontsize= {int or double}, color = {text color})
    plt.annotate(label,
                 xy=(friend_count, minute_count),
                 xytext=(5,-5),
                 textcoords=('offset points')
    )
plt.show()