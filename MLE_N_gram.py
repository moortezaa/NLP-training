def CalcProbabilities(N:int,corpus: str):
    sentences = corpus.split('.')
    words = []
    for sentence in sentences:
        for i in range(N-1):
            sentence = f'<s> {sentence} </s>'
        for word in sentence.split(' '):
            words.append(word)
    sequences = []
    histories = []
    i=0
    while i+N-1 < len(words):
        sec = []
        his = []
        for j in range(N):
            sec.append(words[i+j])
            if j+1<N:
                his.append(words[i+j])
        if his[0] == '</s>':
            i+=1
            continue
        sequences.append(' '.join(sec))
        histories.append(' '.join(his))
        i+=1
    probabilities = []
    for sec in sequences:
        his = ' '.join(sec.split(' ')[:N-1])
        probabilities.append((sec,sequences.count(sec) / histories.count(his)))
    print(probabilities)
    return probabilities

CalcProbabilities(3,"I am Sam.Sam I am.I do not like green eggs and ham")