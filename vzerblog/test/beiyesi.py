#!/usr/bin/env python
#coding=utf-8
__author__ = 'vzer'
import  csv
import  random
import math

def loadCsv(filename):
    lines=csv.reader(open(filename,"rb"))
    dataset=[]
    for i in lines:
        dataset.append(float("".join(i)))
    return dataset

def splitDataset(dataset, splitRatio):
    trainSize=int(len(dataset)*splitRatio)
    trainSet=[]
    copy=list(dataset)
    while len(trainSet)<trainSize:
        index=random.randrange(len(copy))
        trainSet.append(copy.pop(index))
    return [trainSet,copy]

def mean(numbers):
    return sum(numbers)/float(len(numbers))

def stdev(numbers):
    avg=mean(numbers)
    variance=sum([pow((x-avg),2) for x in numbers])/float(len(numbers)-1)
    return math.sqrt(variance)

def summarize(dataset):
	summaries = [(mean(attribute), stdev(attribute)) for attribute in zip(*dataset)]
	del summaries[-1]
	return summaries

if __name__ == '__main__':
    filename="Spready1601p1601.csv"
    dataset =loadCsv(filename)
    print ("Loaded data file {0} with {1} rows".format(filename,len(dataset)))

    #huafen
    splitRatio=0.67
    train,test=splitDataset(dataset,splitRatio)
    print("Split {0} rows into train with {1} and test with {2}".format(len(dataset),len(train),len(test)))
    #summary = summarize(dataset)
    #print('Attribute summaries: {0}').format(summary)
    print("sumary of train: mean={0},stdev={1}".format(mean(train),stdev(train)))