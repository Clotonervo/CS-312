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
    return 1-(1/(2**k))


def mprobability(k):
    return 1-(1/(4**k))


def run_fermat(N,k):
    for number in range(k):
        a = random.randint(2, N-1)
        if mod_exp(a, N-1, N) == 1: #If mod_exp returns 1, then it is still prime, and we test again
            continue
        else:                       #If mod_exp != 1, then it is composite
            return 'composite'
    return 'prime'


def run_miller_rabin(N,k):
    if N % 2 == 0:
        return 'composite'
    for number in range(k):
        a = random.randint(1, N-1)
        x = (N-1)
        while x > 1 and x % 2 == 0:
            if mod_exp(a, x, N) == 1:
                x = x/2
            elif mod_exp(a,x,N) == N-1:
                break
            else:
                return 'composite'
    return 'prime'
