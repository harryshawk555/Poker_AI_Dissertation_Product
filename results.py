import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

aidata = pd.read_csv('aiTestOutcomes.csv')
rdata = pd.read_csv('controlTestOutcomes.csv')

ainp = aidata.to_numpy()
rnp = rdata.to_numpy()

aiBigX = []
aiBigY = []
aiCumu = 0
ai1 = 0
ai2 = 0
ai3 = 0
ai4 = 0
aiSplit = 0

rnBigX = []
rnBigY = []
rnCumu = 0
rn1 = 0
rn2 = 0
rn3 = 0
rn4 = 0
rnSplit = 0


for i in range(0, len(ainp)):
    if ainp[i,1] == 0:
        ai1 += 1
    elif ainp[i,1] == 1:
        ai2 += 1
    elif ainp[i,1] == 2:
        ai3 += 1
    elif ainp[i,1] == 3:
        ai4 += 1
        aiCumu += 1
        aiBigY.append(aiCumu)
        aiBigX.append(i)
    else:
        aiSplit += 1

    if rnp[i,1] == 0:
        rn1 += 1
    elif rnp[i,1] == 1:
        rn2 += 1
    elif rnp[i,1] == 2:
        rn3 += 1
    elif rnp[i,1] == 3:
        rnCumu += 1
        rnBigY.append(rnCumu)
        rnBigX.append(i)
        rn4 += 1
    else: 
        rnSplit += 1

print(ai1,
ai2,
ai3,
ai4,
aiSplit, '\n',
rn1,
rn2,
rn3,
rn4,
rnSplit,
)

plt.plot(aiBigX, aiBigY)
plt.plot(rnBigX, rnBigY)

plt.xlabel('Iterations')
plt.ylabel('Number of Big Wins')
plt.title('Big Wins Over Time')
plt.legend(labels=['AI', 'Random'])

plt.show()

X = np.arange(4)
WinType = ('Big Loss', 'Small Loss', 'Small Win', 'Big Win')
aiBar = [ai1, ai2, ai3, ai4]
rnBar = [rn1, rn2, rn3, rn4]
plt.bar(X+0.00, rnBar, color = 'b', width = 0.33)
plt.bar(X+0.33, aiBar, color = 'g', width = 0.33)
plt.ylabel('Number of Occurances')
plt.title('Win Assessments of Random and AI Agents')
plt.xticks(X, WinType)
plt.yticks(np.arange(0, 8000, 1000))
plt.legend(labels=['Random', 'AI'])

plt.show()

