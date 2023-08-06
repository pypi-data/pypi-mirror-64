def fib(n):
    s=[1,1] 
    while len(s)<n:
        s.append(sum(s[-2::]))
    return sum(s)