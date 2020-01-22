import random


def prime_test(N, k):
    # This is the main function connected to the Test button. You don't need to touch it.
    return run_fermat(N,k), run_miller_rabin(N,k)


def mod_exp(x, y, N):
    if y==0:
        return 1
    z = mod_exp(x, y//2, N)
    if y % 2 == 0:      #y is even
        return (z**2) % N
    else:               #y is odd
        return x * (z**2) % N



def fprobability(k):
    # probability of fermat's theorm being correct is 1/2, and as shown in
    # class, multiple goes at the formula increases this probability by 1/2^x
    # where x is the number of values picked.
    return 1- (1/(2**k))


def mprobability(k):
    # probability of miller_rabin's theorm being correct is 3/4, and as shown in
    # class, multiple goes at the formula increases this probability by 3/4^x
    # where x is the number of values picked.
    return 1-(1/(4**k))


def run_fermat(N,k):
    for number in range(0, k):
        a = random.randint(2, N-1)
        if mod_exp(a, N-1, N) == 1: #If mod_exp returns 1, then it is still prime, and we test again
            continue
        else:                       #If mod_exp != 1, then it is composite
            return 'composite'
    return 'prime'


def run_miller_rabin(N,k):
    # You will need to implement this function and change the return value, which should be
    # either 'prime' or 'composite'.
    #
    # To generate random values for a, you will most likley want to use
    # random.randint(low,hi) which gives a random integer between low and
    #  hi, inclusive.

    for number in range(0, k):
        a = random.randint(2, N-1)
        x = (N-1) * 2

        while x > 1 and x % 2 == 0:
            x = x/2
            if mod_exp(a, x, N) == 1 or mod_exp(a, x, N) == N-1:
                continue
            else:
                return 'composite'

    return 'prime'
