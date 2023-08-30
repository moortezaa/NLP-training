import math
import random
import numpy as np
import matplotlib.pyplot as plt

LEARNING_RATE = 0.1
REGULARIZATION_PENALTY = 0.7


def weightedSumOfEvidenceForClass(inputs: list[float], teta: list[float]) -> float:
    weighted = 0
    for i in range(len(inputs)):
        weighted += inputs[i] * teta[i]
    return weighted + teta[i + 1]


def sigmoid(z: float) -> float:
    return 1 / (1 + math.exp(-z))


def calculateProbability(inputs: list[float], teta: list[float]):
    return sigmoid(weightedSumOfEvidenceForClass(inputs, teta))


def calculateBinaryProbability(
    evidences: list[(float, float)], bias: float, decisionBoundary: float
) -> bool:
    return calculateProbability(evidences, bias) > decisionBoundary


def crossEntropyLoss(probability: float, goldLabel: float) -> float:
    return -(
        (goldLabel * math.log(probability))
        + ((1 - goldLabel) * math.log(1 - probability))
    )


def gradientForAFeature(probability: float, goldLabel: float, feature: float) -> float:
    return (probability - goldLabel) * feature


def gradient(probability: float, goldLabel: float, input: list[float]):
    gradient = []
    for feature in input:
        gradient.append(gradientForAFeature(probability, goldLabel, feature))
    return gradient


def StochasticGradientDescent(trainings: list[(list[float], float)]):
    lastLoss = None
    vectorSize = len(trainings[0][0])
    tetaVector = [0 for _ in range(vectorSize + 1)]
    while lastLoss > 0.0000001:
        for i in range(len(trainings)):
            training = trainings[random.randint(0, len(trainings) - 1)]
            probability = calculateProbability(training[0], tetaVector)
            lastLoss = crossEntropyLoss(probability, training[1])
            g = gradient(probability, training[1], training[0])
            # add new bias
            g.append(probability - training[1])
            for i in tetaVector:
                teta = tetaVector[i]
                tetaVector[i] = teta - LEARNING_RATE * g[i]
    return tetaVector


def getNodeOutput(input, weight):
    return input * weight


# can have a multi thread version of this function
def miniBatchGradintDesent(trainings: list[(list[float], float)], batchSize: int):
    lastLoss = 1
    vectorSize = len(trainings[0][0])
    tetaVector = [0 for _ in range(vectorSize + 1)]
    end = len(trainings) - 1 - batchSize
    si = None
    if end <= 0:
        si = 0
    else:
        si = random.randint(0, end)
    batch = trainings[si : si + batchSize]

    while lastLoss > 0.00001:
        lossSum = 0
        gradientSum = [0 for _ in range(vectorSize + 1)]
        probs = []
        for training in batch:
            probability = calculateProbability(training[0], tetaVector)
            probs.append(probability)
            lossSum += crossEntropyLoss(probability, training[1])
            g = gradient(probability, training[1], training[0])
            # add new bias
            g.append(probability - training[1])
            for i in range(len(gradientSum)):
                gras = gradientSum[i]
                gradientSum[i] = gras + g[i]
        lastLoss = lossSum / batchSize
        print("%.8f" % lastLoss, end="\r")
        for i in range(len(gradientSum)):
            g[i] = gradientSum[i] / batchSize

        for i in range(len(tetaVector)):
            teta = tetaVector[i]
            tetaVector[i] = teta - LEARNING_RATE * g[i]

    return tetaVector  # this is the weights that has been learned; why I named this teta vector?

def miniBatchGradintDesentWithVisualization(trainings: list[(list[float], float)], batchSize: int):
    lastLoss = 1
    vectorSize = len(trainings[0][0])
    tetaVector = [0 for _ in range(vectorSize + 1)]
    end = len(trainings) - 1 - batchSize
    si = None
    if end <= 0:
        si = 0
    else:
        si = random.randint(0, end)
    batch = trainings[si : si + batchSize]

    # creating initial data values
    # of x and y
    x = [0,1]
    x1 = np.linspace(0,1,batchSize)
    y = [getNodeOutput(x, tetaVector[0]) for x in x]

    # to run GUI event loop
    plt.ion()

    # here we are creating sub plots
    figure, ax = plt.subplots()
    ax.set_ylim([0,1])
    ax.plot(x1,[t[1] for t in trainings],'o')
    (line,) = ax.plot(x1, [0 for _ in x1])

    # setting title
    plt.title("probabilities for training data", fontsize=20)

    # setting x-axis label and y-axis label
    plt.xlabel("inputs")
    plt.ylabel("probs")

    while lastLoss > 0.00001:
        lossSum = 0
        gradientSum = [0 for _ in range(vectorSize + 1)]
        probs = []
        for training in batch:
            probability = calculateProbability(training[0], tetaVector)
            probs.append(probability)
            lossSum += crossEntropyLoss(probability, training[1])
            g = gradient(probability, training[1], training[0])
            # add new bias
            g.append(probability - training[1])
            for i in range(len(gradientSum)):
                gras = gradientSum[i]
                gradientSum[i] = gras + g[i]
        lastLoss = lossSum / batchSize
        print("%.8f" % lastLoss, end="\r")
        for i in range(len(gradientSum)):
            g[i] = gradientSum[i] / batchSize

        for i in range(len(tetaVector)):
            teta = tetaVector[i]
            tetaVector[i] = teta - LEARNING_RATE * g[i]

        # updating data values
        line.set_ydata(probs)

        # drawing updated values
        figure.canvas.draw()

        # This will run the GUI event
        # loop until all UI events
        # currently waiting have been processed
        figure.canvas.flush_events()

    return tetaVector

def miniBatchGradintDesentGeneralizedWithVisualization(trainings: list[(list[float], float)], batchSize: int):
    lastLoss = 1
    vectorSize = len(trainings[0][0])
    tetaVector = [0 for _ in range(vectorSize + 1)]
    end = len(trainings) - 1 - batchSize
    si = None
    if end <= 0:
        si = 0
    else:
        si = random.randint(0, end)
    batch = trainings[si : si + batchSize]

    # creating initial data values
    # of x and y
    x = [0,1]
    x1 = np.linspace(0,1,batchSize)
    y = [getNodeOutput(x, tetaVector[0]) for x in x]

    # to run GUI event loop
    plt.ion()

    # here we are creating sub plots
    figure, ax = plt.subplots()
    ax.set_ylim([0,1])
    ax.plot(x1,[t[1] for t in trainings],'o')
    (line,) = ax.plot(x1, [0 for _ in x1])

    # setting title
    plt.title("probabilities for training data", fontsize=20)

    # setting x-axis label and y-axis label
    plt.xlabel("inputs")
    plt.ylabel("probs")

    while lastLoss > 0.00001:
        lossSum = 0
        gradientSum = [0 for _ in range(vectorSize + 1)]
        probs = []
        for training in batch:
            probability = calculateProbability(training[0], tetaVector)
            probs.append(probability)
            lossSum += crossEntropyLoss(probability, training[1])
            g = gradient(probability, training[1], training[0])
            # add new bias
            g.append(probability - training[1])
            for i in range(len(gradientSum)):
                gras = gradientSum[i]
                gradientSum[i] = gras + g[i]
        lastLoss = lossSum / batchSize
        print("%.8f" % lastLoss, end="\r")
        for i in range(len(gradientSum)):
            g[i] = gradientSum[i] / batchSize

        for i in range(len(tetaVector)):
            teta = tetaVector[i]
            tetaVector[i] = teta - LEARNING_RATE * g[i]

        # updating data values
        line.set_ydata(probs)

        # drawing updated values
        figure.canvas.draw()

        # This will run the GUI event
        # loop until all UI events
        # currently waiting have been processed
        figure.canvas.flush_events()

    return tetaVector