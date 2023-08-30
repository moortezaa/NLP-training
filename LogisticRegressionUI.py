from LogisticRegretion import *

#samples:

# Text: I love this movie. It was great and it's easy to have fun with.
# Label: positive

# Text: i really like this movie.
# Label: positive

# Text: this movie is dazzling.
# Label: positive

# Text: very powerful.
# Label: positive

# Text: This is a terrible movie. The plot is boring and the acting is awful.
# Label: negative

# Text: just plain boring.
# Label: negative

# Text: entirely predictable and lacks energy.
# Label: negative

# Text: no surprises and very few laughs.
# Label: negative

# x1: number of positive words
# x2: number of negative words
# x3: lenght
# x4: has no

trainingData = [
    ([4,0,14,0],1),
    ([1,0,5,0],1),
    ([1,0,4,0],1),
    ([1,0,2,0],1),
    ([0,3,14,0],0),
    ([0,1,3,0],0),
    ([0,2,5,0],0),
    ([1,1,6,1],0)
]

weights = miniBatchGradintDesentGeneralizedWithVisualization(trainingData,len(trainingData))