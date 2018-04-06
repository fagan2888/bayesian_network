# First, we build bn, which is a dictionary, from bn.txt.

bn = {}
f = open('bn.txt', 'r')
c = 0
for line in f:
    if line.split(' ')[0] == '%':
        c = c + 1
        continue
    if c == 1:
        vars = line.replace('\n','').replace(' ','').split(',')
        # vars is a list where we put our events.
        for v in vars:
            bn[v] = [[],{}]
    if c == 2:
        edge = line.replace('\n','').replace(' ','').split(',')
        bn[edge[1]][0].append(edge[0])
    if c == 3:
        prob_list = line[2:].replace('\n','').split(')')
        prob = float(prob_list[1].split('=')[1])
        p1 = prob_list[0].split('|')
        if len(p1) == 1:
            p2 = p1[0].split('=')
            bn[p2[0]][1][None] = prob
        if len(p1) == 2:
            q = p1[0].split('=')[0]
            p2 = p1[1].split(',')
            if len(p2) == 1:
                bn[q][1][p2[0].split('=')[1]] = prob
            if len(p2) == 2:
                cond1 = p2[0].split('=')[1]
                cond2 = p2[1].split('=')[1]
                if cond1 == 'T' and cond2 == 'T':
                    bn[q][1]['T,T'] = prob
                if cond1 == 'F' and cond2 == 'T':
                    bn[q][1]['F,T'] = prob
                if cond1 == 'T' and cond2 == 'F':
                    bn[q][1]['T,F'] = prob
                if cond1 == 'F' and cond2 == 'F':
                    bn[q][1]['F,F'] = prob

# e is evidence dictionary.
e = {}
f2 = open('input.txt','r')
d = 0
for line in f2:
    if line.split(' ')[0] == '%':
        d = d+1
        continue
    if d == 1:
        X = line.replace('\n','')
        # X is query that we want to know its probability.
    if d == 2:
        r = line.replace('\n','').replace(' ','').split(',')
        e[r[0].split('=')[0]] = r[0].split('=')[1]
        e[r[1].split('=')[0]] = r[1].split('=')[1]

def enumeration_ask(X, e):
    e[X] = 'T'
    key1 = vars
    Qt = enumerate_all(key1, e)
    e[X] = 'F'
    key2 = vars
    Qf = enumerate_all(key2, e)
    return (Qt/(Qt + Qf),Qf/(Qt + Qf))


def enumerate_all(vars, e):
    if vars == []:
        return 1.0
    else:
        Y = vars[0]
        if Y in e:
            if e[Y] == 'T':
                return prob(Y,e,bn) * enumerate_all(vars[1:], e)

            else:
                return (1 - prob(Y,e,bn)) * enumerate_all(vars[1:], e)
        else:
            e[Y] = 'T'
            prob_true = prob(Y,e,bn) * enumerate_all(vars[1:], e)
            e[Y] = 'F'
            prob_false = (1 - prob(Y,e,bn)) * enumerate_all(vars[1:], e)
            e.pop(Y, None)
            return prob_true + prob_false


# function prob is used to calculate probability.
def prob(Y,e,bn):
    a = []
    if bn[Y][0] != []:
        parents = bn[Y][0]
        for i in parents:
            a.append(e[i])
        if len(a) == 1:
            return bn[Y][1][a[0]]
        if len(a) == 2:
            if a[0] == 'T' and a[1] == 'T':
                return bn[Y][1]['T,T']
            if a[0] == 'F' and a[1] == 'T':
                return bn[Y][1]['F,T']
            if a[0] == 'T' and a[1] == 'F':
                return bn[Y][1]['T,F']
            if a[0] == 'F' and a[1] == 'F':
                return bn[Y][1]['F,F']
    else:
        return bn[Y][1][None]


en = enumeration_ask(X, e)
print('The probability is '+ str(en))



