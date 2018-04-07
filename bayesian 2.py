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
    edge = line.replace('\n', '').replace(' ', '').split(',')

    if c == 2:
        edge = line.replace('\n','').replace(' ','').split(',')
        bn[edge[1]][0].append(edge[0])
    if c == 3:
        event, prob = line[2:-1].split(')=')
        prob = float(prob)
        event = [[s.split('=') for s in e.split(',')]
                 for e in event.split('|')]
        [[var, val]] = event[0]
        parent = [] if len(event) == 1 else event[1]
        parent_vals = tuple(v[1] for v in parent)
        if var not in bn:
            bn[var] = [[p for p,_ in parent], {}]

        bn[var][1][parent_vals] = prob


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
        for i in range(len(r)):
            e[r[i].split('=')[0]] = r[i].split('=')[1]
        # e[r[1].split('=')[0]] = r[1].split('=')[1]

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
    parent, parent_prob = bn[Y]
    parent_vals = tuple(e[i] for i in parent)
    return parent_prob[parent_vals]


en = enumeration_ask(X, e)
print('The probability is '+ str(en))



