import math
import re
from Utils import *


def TrainNaiveBayes(
    documents: list, classifications: list, smoothing: int = 1
) -> (dict, dict, list):
    logPerior = {}
    logLikelihood = {}
    for c in classifications:
        nDoc = len(documents)
        cDocs = list(filter(lambda d: d["goldTag"] == c, documents))
        nC = len(cDocs)
        logPerior[c] = math.log(nC / nDoc)
        dVocab = []
        for d in documents:
            for w in d["text"].split(" "):
                if w not in dVocab:
                    dVocab.append(w)

        bigDoc = ""
        for d in cDocs:
            if len(bigDoc) > 0:
                bigDoc += " "
            bigDoc += d["text"]
        start = datetime.datetime.now()
        for i in range(len(dVocab)):
            w = dVocab[i]
            countWC = len(re.findall(w, bigDoc))
            countC = len(bigDoc.split(" "))
            logLikelihood[w, c] = math.log(
                (countWC + smoothing) / (countC + smoothing * len(dVocab))
            )
            showProgress(i, dVocab, start)
        print()
    return (logPerior, logLikelihood, dVocab)


def TrainBinaryNaiveBayes(
    documents: list, classifications: list, smoothing: int = 1
) -> (dict, dict, list):
    logPerior = {}
    logLikelihood = {}
    for c in classifications:
        nDoc = len(documents)
        cDocs = list(filter(lambda d: d["goldTag"] == c, documents))
        nC = len(cDocs)
        logPerior[c] = math.log(nC / nDoc)
        dVocab = []
        for d in documents:
            for w in d["text"].split(" "):
                if w not in dVocab:
                    dVocab.append(w)

        bigDoc = ""
        for d in cDocs:
            if len(bigDoc) > 0:
                bigDoc += " "
            bigDoc += d["text"]
        start = datetime.datetime.now()
        for i in range(len(dVocab)):
            w = dVocab[i]
            countWC = 0
            if re.match(w, bigDoc) != None:
                countWC = 1

            countC = len(bigDoc.split(" "))
            logLikelihood[w, c] = math.log(
                (countWC + smoothing) / (countC + smoothing * len(dVocab))
            )
            showProgress(i, dVocab, start)
        print()
    return (logPerior, logLikelihood, dVocab)


def TestNaiveBayes(
    testDoc: str,
    trainingData: (dict, dict),
    classifications: list,
):
    sum = {}
    for c in classifications:
        sum[c] = trainingData[0][c]
        for w in testDoc.split(" "):
            if w in trainingData[2]:
                sum[c] = sum[c] + trainingData[1][w, c]
        # print(f'{c}: {AntilogProbability(sum[c])}')
    return max(sum, key=sum.get)


def NormalizeForBayes(text: str):
    text = text.lower()
    negations = ["n’t", "n't", "n`t", "not", "no", "never"]
    for neg in negations:
        try:
            start = text.index(neg)
            # finding closest punctuation
            punctuations = [",", ".", ";", ":"]
            end = 0
            for p in punctuations:
                try:
                    i = text.index(p, start)
                except:
                    continue
                if i < end:
                    end = i
            if end <= start:
                end = len(text)
            start = start + len(neg)
            sub = text[start:end]
            words = sub.split(" ")
            newSub = " NOT_".join(words)
            text = text.replace(sub, newSub, 1)
        except:
            continue
    return text


def NormalizeDocuments(docs: list):
    for d in docs:
        d["text"] = NormalizeForBayes(d["text"])
    return docs


def PrintTrainingData(trainingData):
    print("%15s" % "", end="\t")
    for c in trainingData[0]:
        print("%8s" % c, end="\t")
    print()
    for w in trainingData[2]:
        print("%15s" % w, end="\t")
        for c in trainingData[0]:
            print("%.8f" % AntilogProbability(trainingData[1][w, c]), end="\t")
        print()


def GetProbabilityInClass(
    text: str, classification: str, trainingData: (dict, dict, list)
):
    sum = trainingData[0][classification]
    for w in text.split(" "):
        if w in trainingData[2]:
            sum = sum + trainingData[1][w, classification]
    return AntilogProbability(sum)


def PrintConfusionMatrix(testData, trainingData):
    testResult = {
        "true positive": 0,
        "false positive": 0,
        "true negative": 0,
        "false negative": 0,
    }
    for test in testData:
        r = TestNaiveBayes(
            NormalizeForBayes(test["text"]), trainingData, [c for c in trainingData[0]]
        )
        if r == "-":
            if r == test["goldLabel"]:
                testResult["true negative"] += 1
            else:
                testResult["false negative"] += 1
        else:
            if r == test["goldLabel"]:
                testResult["true positive"] += 1
            else:
                testResult["false positive"] += 1
    print("%15s" % "", "%14s" % "gold positive", "%14s" % "gold negative")
    print(
        "%15s" % "system positive",
        "\033[42m%14d\033[0m" % testResult["true positive"],
        "%14d" % testResult["false positive"],
        "\tpercision:",
        GetPercision(testResult),
    )
    print(
        "%15s" % "system negative",
        "%14d" % testResult["false negative"],
        "\033[42m%14d\033[0m" % testResult["true negative"],
    )
    print(
        "%15s" % "",
        "%14s" % "recall:",
        "%14d" % GetRecall(testResult),
        "\t accuracy:",
        GetAccuracy(testResult),
    )
    return testResult


def GetPercision(testResult):
    return testResult["true positive"] / (
        testResult["true positive"] + testResult["false positive"]
    )


def GetRecall(testResult):
    return testResult["true positive"] / (
        testResult["true positive"] + testResult["false negative"]
    )


def GetAccuracy(testResult):
    return (testResult["true negative"] + testResult["true positive"]) / (
        testResult["false negative"]
        + testResult["false positive"]
        + testResult["true negative"]
        + testResult["true positive"]
    )


def GetFMeasure(testResult, beta):
    p = GetPercision(testResult)
    r = GetRecall(testResult)
    return ((beta+1)*p*r)/(((beta**2)*p)+r)