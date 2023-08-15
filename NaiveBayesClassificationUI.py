from NaiveBayesClassification import *

trainingData = TrainNaiveBayes(
    NormalizeDocuments(
        [
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
            {"goldTag": "-","text": "awful bad bias catastrophe cheat deny envious foul harsh hate",},
            {"goldTag": "+", "text": "very powerful"},
            {"goldTag": "+", "text": "the most fun film of the summer"},
            {"goldTag": "+", "text": "i really like this movie"},
            {"goldTag": "+", "text": "this movie made me cry"},
            {"goldTag": "+","text": "admirable beautiful confident dazzling ecstatic favor glee great",},
        ]
    ),
    ["-", "+"],
)

# PrintTrainingData(trainingData)

tests = [
    {"goldLabel":"-","text":"predictable with no fun"},
    {"goldLabel":"+","text":"i really like this movie"},
    {"goldLabel":"-","text":"i don't like this movie"},
    {"goldLabel":"-","text":"boring AF"},
    {"goldLabel":"-","text":"the most predictable movie ever"},
    {"goldLabel":"+","text":"this movie is dazzling"},
    {"goldLabel":"-","text":"i hate it"},
]

for t in tests:
    nt = NormalizeForBayes(t["text"])
    r = TestNaiveBayes(nt, trainingData, ["-", "+"])
    # print()
    print(f'classification for \033[33m"{t["text"]}"\033[0m is: \033[33m{r}\033[0m')
    # print(f'- probability: {"%.8f"%GetProbabilityInClass(nt,"-",trainingData)}')
    # print(f'+ probability: {"%.8f"%GetProbabilityInClass(nt,"+",trainingData)}')

tr = PrintConfusionMatrix(tests,trainingData)
print(GetFMeasure(tr,1))
