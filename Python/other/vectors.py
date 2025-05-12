def vector_add(arr1, arr2):
    return [x+y for x, y in zip(arr1, arr2)]

def vector_sum(vectors):
    result = vectors[0]
    for vector in vectors[1:]:
        result = vector_add(result,vector)
    return result
friends = [ 70, 65, 72, 63, 71, 64, 60, 64, 67]
print(vector_sum(friends))

