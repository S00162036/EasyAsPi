# Example of kNN implemented from Scratch in Python

import csv
import random
import math
import operator
#from DataBaseConnect import SendData
from TestExecJS import SendToDB
from WriteToCSV import WriteToCSV

#Load the training data... no need for the testSet or split anymore as data is being passed in... too tired to remove anymore 
def loadDataset(filename, split, trainingSet=[] , testSet=[]):
	with open(filename, 'rb') as csvfile:
	    lines = csv.reader(csvfile)
	    dataset = list(lines)
	    for x in range(len(dataset)-1):
	        for y in range(2):
	            dataset[x][y] = float(dataset[x][y])
            #Randomly assign objects to the trainingSet array, and the rest to the testSet... again no need anymore
	        if random.random() < split:
	            trainingSet.append(dataset[x])
	        else:
	            testSet.append(dataset[x])

#Get the distance between the testPoint and the nearest trainingData
def euclideanDistance(instance1, instance2, length):
	distance = 0
	for x in range(length):
		distance += pow((instance1[x] - instance2[x]), 2)
	return math.sqrt(distance)

#Find the k nearest neighbours - Obviously - using our distance measurer above, and return the neighbours that most closely match our testData
def getNeighbors(trainingSet, testInstance, k):
	distances = []
	length = len(testInstance)-1
	for x in range(len(trainingSet)):
		dist = euclideanDistance(testInstance, trainingSet[x], length)
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

#Let each neighbour "Vote" for what the testData is - what's the most common object returned
def getResponse(neighbors):
	classVotes = {}
	for x in range(len(neighbors)):
		response = neighbors[x][-1]
		if response in classVotes:
			classVotes[response] += 1
		else:
			classVotes[response] = 1
	sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]

#Literally check how many times our predicted result Name matches the actual Name... kinda pointless for a single input, but great for lots
def getAccuracy(testSet, predictions):
	correct = 0
	for x in range(len(testSet)):
		if testSet[x][-1] == predictions[x]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0

#Actually pull everything together, This is where all our coin info will be sent
def main(heightIn, weightIn):
	# prepare data
	trainingSet=[]
    #The hardCoded values below will be variables we pass in from the physical device
	testSet=[[heightIn, weightIn,"E.50"]] #The label here is to test against the accuracy
	split = 30
	loadDataset('test.Data.txt', split, trainingSet, testSet)
	print 'Train set: ' + repr(len(trainingSet))
	print 'Test set: ' + repr(len(testSet))
	# generate predictions
	predictions=[]
	k = 3
	for x in range(len(testSet)):
		neighbors = getNeighbors(trainingSet, testSet[x], k)
		result = getResponse(neighbors)
		predictions.append(result)
		print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
	accuracy = getAccuracy(testSet, predictions)
	#SendData(result, heightIn, weightIn)
	WriteToCSV(weightIn, heightIn, result)
	SendToDB(result)
	return(result)
	print('Accuracy: ' + repr(accuracy) + '%')

	
#inWeight = input("Weight : ")
#inHeight = input("Height : ")
#Execute the main method, will be passing in variables here
#main(inHeight, inWeight)#24.16,7.89)