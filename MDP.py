
import numpy as np


f = open('mdpinput.txt', 'r')
c = 0
P = {}
A = []
initial_R = []
for line in f:
    if line.split(' ')[0] == '%':
        c = c + 1
        continue
    if c == 1:
        states = line.replace('\n','').replace(' ','').split(',')
        S = list(range(len(states)))
        # we store the states in S
    if c == 2:
        actions = line.replace('\n', '').replace(' ','').split(',')
        A = list(range(len(actions)))
        for i in range(len(A)):
            P[i] = []
        # we store our actions in A
    for i in range(5, 5+len(A)):
        if c == i:
            P[A[i - 5]].append(line.replace('\n', '').replace(' ','').split(','))
    # P is transition matrix based on specific each action in A
    if c == 5+len(A):
        initial_R.append(float(line.replace('\n', '').replace(' ', '').split(',')[2]))
    if c == 5+len(A)+1:
        gamma = float(line.replace('\n',''))
        # value of gamma
    if c == 5+len(A)+2:
        epsilon = float(line.replace('\n',''))
        # value of epsilon

for i in range(len(A)):
    for n in range(len(S)):
        for m in range(len(S)):
            P[A[i]][n][m] = float(P[A[i]][n][m])

R = np.reshape(initial_R, (len(S), len(A)))
# R is our reward matrix read from input.txt
def value_iteration(S, A, P, epsilon):
    u1 = len(S) * [0]
    u2 = len(S) * [0]
    act = len(S) * [0]
    delta = 1
    j = 0
    while(delta > epsilon*(1- gamma)/gamma):
        j = j+1
        u1 = u2[:]
        delta = 0
        for s in S:
            max_index, max_value = find_max(P, A, s, u1)
            u2[s] = max_value
            act[s] = max_index
            if abs(u1[s] - u2[s]) > delta:
                delta = abs(u1[s] - u2[s])
    return u1, act


def find_max(P, A, s, u):
    amax = []
    for a in A:
        amax.append(R[s][a] + gamma*np.matmul(P[a][s], u))
    return amax.index(max(amax)), max(amax)


u, opt_act = value_iteration(S, A, P, epsilon)

output = open('policy.txt', 'w+')
output.write('% Format:  State: Action (Value)\n')

for i in range(len(S)):
    output.write('S' + str(i) +': ' +'a' + str(opt_act[i]) + ' (' +str(round(u[i],2)) + ')' + '\n')

output.close()