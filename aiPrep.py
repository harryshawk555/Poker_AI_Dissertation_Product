from initialize import *
from handCheck import Check
from MultiCheck import MultiCheck
from MultiCheck import Hand
from ShowdownCalc import *
from scipy.special import comb
from joblib import Parallel, delayed
from itertools import combinations, chain
from numba import jit, njit, types, typeof, typed, cuda, config, threading_layer
from numba.experimental import jitclass
from threading import Thread
import timeit
import math
import cupy as cp
import numba.cuda as cuda
import numpy as np
import random
import math
#import multiprocessing
import torch.multiprocessing as tm

global MultiShowdown


def handRankAiCalcsPreFlop(Deck):

    handCombList = []
    handAbsValue = []
    draws = 0
    wins = 0

    for i in range(0,len(Deck)-1):
        for j in range(i+1, len(Deck)):
            
            potHand = [Deck[i],Deck[j]]
            chenScore = math.ceil(chen_formula(potHand))
            HandScore = [potHand,chenScore]
            handCombList.append(HandScore)
    
    handCombList.sort(key=lambda x: x[1], reverse=True)

    for i in range(0,len(handCombList)-1):
        for j in range(0, len(handCombList)-1):
            if handCombList[i][1] > handCombList[j][1]:
                wins += 1
            elif handCombList[i][1] == handCombList[j][1]:
                draws +=1
        absVal = wins + ((draws - 1)/2)
        handAbsValue.append([handCombList[i][0],absVal])
        wins = 0
        draws = 0
    return handAbsValue

def indexer(list, filter):
    count = 0 
    for x in list:
        if x[0] == filter:
            return count
        else:
            count += 1

def indexerB(list, filter):
    count = 0 
    for x in list:
        if x[0][0].name == filter[0].name and x[0][1].name == filter[1].name:
            return count
        else:
            count += 1

def handRankAiCalcsPostFlop(board,Deck):
    global handCheck
    global handWinLoss
    global total_it
    global handAbsValue

    handCombList = []
    handAbsValue = []
    lenb = len(board)
    if lenb == 5:
        lend = 1081
    elif lenb == 4:
        lend = 1128
    elif lenb == 3:
        lend = 1176
    else:
        lend = 1081
    handWinLoss = np.empty((lend,3), dtype=object)
    handCheck = []
    fullHand = []
    fullHands = []
    index = 0

    for i in range(0,len(Deck)-1):
        if board.count(Deck[i])!=1:
            for j in range(i+1, len(Deck)):
                if board.count(Deck[j])!=1:
                    fullHand = []
                    for k in board:
                        fullHand.append(k)
                    fullHand.append(Deck[i])
                    fullHand.append(Deck[j])
                    currHand = [Deck[i],Deck[j]]
                    handCombList.append(currHand)
                    handWinLoss[index,0] = currHand
                    handWinLoss[index,1] = 0
                    handWinLoss[index,2] = 0
                    fullHands.append([fullHand,currHand])
                    if index < lend:
                        index += 1
    
    handCheck = MultiCheck(fullHands)


    
    total_it = (len(handCheck)*((len(handCheck)-1)))/2

    #sTime = timeit.default_timer()
    multiHandRankV2(handCheck)
    for i in range(0,len(handWinLoss)):
        absVal = handWinLoss[i][1] + (handWinLoss[i][2]/2)
        handAbsValue.append((handWinLoss[i][0],absVal)) 
    #stop = timeit.default_timer()
    #print('Time :', stop-sTime)

    return handAbsValue   

def chen_formula(hand):
    gap = 0
    suited = 0

    high_card = max(hand, key=lambda x: x.value + x.modif)
    if high_card.value == 1:
        basePoint = 10
    elif high_card.value == 13:
        basePoint = 8
    elif high_card.value == 12:
        basePoint = 7
    elif high_card.value == 11:
        basePoint = 6
    else:
        basePoint = high_card.value/2

    if hand[0].value + hand[0].modif == hand[1].value + hand[1].modif:
        basePoint = basePoint*2
        if basePoint < 5:
            basePoint = 5
    elif abs((hand[0].value + hand[0].modif) - (hand[1].value + hand[1].modif)) == 1:
        gap = 0
    elif abs((hand[0].value + hand[0].modif) - (hand[1].value + hand[1].modif)) == 2:
        gap = 1
    elif abs((hand[0].value + hand[0].modif) - (hand[1].value + hand[1].modif)) == 3:
        gap = 2
    elif abs((hand[0].value + hand[0].modif) - (hand[1].value + hand[1].modif)) == 4:
        gap = 4
    else:
        gap = 5

    if (gap == 1 or gap == 2) and high_card.value + high_card.modif < 12:
        gap -= 1

    if hand[0].name[1]== hand[1].name[1]:
        suited = 2

    chen_score = basePoint+suited-gap
    
    return chen_score

def bucketing(handAbsValue, k):
    # Step 1: Create k centroid points in the interval between the minimum and maximum hand values.
    min_val = min(handAbsValue, key=lambda x: x[1])[1]
    max_val = max(handAbsValue, key=lambda x: x[1])[1]
    centroids = [random.uniform(min_val, max_val) for _ in range(0,k)]
    
    while True:
        # Step 2: Assign each hand to the nearest centroid.
        clusters = [[] for _ in range(0,k)]
        for hand in handAbsValue:
            distances = [abs(hand[1] - centroid) for centroid in centroids]
            cluster_index = distances.index(min(distances))
            clusters[cluster_index].append(hand)
        
        # Step 3: Adjust each centroid to be the mean of their assigned hand values.
        new_centroids = []
        for cluster in clusters:
            if len(cluster) > 0:
                values = [hand[1] for hand in cluster]
                new_centroid = sum(values) / len(values)
                new_centroids.append(new_centroid)
            else:
                new_centroids.append(0)
        
        # Check for convergence
        if math.isclose(sum(new_centroids), sum(centroids)):
            break
        
        centroids = new_centroids
    
    # Step 4: Return the clusters with their assigned hands
    clusters = [[] for _ in range(0,k)]
    for hand in handAbsValue:
        distances = [abs(hand[1] - centroid) for centroid in centroids]
        cluster_index = distances.index(min(distances))
        clusters[cluster_index].append(hand)
    
    Final_Clusters = []
    Final_Centroids = []
    for i in range(0, len(clusters)-1):
        if clusters[i] != []:
            Final_Centroids.append(centroids[i])
            Final_Clusters.append(clusters[i])
   
    return Final_Clusters,Final_Centroids

def postBucketing(handAbsValue, k):
    # Step 1: Create k centroid points in the interval between the minimum and maximum hand values.
    min_val = min(handAbsValue, key=lambda x: x[1])[1]
    max_val = max(handAbsValue, key=lambda x: x[1])[1]
    centroids = [random.uniform(min_val, max_val) for _ in range(0,k)]
    
    while True:
        # Step 2: Assign each hand to the nearest centroid.
        clusters = [[] for _ in range(0,k)]
        for hand in handAbsValue:
            distances = [abs(hand[1] - centroid) for centroid in centroids]
            cluster_index = distances.index(min(distances))
            clusters[cluster_index].append(hand)
        
        # Step 3: Adjust each centroid to be the mean of their assigned hand values.
        new_centroids = []
        for cluster in clusters:
            if len(cluster) > 0:
                values = [hand[1] for hand in cluster]
                new_centroid = sum(values) / len(values)
                new_centroids.append(new_centroid)
            else:
                new_centroids.append(0)
        
        # Check for convergence
        if math.isclose(sum(new_centroids), sum(centroids)):
            break
        
        centroids = new_centroids
    
    # Step 4: Return the clusters with their assigned hands
    clusters = [[] for _ in range(0,k)]
    for hand in handAbsValue:
        distances = [abs(hand[1] - centroid) for centroid in centroids]
        cluster_index = distances.index(min(distances))
        clusters[cluster_index].append(hand)

    Final_Clusters = []
    Final_Centroids = []
    for i in range(0, len(clusters)-1):
        if clusters[i] != []:
            Final_Centroids.append(centroids[i])
            Final_Clusters.append(clusters[i])
   
    return Final_Clusters,Final_Centroids


def optimBucket2(cluster,absValList):
    K2 = 800
    MAX = 100
    clusters = []
    ci = np.zeros((20,MAX-1))
    pi = np.zeros(20)
    xi = np.zeros((20,MAX))    
    for i in range(0, len(cluster[0])-1):
        if len(cluster[0][i]) > 0:
            error = 0 
            currCluster = cluster[0][i]
            pro = len(cluster[0][i])
            pi[i] = (pro/1326)  # compute probability of getting dealt a hand in parent i
            for k in range(1, MAX-2):
                clusters = postBucketing(currCluster, k)
                distances = clusters[1]
                for j in distances:
                    error += j**2
                ci[i,k-1] = error*pi[i]
    xi_indexList = []
    xi_ErrorList = np.min(ci, axis=1)
    for i in range(0,len(ci)-1):
        for j in range(0, len(ci[i])-1):
            if np.any(ci[i,j] == xi_ErrorList[i]) and sum(xi_indexList) < K2:  
                xi_indexList.append(j)

    return sum(xi_indexList)+len(xi_indexList)

def MAIN():
    global Deck
    sTime = timeit.default_timer()
    Deck = Initialize()
    board = random.sample(Deck, 5)
    AiPreInputs = bucketing(handRankAiCalcsPreFlop(), 9)
    AiHandAnal = handRankAiCalcsPostFlop(board)
    AiPostInputs = bucketing(AiHandAnal, optimBucket2(AiPreInputs,AiHandAnal))
    #print(AiPreInputs)
    stop = timeit.default_timer()
    print('Time :', stop-sTime)
    print(AiPostInputs)
    count = 0

def multiHandRank():
    global Deck
    global handCheck
    global handWinLoss
    global total_it
    global handAbsValue
    global allShowdowns
    global cores
    global threadIndexes
    global MultiShowdown
    global MultiCheck
    global Initialize
    global Hand

    #Change this, work on a scoring system and will speed it up significantly
    cores = 2
    process = []
    dt = np.dtype((object))
    allShowdowns = np.fromiter(combinations(handCheck,2),dt)
    threadCountsDiff = round(len(allShowdowns)/cores)
    threadIndexes = []
    for i in range(0,len(allShowdowns)-1,threadCountsDiff):
        threadIndexes.append([i,i+threadCountsDiff-1])
    if threadCountsDiff * cores > len(allShowdowns):
        err = (threadCountsDiff * cores) - len(allShowdowns)
        threadIndexes[len(threadIndexes)-1][1] = len(allShowdowns)-1



    handWinLoss = MultiShowdown(allShowdowns,handWinLoss)
    tm.set_start_method('spawn')
    queue = tm.Queue()
    queue.put(allShowdowns)
    queue.put(handWinLoss)
    handled = []
    with tm.Pool(cores-1) as pool:
        for i in range(0, len(threadIndexes)):
            handle = pool.map_async(MultiShowdown(threadIndexes[i][0], threadIndexes[i][1]),range(0))            
            handled.append(handle.get())
        
            
                
    #Parallel(n_jobs=800,prefer="threads")(delayed(MultiShowdown)(threadIndexes[j-1][0],threadIndexes[j-1][1])for j in range(0,len(threadIndexes)-1))


config.THREADING_LAYER = 'threadsafe'

#@njit(parallel=True)
#@np.fuse()
def MultiShowdown(start, finish):
    count = 0
    showdownResult = ''


    for showdowns in range(start,finish):
        aHandEnum = allShowdowns[showdowns][0][0]
        bHandEnum = allShowdowns[showdowns][1][0]
        if aHandEnum[0].value > bHandEnum[0].value:
            showdownResult = 'a'
        elif aHandEnum[0].value < bHandEnum[0].value:
            showdownResult = 'b'
        else:
            valListA = np.zeros(5)
            valListB = np.zeros(5)
            count = 0
            for card in aHandEnum[1]:
                valListA[count] = card.value+card.modif
                count+=1
            count = 0
            for card in bHandEnum[1]:
                valListB[count] = card.value+card.modif
                count+=1
            count = 0
            if np.all(valListA == valListB):
                showdownResult = 'chop'
            
            np.sort(valListA)
            np.sort(valListB)
            aMode = statistics.mode(valListA)
            bMode = statistics.mode(valListB)
            aMMode = statistics.multimode(valListA)
            bMMode = statistics.multimode(valListB)
            aMMode.sort(reverse=True)
            bMMode.sort(reverse=True)


            if aHandEnum[0].value == 9 or aHandEnum[0].value == 5:
                if np.min(valListA[0:4]) == 2 and np.max(valListA) == 14:
                    valListA = np.array([1,2,3,4,5])
                if np.min(valListB) == 2 and np.max(valListB) == 14:
                    valListB = np.array([1,2,3,4,5])
                if np.max(valListA) > np.max(valListB):
                    showdownResult = 'a'
                elif np.max(valListA) < np.max(valListB):
                    showdownResult = 'b'
                else:
                    showdownResult = 'chop'
            
            if aHandEnum[0].value == 8 or aHandEnum[0].value == 7:
                if aMode > bMode:
                    showdownResult = 'a'
                elif aMode<bMode:
                    showdownResult = 'b'
                else:
                    
                    aKicker = np.sum(np.where(np.count_nonzero(valListA) == 1, valListA,0))
                    bKicker = np.sum(np.where(np.count_nonzero(valListB) == 1, valListB,0))
                    if aKicker > bKicker:
                        showdownResult = 'a'
                    elif aKicker < bKicker:
                        showdownResult = 'b'
                    else:
                        showdownResult = 'chop'
            
            if aHandEnum[0].value == 6 or aHandEnum[0].value == 1:
                for i in range(0, len(valListA)-1):
                    if valListA[i] > valListB[i]:
                        showdownResult = 'a'
                    elif valListA[i] < valListB[i]:
                        showdownResult = 'b'
                showdownResult = 'chop'

            if aHandEnum[0].value == 2 or aHandEnum[0].value == 4:
                if aMode > bMode:
                    showdownResult = 'a'
                elif aMode<bMode:
                    showdownResult = 'b'
                else:
                    valListA.sort()
                    valListB.sort()
                    NewValListA = np.zeros(3)
                    NewValListB = np.zeros(3)
                    count = 0
                    for i in valListA:
                        if np.count_nonzero(valListA == i) <1 and i != aMode:
                            NewValListA[count] =  i
                            count +=1
                    count = 0
                    for i in valListB:
                        if np.count_nonzero(valListB == i) <1 and i != aMode:
                            NewValListB[count] = i
                            count += 1
                    for i in range(0, len(NewValListA)-1):
                        if NewValListA[i] > NewValListB[i]:
                            showdownResult = 'a'
                            break
                        elif NewValListA[i] < NewValListB[i]:
                            showdownResult = 'b'
                            break
                        else:
                            if i == len(NewValListA)-1:
                                showdownResult = 'chop'
                
            if aHandEnum[0].value == 3:
                aMMode.sort(reverse=True)
                bMMode.sort(reverse=True)
                if aMMode[0]>bMMode[0]:
                    showdownResult = 'a'
                elif aMMode[0]<bMMode[0]:
                    showdownResult = 'b'
                else:
                    if aMMode[1] > bMMode[1]:
                        showdownResult = 'a'
                    elif aMMode[1] < bMMode[1]:
                        showdownResult = 'b'
                aKicker = np.sum(np.where(np.count_nonzero(valListA) == 1, valListA,0))
                bKicker = np.sum(np.where(np.count_nonzero(valListB) == 1, valListB,0))
                if aKicker > bKicker:
                    showdownResult = 'a'
                elif aKicker < bKicker:
                    showdownResult = 'b'
                else:
                    showdownResult = 'chop'

        
                
        if showdownResult == 'a':
            handWinLoss[int(allShowdowns[showdowns][1][2])][1] += 1
        elif showdownResult == 'chop':
            handWinLoss[int(allShowdowns[showdowns][1][2])][2] +=1
            handWinLoss[int(allShowdowns[showdowns][0][2])][2] +=1
        elif showdownResult == 'b':
            handWinLoss[int(allShowdowns[showdowns][0][2])][1] +=1

        count+=1
        print(count)
    print('Done')    
    return handWinLoss

def multiHandRankV2(handCheck):
    global handWinLoss
    for i in range(0, len(handCheck)):
        for j in range(i, len(handCheck)):
            if handCheck[i,0][3] > handCheck[j,0][3]:
                handWinLoss[int(handCheck[i,2])][1] += 1
            elif handCheck[i,0][3] == handCheck[j,0][3]:
                handWinLoss[int(handCheck[i,2])][2] += 1
                handWinLoss[int(handCheck[j,2])][2] += 1
            else:
                handWinLoss[int(handCheck[j,2])][1] += 1


def comb_index(n, k):
    count = comb(n, k, exact=True)
    index = np.fromiter(chain.from_iterable(combinations(range(n), k)), int, count=count*k)
    return index.reshape(-1, k)

def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

#@cuda.jit




if __name__ == '__main__':
    MAIN()