prev = [1]
#print(prev)
for row in range(1, 10000):
    curr = [1]
    if row > 5:
        mid = int((row / 2) + 1)
        if row % 2 != 0:
            right = mid + 1
        else:
            right = mid - 1

        for index in range(1, mid):
            curr.append(prev[index-1] + prev[index])
        
        r = curr[0:right]
        r.reverse()
        curr.extend(r)
    else:
        for index in range(1, row):
            curr.append(prev[index-1] + prev[index])
        curr.append(1)
    #print curr
    prev = curr