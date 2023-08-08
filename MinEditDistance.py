def GetMinEditDistanceLevenshtein(st1: str, st2: str) -> int:
    n = len(st1)
    m = len(st2)
    d = {}
    for row in range(n + 1):
        for col in range(m + 1):
            if row == 0:
                d[row, col] = col
            elif col == 0:
                d[row, col] = row
            else:
                subcost = 0
                if row != 0 and col != 0:
                    if st1[row - 1] != st2[col - 1]:
                        subcost = 2

                d[row, col] = min(
                    d[row - 1, col] + 1,
                    d[row, col - 1] + 1,
                    d[row - 1, col - 1] + subcost,
                )
    return d[row, col]


def GetMinEditDistanceLevenshteinPrintMatrix(st1: str, st2: str) -> int:
    n = len(st1)
    m = len(st2)
    d = {}
    print(end="\t")
    for col in range(m + 1):
        if col == 0:
            print("#", end="\t")
        else:
            print(st2[col - 1], end="\t")
    print()
    for row in range(n + 1):
        if row == 0:
            print("#", end="\t")
        else:
            print(st1[row - 1], end="\t")
        for col in range(m + 1):
            if row == 0:
                d[row, col] = col
            elif col == 0:
                d[row, col] = row
            else:
                subcost = 0
                if row != 0 and col != 0:
                    if st1[row - 1] != st2[col - 1]:
                        subcost = 2

                d[row, col] = min(
                    d[row - 1, col] + 1,
                    d[row, col - 1] + 1,
                    d[row - 1, col - 1] + subcost,
                )
            print(d[row, col], end="\t")
        print()
    return d[row, col]


def GetMinEditDistanceLevenshteinPrintMatrixAddTraceBack(st1: str, st2: str) -> int:
    n = len(st1)
    m = len(st2)
    d = {}
    print(end="\t")
    for col in range(m + 1):
        if col == 0:
            print("#", end="\t")
        else:
            print(st2[col - 1], end="\t")
    print()
    for row in range(n + 1):
        if row == 0:
            print("#", end="\t")
        else:
            print(st1[row - 1], end="\t")
        for col in range(m + 1):
            d[row,col,0] = []
            if row==0 and col==0:
                d[row,col]=0
            elif row == 0:
                d[row, col] = col
                d[row,col,0].append((row,col-1,"ins"))
                print("←", end='')
            elif col == 0:
                d[row, col] = row
                d[row,col,0].append((row-1,col,"del"))
                print("↑", end='')
            else:
                subcost = 0
                if row != 0 and col != 0:
                    if st1[row - 1] != st2[col - 1]:
                        subcost = 2

                deleteVal = d[row - 1, col] + 1
                insertVal = d[row, col - 1] + 1
                subVal = d[row - 1, col - 1] + subcost
                minVal = min(
                    d[row - 1, col] + 1,
                    d[row, col - 1] + 1,
                    d[row - 1, col - 1] + subcost,
                )

                if minVal == subVal:
                    print("⬉",end=' ')
                    d[row,col,0].append((row-1,col-1,"sub"))
                if minVal == deleteVal:
                    print("↑", end='')
                    d[row,col,0].append((row-1,col,"del"))
                if minVal == insertVal:
                    print("←", end='')
                    d[row,col,0].append((row,col-1,"ins"))

                d[row, col] = minVal
            print(d[row, col], end="\t")
        print()
    #back tracing
    BackTraceWithPrint(d,n,m,st1,st2)
    return d[row, col]

def BackTraceWithPrint(matrix,row,column,st1,st2):
    state = (row,column,"end")
    paths = [[state]]
    i=0
    while i<len(paths):
        path = paths[i]
        state = path[0]
        if state[0] == 0 and state[1] == 0:
            i+=1
            continue
        moves = matrix[state[0],state[1],0]
        pathCopy = path.copy()
        paths.remove(path)
        for move in moves:
            newPath = pathCopy.copy()
            newPath.insert(0,move)
            paths.append(newPath)
    
    pathnum =0
    for path in paths:
        pathnum +=1
        print(f'____________{pathnum}____________')
        edit = None
        for move in path:
            if edit == None:
                edit = move[2]
                continue
            if edit == "sub":
                print(f'{st1[move[0]-1]} -sub-> {st2[move[1]-1]}')
            if edit == "del":
                print(f'{st1[move[0]-1]} -del-> #')
            if edit == "ins":
                print(f'# -ins-> {st2[move[1]-1]}')
            edit = move[2]