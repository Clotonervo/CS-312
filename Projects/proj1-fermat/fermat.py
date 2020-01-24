import random


def prime_test(N, k):
    return run_fermat(N,k), run_miller_rabin(N,k)


def mod_exp(x, y, N):   # Runs in O(n^3), assuming we have n bits for input
    if y==0:
        return 1
    z = mod_exp(x, y//2, N)
    if y % 2 == 0:      # O(1)
        return (z**2) % N   # Bit shift and then check last bit, O(n^2)
    else:
        return x * (z**2) % N   # n^2 + 2n^2 so O(n^2)



def fprobability(k):    # Runs in O(n^2) time, while space complexity is O(1)
    return 1-(1/(2**k)) # Division is O(n^2), while subtraction and division are O(n) and O(2n)


def mprobability(k):    # Runs in O(n^2) time, while space complexity is O(1)
    return 1-(1/(4**k)) # Division is O(n^2), while subtraction and division are O(n) and O(2n)


def run_fermat(N,k):        # Runs in O(k*n^3) time
    for number in range(k):
        a = random.randint(2, N-1) # O(1) time
        if mod_exp(a, N-1, N) == 1: # mod_exp runs in O(n^3) time
            continue
        else:
            return 'composite'
    return 'prime'


def run_miller_rabin(N,k):  # Runs in O(n^4*k)
    if N % 2 == 0:  # O(1) because just needs to check last bit
        return 'composite'
    for number in range(k):
        a = random.randint(1, N-1)  # O(1)
        x = (N-1)   # O(n) time
        while x > 1 and x % 2 == 0: # Repeats this at most N times, so O(n)
            if mod_exp(a, x, N) == 1:   # mod_exp runs in O(n^3) time
                x = x/2 # O(n^2) for division
            elif mod_exp(a,x,N) == N-1: # mod_exp runs in O(n^3) time
                break
            else:
                return 'composite'
    return 'prime'
