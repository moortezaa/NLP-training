from MLE_N_gram import *

N=2

def calc_prob(source,destination,function):
    probabilities = None
    with open(source, "r") as f:
        probabilities = function(N, NormalizeCorpus(f.read()))

    with open(destination, "w") as f:
        f.writelines(f"{key},{probabilities[key]}\n" for key in probabilities)
    return probabilities


def load_prob(source):
    probabilities = {}
    with open("BeRP probabilities.txt", "r") as f:
        for line in f:
            p = line.replace('\n','').split(",")
            probabilities[p[0]]=p[1]
    return probabilities


probabilities = calc_prob("BeRP transcript.txt","BeRP probabilities Add one smoothing.txt",CalcProbabilitiesLogWithAddOneSmoothing)

# sample = ["i", "want", "to", "eat", "english", "food", "lunch", "spend"]
# for w1 in sample:
#     for w2 in sample:
#         sec = w1 + " " + w2
#         try:
#             print(f"{sec} -> {probabilities[sec]}")
#         except:
#             print(f"{sec} -> 0")

# print('%.6f'%CalcSentenceProbabilityLog(N,probabilities,'i want english food'))

print(AntilogProbability( probabilities["am sam"]))