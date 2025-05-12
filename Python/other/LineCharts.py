import matplotlib.pyplot as plt
import copy
variance = [1,2,4,8,16,32,64,128,256]
# lists and dictionaries are passed by reference and will point to the same memory address. Use something like copy.copy() or copy.deepcopy() to make copies of lists. deepcopy() is for lists which contain other lists and prevent pointing to their memory addresses
bias_squared = copy.deepcopy(variance)
# reverses the list order
bias_squared.reverse()

""" print the memory address 
print(hex(id(variance)))
print(hex(id(bias_squared))) 
"""

# zip takes n lists and makes pairs
""" 
    list1 = [1, 2, 4]
    list2 = [9, 8, 6]
    zip(list1,list2) === zip([1, 2, 4], [9, 8, 6])
                      => (1,9), (2,8), (4,6)
    this can be iterated through their x-y coordinate points 

    can have more coordinates than just x,y can have n number
    list1 = [1, 2, 4]
    list2 = [9, 8, 6]
    list3 = [4, 1, 5]

[print(x+y+z) for x,y,z in zip(list1,list2,list3)]
"""
total_error = [x+y for x, y in zip(variance,bias_squared)]

# xs = index for index in total number indices of variance, getting the size for the x axis
xs =[i for i,_ in enumerate(variance)]

plt.plot(xs, variance, 'g-', label='variance')
plt.plot(xs, bias_squared, 'r-', label='bias')
plt.plot(xs, total_error, 'b:', label='total error')
plt.legend()
plt.xlabel("model")
plt.title("Title")


plt.show()