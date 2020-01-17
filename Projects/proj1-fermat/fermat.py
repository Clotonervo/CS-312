import random


def prime_test(N, k):
    # This is the main function connected to the Test button. You don't need to touch it.
    return run_fermat(N,k), run_miller_rabin(N,k)


def mod_exp(x, y, N):
    if y==0:
        return 1
    z = modexp(x, y//2, N)
    if y % 2 == 0:      #y is even
        return (z**2) % N
    else:               #y is odd
        return x * (z**2) % N



def fprobability(k):
    # probability of the primality working first try is 1/2, and as shown in
    # class, multiple goes at the formula increases this probability by 1/2^x
    # where x is the number of values picked.
    return 1/(2**k)


def mprobability(k):
    # You will need to implement this function and change the return value.
    return 0.0


def run_fermat(N,k):
    # You will need to implement this function and change the return value, which should be
    # either 'prime' or 'composite'.
    #
    # To generate random values for a, you will most likley want to use
    # random.randint(low,hi) which gives a random integer between low and
    #  hi, inclusive.
    return 'prime'


def run_miller_rabin(N,k):
    # You will need to implement this function and change the return value, which should be
    # either 'prime' or 'composite'.
    #
    # To generate random values for a, you will most likley want to use
    # random.randint(low,hi) which gives a random integer between low and
    #  hi, inclusive.
    return 'composite'
