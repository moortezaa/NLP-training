import datetime
import math

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

def AntilogProbability(prob):
    return math.exp(prob)