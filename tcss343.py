import random
import math
import tracemalloc
from time import perf_counter

"""
TCSS 334 A Fall 2022
Homework #4

@author Michael Theisen
@param S, a list of integers
@param n, the number of integers in the list
@param t, the total to reach for there to be a subset

"""


# Design and implement a brute force solution for this problem.
def subsetSumRecursive(S, n, t):
    # Start with the potential for the t be 0 to be TRUE.
    if t == 0 and n >= 1:
        return True
    # Then ensure a FALSE for an empty list regardless of total.
    if t >= 0 and n == 0:
        return False
    # Then we deal with the idea of the sum being greater or equal to the last element
    if sum(S) == t:
        print(S)
    if S[n - 1] <= t:
        return subsetSumRecursive(S, n - 1, t) or subsetSumRecursive(S, n - 1, t - S[n - 1])
    # And when it is not
    else:
        return subsetSumRecursive(S, n - 1, t)
    # This is my interpretation of the self-reduction on slide 4 of week 7
    # with a little messing around to get it to actually work.
    # I'm ignoring the potential negative values inside the lists.


################################################################################################
"""
@param S, a list of integers
@param n, the number of integers in the list
@param t, the total to reach for there to be a subset

"""


# Design and implement a DP solution for this problem.
def subsetSumDynamic(S, n, t):
    # Let A[1...n][0...t] be an array of integers of size (n * (t + 1))
    # where it's True when t
    A = [[False for i in range(t + 1)] for j in range(n + 1)]

    # When t is 0 then True
    for i in range(1, n + 1):
        A[i][0] = True

    # When t is not 0 and S is empty then False
    for j in range(1, t + 1):
        A[0][j] = False

    for i in range(2, n + 1):
        for j in range(1, t + 1):
            if j >= S[i - 1]:
                A[i][j] = A[i - 1][j] or A[i - 1][j - S[i - 1]]
            else:
                A[i][j] = A[i - 1][j]

    return A[n][t]
    # This was my interpretation of the pseudocode present in the lecture slides


################################################################################################
"""
@param S, a list of integers
@param n, the number of integers in the list
@param t, the total to reach for there to be a subset

"""


# Design and implement a solution for this problem based on the clever algorithm.
def subsetSumClever(S, n, t):
    H = []  # Higher, H = {⌊n/2⌋ + 1...n-1}
    # for i in range(math.floor(n / 2) + 1, n - 1):
    #     H.append(i)
    L = []  # Lower , L = {0...⌊n/2⌋}
    # for i in range(0, math.floor(n / 2)):
    #     L.append(i)
    if sum(S) % 2:
        return False

    t = sum(S) // 2
    for i in range(len(S)-1):
        for t in L:
            if (t + S[i]) == t:
                return True
            H.append(t + S[i])
            H.append(t)
        L = H
    if t in L:
        return True
    else:
        return False

    # tableT = []
    #     for L
    # tableW = []

    # if n % 2 == 0:
    #     L = [n/2]
    # else:
    #     L = [(n/2) + 1]
    # H = [n/2]


################################################################################################
"""
@param S, a list of integers
@param i, the number of integers in the list
@param t, the total to reach for there to be a subset
@param recoverSubsets, the list appended to for recovery of the subsets

"""


def Printer(S, i, t, recoverSubsets):
    if i == 0 and t == 0:
        print(recoverSubsets)
        return
    if i == 0 and t != 0 and A[0][t]:
        recoverSubsets.append(S[i])
        print(recoverSubsets)
        return
    if A[i - 1][t]:
        temp = []
        temp.extend(recoverSubsets)
        Printer(S, i - 1, t, temp)
    if t >= S[i] and A[i - 1][t - S[i]]:
        recoverSubsets.append(S[i])
        Printer(S, i - 1, t - S[i], recoverSubsets)


################################################################################################
"""
@param S, a list of integers
@param n, the number of integers in the list
@param t, the total to reach for there to be a subset

"""


def backPropagator(S, n, t):
    global A
    A = [[False for i in range(t + 1)] for j in range(n)]  # from the slides
    # When t is 0 then True
    for i in range(n):
        A[i][0] = True

    # for j in range(1, t):  # why doesnt this work
    #    if S[1] = j:
    #       A[1][j] = True
    #    else:
    #       A[1][j] = False

    #    A[0][j] = False
    if S[0] <= t:
        A[0][S[0]] = True

    for i in range(1, n):  # why 1 and not 2
        for j in range(1, t + 1):  # just t not (t-1)
            if j >= S[i]:
                A[i][j] = A[i - 1][j] or A[i - 1][j - S[i]]
            else:
                A[i][j] = A[i - 1][j]

    recoverSubsets = []
    Printer(S, n - 1, t, recoverSubsets)
    # Currently, I wrote the subsetSumDynamic first and tried to incorporate the subsets
    # but in the process I messed up the bounds of the lists and haven't fixed them yet.
    # That being said, it wasn't pressing. So, that is one definite bug.


################################################################################################
"""
@param n, the number of random integers in the list
@param r, the end range for sampled random elements
@param v, a boolean to test for existence of the subset

"""


def Driver(n, r, v):
    S = []
    t = 0
    for i in range(n):
        S.append(random.randint(1, r))
    start = perf_counter()
    tracemalloc.start()
    if v:
        # the sum of a random subset of S guaranteeing a solution.
        a = S[random.randint(1, math.floor(n / 2))]
        b = S[random.randint(((math.floor(n / 2)) + 1), n)]
        t = a + b
        print("\nThe Driver Testing code evaluates to: TRUE\nThere is a subset that adds to t =", t,
              "within the set: S", S,
              "such that the subset \nis: A [", a, ",", b, "] where n =", n, "and r =", r, ".")
    else:
        # random value larger than the sum of all values on S
        for elements in range(0, len(S)):
            t = t + S[elements] + random.randint(1, r)
        print("There is no subset that adds to: t =", t, "within the set", S)
    end = perf_counter()
    print("The evaluation time is in milliseconds is:", ((end - start) * 1000), "milliseconds")
    print("A representation of the space requirements is:")

    snapshot = tracemalloc.take_snapshot()
    for stat in snapshot.statistics("lineno"):
        print(stat)
    tracemalloc.stop()

    ###########################################################################

    start = perf_counter()
    tracemalloc.start()
    if subsetSumRecursive(S, n, t) == True:
        print("\nThe Brute Force Recursive Algorithm evaluates to: TRUE")
        print("This indicates that for the set S", S, " where n =", n, ", r =", r, ", and t =", t,
              ", there is/are a subset(s) A")
        backPropagator(S, n, t)
        # True and a set of indices A subset {0...n-1}. How do I do that without a library?
    else:
        print("\nThe Brute Force Recursive Algorithm evaluates to: FALSE")
    end = perf_counter()
    print("The evaluation time is in milliseconds is:", ((end - start) * 1000), "milliseconds")
    print("A representation of the space requirements is:")

    snapshot = tracemalloc.take_snapshot()
    for stat in snapshot.statistics("lineno"):
        print(stat)
    tracemalloc.stop()

    ###########################################################################

    start = perf_counter()
    tracemalloc.start()
    if subsetSumDynamic(S, n, t) == True:
        print("\nThe Dynamic Programming Algorithm evaluates to: TRUE")
        print("This indicates that for the set S", S, " where n =", n, ", r =", r, ", and t =", t,
              ", there is/are a subset(s) A")
        backPropagator(S, n, t)

    else:
        print("\nThe Dynamic Programming Algorithm evaluates to: FALSE")
    end = perf_counter()
    print("The evaluation time is in milliseconds is:", ((end - start) * 1000), "milliseconds")
    print("A representation of the space requirements is:")
    snapshot = tracemalloc.take_snapshot()
    for stat in snapshot.statistics("lineno"):
        print(stat)
    tracemalloc.stop()

    ###########################################################################

    # tracemalloc.start()
    # if subsetSumClever(S, n, t) == True:
    #     print("\nThe Clever Algorithm evaluates to: TRUE")
    #     print("This indicates that for the set S", S, " where n =", n, ", r =", r, ", and t =", t,
    #           ", there is/are a subset(s) A")
    #     backPropagator(S, n, t)
    # else:
    #     print("\n The Clever Algorithm evaluates to: FALSE")
    # end = perf_counter()
    # print("The evaluation time is in milliseconds is:", ((end - start) * 1000), "milliseconds")
    # print("A representation of the space requirements is:")
    # snapshot = tracemalloc.take_snapshot()
    # for stat in snapshot.statistics("lineno"):
    #     print(stat)
    # tracemalloc.stop()


#Driver(50, 1_000, True)
#Driver(20, 1_000, False)
Driver(10, 1_000_000, True)
#Driver(80, 1_000_000, False)
