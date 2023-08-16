from NaiveBayesClassification import *

trainSet1 = [
    {"goldTag": "-", "text": "just plain boring"},
    {"goldTag": "-", "text": "entirely predictable and lacks energy"},
    # {"goldTag":"-","text":"predictable"},
    # {"goldTag":"-","text":"predictable"},
    # {"goldTag":"-","text":"predictable"},
    # {"goldTag":"-","text":"predictable"},
    # {"goldTag":"-","text":"predictable"},
    # {"goldTag":"-","text":"predictable"},
    {"goldTag": "-", "text": "no surprises and very few laughs"},
    {"goldTag": "-", "text": "i don't like this movie"},
    {
        "goldTag": "-",
        "text": "awful bad bias catastrophe cheat deny envious foul harsh hate",
    },
    {"goldTag": "+", "text": "very powerful"},
    {"goldTag": "+", "text": "the most fun film of the summer"},
    {"goldTag": "+", "text": "i really like this movie"},
    {"goldTag": "+", "text": "this movie made me cry"},
    {
        "goldTag": "+",
        "text": "admirable beautiful confident dazzling ecstatic favor glee great",
    },
]
classification1 = ["-","+"]

trainSet2 = [
    {"goldTag": "comedy", "text": "fun, couple, love, love,"},
    {"goldTag": "comedy", "text": "couple, fly, fast, fun, fun,"},
    {"goldTag": "action", "text": "fast, furious, shoot,"},
    {"goldTag": "action", "text": "furious, shoot, shoot, fun,"},
    {"goldTag": "action", "text": "fly, fast, shoot, love,"},
]
classification2 = ["comedy","action"]

trainSet3 = [
    {"goldTag": "+", "text": "good good good great great great"},
    {"goldTag": "+", "text": "poor great great"},
    {"goldTag": "-", "text": "good poor poor poor"},
    {"goldTag": "-", "text": "good poor poor poor poor poor great great"},
    {"goldTag": "-", "text": "poor poor"},
]
classification3 = ["-","+"]

trainingData = TrainBinaryNaiveBayes(
    NormalizeDocuments(trainSet3),
    classification3,
)

# PrintTrainingData(trainingData)

tests1 = [
    {"goldLabel": "-", "text": "predictable with no fun"},
    {"goldLabel": "+", "text": "i really like this movie"},
    {"goldLabel": "-", "text": "i don't like this movie"},
    {"goldLabel": "-", "text": "boring AF"},
    {"goldLabel": "-", "text": "the most predictable movie ever"},
    {"goldLabel": "+", "text": "this movie is dazzling"},
    {"goldLabel": "-", "text": "i hate it"},
]

tests2=[
    {"goldLabel": "action", "text": "fast, couple, shoot, fly,"},
]

tests3=[
    {"goldLabel": "-", "text": "A good, good plot and great characters, but poor acting."},
]

for t in tests3:
    nt = NormalizeForBayes(t["text"])
    r = TestNaiveBayes(nt, trainingData, classification3)
    # print()
    print(f'classification for \033[33m"{t["text"]}"\033[0m is: \033[33m{r}\033[0m')
    # print(f'- probability: {"%.8f"%GetProbabilityInClass(nt,"-",trainingData)}')
    # print(f'+ probability: {"%.8f"%GetProbabilityInClass(nt,"+",trainingData)}')

tr = PrintConfusionMatrix(tests3, trainingData)
print(GetFMeasure(tr, 1))

#TODO: change functions to support more then two classifications