import matplotlib.pyplot as plt


time = [3.67129185542e-05, 5.21418181369e-05, 6.6118182319e-05]
nodes = [95364, 74617, 61784]



depth = [1, 2, 3, 4, 5, 6]

# Board Al
minimax_A = [10, 190, 2130, 34983, 417455, 6666384]
alphabeta_A = [10, 190, 1087, 6051, 33803, 266828]
figA = plt.figure()
dc4A = figA.add_subplot(111)
dc4A.scatter(depth, minimax_A, label='Minimax')
plt.title('Minimax and AlphaBeta algorithms opened nodes - Config A')
plt.xlabel('Depth cutoff')
plt.ylabel('Opened nodes in search tree')
plt.yscale('log')
dc4A.scatter(depth, alphabeta_A, color='red', label='AlphaBeta')
plt.legend(loc='upper left')
for i, txt in enumerate(minimax_A):
    dc4A.annotate(txt, (depth[i],minimax_A[i]))
for i, txt in enumerate(alphabeta_A):
    dc4A.annotate(txt, (depth[i],alphabeta_A[i]))
plt.show()

# Board B
minimax_B = [17, 223, 3754, 46051, 775913, 6699090]
alphabeta_B = [17, 223, 1386, 9224, 60808, 394456]
figB = plt.figure()
dc4B = figB.add_subplot(111)
dc4B.scatter(depth, minimax_B, label='Minimax')
plt.title('Minimax and AlphaBeta algorithms opened nodes - Config B')
plt.xlabel('Depth cutoff')
plt.ylabel('Opened nodes in search tree')
plt.yscale('log')
dc4B.scatter(depth, alphabeta_B, color='red', label='AlphaBeta')
plt.legend(loc='upper left')
for i, txt in enumerate(minimax_B):
    dc4B.annotate(txt, (depth[i],minimax_B[i]))
for i, txt in enumerate(alphabeta_B):
    dc4B.annotate(txt, (depth[i],alphabeta_B[i]))
plt.show()

# Board C
minimax_C = [14, 211, 3236, 49864, 790825, 7473096]
alphabeta_C = [14, 211, 1153, 5528, 24740, 199999]
alphabeta_C_rand = [14, 211, 1390, 8793, 35764, 213438]
alphabeta_C_ordering = [14, 211, 736, 4572, 16754, 81087]

figC = plt.figure()
dc4C = figC.add_subplot(111)
plt.title('Effect of move generation on opened nodes - Config C')
plt.xlabel('Depth cutoff')
plt.ylabel('Opened nodes in search tree')
plt.yscale('log')
dc4C.scatter(depth, alphabeta_C, color='blue', label='Left Right generated moves')
dc4C.scatter(depth, alphabeta_C_ordering, color='red', label='Ordered moves')
dc4C.scatter(depth, alphabeta_C_rand, color='green', label='Random generated moves')
plt.legend(loc='upper left')
for i, txt in enumerate(alphabeta_C):
    dc4C.annotate(txt, (depth[i],alphabeta_C[i]), verticalalignment='center')
for i, txt in enumerate(alphabeta_C_rand):
    dc4C.annotate(txt, (depth[i],alphabeta_C_rand[i]), verticalalignment='bottom')
for i, txt in enumerate(alphabeta_C_ordering):
    dc4C.annotate(txt, (depth[i],alphabeta_C_ordering[i]), verticalalignment='top')
plt.show()
