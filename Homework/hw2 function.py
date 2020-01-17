def modexp(x,y,N):
    if y==0:
        return 1
    z = modexp(x, y//2, N)
    if y % 2 == 0:  #is even
        return (z**2) % N
    else:
        return x * (z**2) % N



print(modexp(2, 21, 18))
