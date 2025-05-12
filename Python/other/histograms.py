from collections import Counter
import matplotlib.pyplot as plt
grades = [83,95,91,87,70,0,85,82,100,67,73,77,0]

# Decile is a function, the equivalent function in the more traditional sense is
"""
    def decile(grade):
        return grade // 10 * 10
"""
# lambda is the keyword which defines a function
# the '//' operator performs integer division which drops any remainders
#    e.g 83//10 = 8
# then the resulting value is multiplied by 10
decile = lambda grade: grade // 10 * 10

# histogram here is defined as a dictionary
"""
    histogram = {
        60: 1,
        70: 2,
        80: 5,
        90: 3
    }
"""
# Counter counts the number of occurrences of each unique item in an iterable. Does not automatically sort the data.
# To sort the data do sorted_hist = dict(sorted(histogram.items()))
histogram = Counter(decile(grade) for grade in grades)
barWidth = 8
# plt.bar() has 3 arguments: x values, y values, and the bar width
plt.bar([x for x in histogram.keys()], 
        histogram.values(),
        barWidth)

# Defines axis range: 
# X axis: -5 to 105 
# Y axis:  0 to  5
plt.axis([-5,105,0,5])
# Defines number of tick marks on x axis
plt.xticks([10*i for i in range(11)])
plt.show()