import math
import datetime


def CalcProbabilities(N: int, corpus: str) -> dict:
    sentences = corpus.split("\n")
    words = []
    for sentence in sentences:
        for i in range(N - 1):
            sentence = f"<s> {sentence} </s>"
        for word in sentence.split(" "):
            words.append(word)
    uniqueSequences = []
    sequences = []
    histories = []
    i = 0
    while i + N - 1 < len(words):
        sec = []
        his = []
        for j in range(N):
            sec.append(words[i + j])
            if j + 1 < N:
                his.append(words[i + j])
        if his[0] == "</s>":
            i += 1
            continue
        joinedSec = " ".join(sec)
        if joinedSec not in uniqueSequences:
            uniqueSequences.append(joinedSec)
        sequences.append(joinedSec)
        histories.append(" ".join(his))
        i += 1
    probabilities = {}
    for sec in uniqueSequences:
        his = " ".join(sec.split(" ")[: N - 1])
        prob = sequences.count(sec) / histories.count(his)
        probabilities[sec] = prob
        print(f"{sec} -> {prob}")
    return probabilities


def CalcProbabilitiesLog(N: int, corpus: str) -> dict:
    sentences = corpus.split("\n")
    words = []
    for sentence in sentences:
        for i in range(N - 1):
            sentence = f"<s> {sentence} </s>"
        for word in sentence.split(" "):
            words.append(word)
    uniqueSequences = []
    sequences = []
    histories = []
    i = 0
    while i + N - 1 < len(words):
        sec = []
        his = []
        for j in range(N):
            sec.append(words[i + j])
            if j + 1 < N:
                his.append(words[i + j])
        if his[0] == "</s>":
            i += 1
            continue
        joinedSec = " ".join(sec)
        if joinedSec not in uniqueSequences:
            uniqueSequences.append(joinedSec)
        sequences.append(joinedSec)
        histories.append(" ".join(his))
        i += 1
    probabilities = {}
    i = 0
    start = datetime.datetime.now()
    for sec in uniqueSequences:
        his = " ".join(sec.split(" ")[: N - 1])
        prob = math.log(sequences.count(sec) / histories.count(his))
        probabilities[sec] = prob
        showProgress(i, uniqueSequences, start)
        i += 1
    print()
    return probabilities


def CalcProbabilitiesLogWithAddOneSmoothing(N: int, corpus: str) -> dict:
    sentences = corpus.split("\n")
    words = []
    uniqueWords = []
    for sentence in sentences:
        for i in range(N - 1):
            sentence = f"<s> {sentence} </s>"
        for word in sentence.split(" "):
            words.append(word)
            if word not in uniqueWords:
                uniqueWords.append(word)

    uniqueSequences = [""]
    for i in range(N):
        increaseSequencesLenght(uniqueSequences, uniqueWords)

    sequences = []
    histories = []
    i = 0
    while i + N - 1 < len(words):
        sec = []
        his = []
        for j in range(N):
            sec.append(words[i + j])
            if j + 1 < N:
                his.append(words[i + j])
        if his[0] == "</s>":
            i += 1
            continue
        sequences.append(" ".join(sec))
        histories.append(" ".join(his))
        i += 1
    probabilities = {}
    start = datetime.datetime.now()
    V = len(uniqueWords)
    for i in range(len(uniqueSequences)):
        sec = uniqueSequences[i]
        his = " ".join(sec.split(" ")[: N - 1])
        prob = math.log((sequences.count(sec) + 1) / (histories.count(his) + V))
        probabilities[sec] = prob
        showProgress(i, uniqueSequences, start)
    print()
    return probabilities


def showProgress(i, iterable, startDateTime):
    now = datetime.datetime.now()
    progress = (i + 1) / len(iterable) * 100
    intprog = int(progress)
    elapsed = now - startDateTime
    print(
        "[\033[01m\033[32m"
        + "■" * intprog
        + "\033[0m\033[37m"
        + "-" * (100 - intprog)
        + "\033[0m]",
        "%.2f%%" % progress,
        "elapsed: ",
        elapsed,
        "remaining:",
        datetime.timedelta(
            seconds=int(elapsed.total_seconds() / progress * (100 - progress))
        ),
        end="\r",
    )


def CalcSentenceProbability(N: int, probabilities: dict, sentence: str) -> float:
    sentence = "<s> " + sentence + " </s>"
    words = sentence.split(" ")
    prob = 1
    i = 0
    while i + N - 1 < len(words):
        sec = []
        for j in range(N):
            sec.append(words[i + j])
        sequence = " ".join(sec)
        prob *= getProb(probabilities, sequence)
        i += 1
    return prob


def CalcSentenceProbabilityLog(N: int, probabilities: dict, sentence: str) -> float:
    sentence = "<s> " + sentence + " </s>"
    words = sentence.split(" ")
    prob = 0
    i = 0
    while i + N - 1 < len(words):
        sec = []
        for j in range(N):
            sec.append(words[i + j])
        sequence = " ".join(sec)
        prob += getProb(probabilities, sequence)
        i += 1
    return math.exp(prob)


def getProb(probabilities: dict, sec: str) -> float:
    try:
        return float(probabilities[sec])
    except:
        return 0


def increaseSequencesLenght(sequences: list, words: list):
    i = 0
    while i < len(sequences):
        sequence = sequences[i]
        sec = sequence.split(" ")
        if sec[0] == "":
            sec = []
        sequences.remove(sequence)
        for word in words:
            newSec = sec.copy()
            newSec.append(word)
            sequences.insert(i, " ".join(newSec))
            i += 1

def NormalizeCorpus(corpus:str):
    return corpus.lower()

def AntilogProbability(prob):
    return math.exp(prob)