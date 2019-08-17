import sys
import csv
from decimal import *
import math

class Node(object):
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = []

    def add_child(self, obj):
        self.children.append(obj)

    def add_parent(self, obj):
        self.parent.append(obj)


train_file = sys.argv[1]
test_file = sys.argv[2]


# Counts for individual votes (last entry is party which is ignored)
RY=[1]*43
RN=[1]*43
DY=[1]*43
DN=[1]*43
D_count = 0
R_count = 0

# Load training data (map out decision tree)
data = csv.reader(open(train_file, newline=''), delimiter=',')
for row in data:
    i = 0
    if(row[42]) == 'Democrat':
        D_count += 1
        for vote in row:
            if vote=="Yea":
                DY[i] +=1
            elif vote=="Nay":
                DN[i] +=1
            i+=1
    elif(row[42]) == 'Republican':
        R_count += 1
        for vote in row:
            if vote == "Yea":
                RY[i] += 1
            elif vote == "Nay":
                RN[i] += 1
            i+=1
    else:
        print("Invalid party!")



divider = []
importance = []
Total_count = R_count + D_count

# Just a test - choosing importance by difference in counts
for x in range (0,42):
    dif = abs(RY[x]+DY[x]-RN[x]-DN[x])
    divider.append([dif,x])

# Sort by difference, decreasing
divider.sort(key=lambda x: x[0], reverse=True)

#print(divider)

"""

    P = D
    N = R
    PN = D_count + R_count
    q = D_count / D_count + R_count
    H(Goal) = -(qlog2q+(1-q) log2 (1-q))
    Remainder = DY + RY/ PN * B(DY/DY+RY)


"""
def Bq(P,N):
    q = P/(P+N)
    bq = -1 *(q * math.log2(q) + (1 - q) * math.log2(1-q))
    bq = math.log2(q)
    return bq
def Remainder(Pk,Nk):
    remainder = ((Pk+Nk)/Total_count)*Bq(Pk,Nk)
    return remainder

Goal = Bq(D_count, R_count)

for x in range (0,42):
    Rem = Remainder(DY[x],RY[x]) + Remainder(DN[x],RN[x])
    Gain = Goal - Rem
    importance.append([Gain,x])

importance.sort(key=lambda x: x[0], reverse=True)
#print(importance)

""" dec_tree = dict()
dec_tree["Root"] = "Root"
# dec_tree[child_id] = parent_id"""

#Test between divider and importance for ordering
choice = importance
expand = []

# Build dec tree
root = Node("Root")
data = csv.reader(open(train_file, newline=''), delimiter=',')
for row in data:
    expand.append(root)
    parent = root
    # Add most important votes first
    for item in choice: #[bits,vote num]
        new_child = True
        num = item[1] # The vote number (attribute)
        vote = row[num]
        if vote == "Yea" or vote == "Nay":
            tag = vote
        else:
            tag = "Other"

        for c in parent.children:
            if c.data == tag:
                child = c
                new_child = False
                break
        if new_child:
            child = Node(tag)
            parent.add_child(child)
            child.add_parent(parent)

        parent = child

    # Add leaf node
    child = Node(row[42])
    parent.add_child(child)
    child.add_parent(parent)

# Finds probability of all paths combined given root
def tree_prob(t_root):
    r_count = 0
    d_count = 0
    explore = []
    explore.append(t_root)

    while len(explore)>0:
        par = explore.pop(0)

        for chi in par.children:
            if chi.data == "Republican":
                r_count += 1
            elif chi.data == "Democrat":
                d_count += 1
            else:
                explore.append(chi)


    results = [d_count,r_count]
    return results
# Use decision tree on test data
path = []
test = csv.reader(open(test_file, newline=''), delimiter=',')
for row in test:
    parent = root
    prediction = ''
    confidence = 0
    R_count = 0
    D_count = 0
    done = False

    for item in choice:
        found = False
        num = item[1]
        vote = row[num]
        #print(num)
        path.append(parent)
        if vote == "Yea" or vote == "Nay":
            tag = vote
        else:
            tag = "Other"

        for c in parent.children:
            test_child = c
            if c.data == tag:
                child = c
                parent = child
                found = True
                break

        # Option not mapped
        if not found:
            break
            #parent = test_child
            #print("vote not found")

    for c in parent.children:
        if c.data == "Republican" or c.data == "Democrat":
            party = c.data
            confidence = 1
            done = True
    if not done:

        res = tree_prob(path.pop())
        if res[0] == 0 and res[1] == 0:
            tree_prob(path.pop)

        #[d_count,r_count]
        if(res[0]>=res[1]):
            party = "Democrat"
            confidence = res[0]/(res[0]+res[1])

        else:
            party = "Republican"
            confidence = res[1]/(res[0]+res[1])

    print("%s,%.15f" % (party,confidence))














