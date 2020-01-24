import random


def prime_test(N, k):
    return run_fermat(N,k), run_miller_rabin(N,k)


def mod_exp(x, y, N):   # Runs in O(n^3), assuming we have n bits for input
    if y == 0:
        return 1
    z = mod_exp(x, y//2, N)
    if y % 2 == 0:      # O(1), check if y is even
        return (z**2) % N   # Bit shift and then check last bit, O(n^2), y is even
    else:
        return x * (z**2) % N   # n^2 + 2n^2 so O(n^2), y is odd


# The Fermat algorithm has a 1/2 chance of being incorrect after its initial run, so
# we simply multiply that probability to the k to get the probability we are wrong after k trials,
# and subtract that from 1
def fprobability(k):    # Runs in O(n^2) time, while space complexity is O(1)
    return 1-(1/(2**k)) # Division is O(n^2), while subtraction and division are O(n) and O(2n)


# The Miller Rabin algorithm has a 1/4 chance of being incorrect after its initial run, so
# we simply multiply that probability to the k to get the probability we are wrong after k trials,
# and subtract that from 1
def mprobability(k):    # Runs in O(n^2) time, while space complexity is O(1)
    return 1-(1/(4**k)) # Division is O(n^2), while subtraction and division are O(n) and O(2n)


def run_fermat(N,k):        # Runs in O(k*n^3) time
    for number in range(k):
        a = random.randint(2, N-1) # O(1) time, [a] becomes our random number
        # If mod_exp equals 1, then we know it is probability prime
        if mod_exp(a, N-1, N) == 1: # mod_exp runs in O(n^3) time
            continue
        else:   # If mod_exp isn't 1, then we know it is composite
            return 'composite'
    return 'prime'



def run_miller_rabin(N,k):  # Runs in O(n^4*k)
    # We check if N is even to give quick return
    if N % 2 == 0:  # O(1) because just needs to check last bit
        return 'composite'
    for number in range(k):
        a = random.randint(1, N-1)  # O(1), [a] becomes our random number
        x = (N-1)   # O(n) time, set up the exponent
        # If x is less than 1 we are done, and if x is even then we are done
        while x > 1 and x % 2 == 0: # Repeats this at most N times, so O(n)
            if mod_exp(a, x, N) == 1:   # mod_exp runs in O(n^3) time
                # We take the square root, or divide the exponent by 2
                x = x/2 # O(n^2) for division
            elif mod_exp(a,x,N) == N-1: # mod_exp runs in O(n^3) time
                # For this a, the algorithm works, so go back and check others
                break
            else:   # It must be composite if mod_exp isn't 1 or -1
                return 'composite'
    return 'prime'
