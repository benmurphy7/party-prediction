import sys
import csv
from decimal import *

train_file = sys.argv[1]
test_file = sys.argv[2]


# Counts for individual votes (last entry is party which is ignored)
RY=[1]*43
RN=[1]*43
DY=[1]*43
DN=[1]*43

count = 0
R_count = 0
D_count = 0

# Load training data
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
    count+=1

#Load test data
test = csv.reader(open(test_file, newline=''), delimiter=',')
for row in test:
    Dem = 1
    Rep = 1

    # P(Party)
    PR = R_count / (R_count + D_count)
    PD = 1 - PR

    count = 0

    for i in range(0,42):
        vote = False
        # Total of all counted votes
        VoteSum = RY[i] + DY[i] + RN[i] + DN[i]

        # Check the product math here...
        getcontext().prec = 128
        # 1/P(Vote)*P(Vote|Party)*P(Party)
        if row[i] == "Yea":
            RP = Decimal( (1/( (RY[i]+DY[i])/VoteSum )) * (RY[i]/(RY[i] + RN[i])) )
            DP = Decimal( (1/( (RY[i]+DY[i])/VoteSum )) * (DY[i]/(DY[i] + DN[i])) )
            vote = True
        elif row[i] == "Nay":
            RP = Decimal( (1/( (RN[i]+DN[i])/VoteSum )) * (RN[i]/(RY[i] + RN[i])) )
            DP = Decimal( (1/( (RN[i]+DN[i])/VoteSum )) * (DN[i]/(DY[i] + DN[i])) )
            vote = True
        if vote==True:
            count+=1
            Dem = Decimal(Dem * DP)
            Rep = Decimal(Rep * RP)
            #print("Dem: %.6f" % DP)
            #print("Rep: %.6f" % RP)
        #else:
            #print("No Vote")
    #print("Dem:  ,%s" % Dem)
    #print("Rep:  ,%s" % Rep)
    #Dem = Dem * Decimal(PD)
    Rep = Rep * Decimal(PR)
    Dem = Dem * Decimal(PD)
    Total = Decimal(Dem + Rep)
    Dem = Dem/Total
    Rep = Rep/Total

    #Currently using average probability of individual votes
    if (Dem>Rep):
        print("Democrat,%.15f" % Dem)
        #print("Democrat,%f" % DS)
    else:
        print("Republican,%.15f" % Rep)
        #print("Republican,%f" % RS)





