V = [[0, 0, 1, 1, 1, 0, 0, 0, 0, 0], [0, 0, 1, 1, 0, 1, 0, 0, 0, 0], [1, 1, 0, 1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1, 1, 1, 0]]

#HAC POC

#clusters hashmap
clusters = {}
i = 1
for v in V:
    print v
    clusters['d' + str(i)] = v
    i += 1

print clusters
