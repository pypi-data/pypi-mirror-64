def fib(n):
    s=[1,1] 
    while len(s)<n:
        s.append(sum(s[-2::]))
    return sum(s)


def hydro(string):
    pre = { "Meth": 1, "Eth": 2, "Prop": 3, "But": 4, "Pent": 5, "Hex": 6, "Hept": 7, "Oct": 8, "Non": 9, "Dec": 10}
    carb = pre[string[:3]] if string[:3] in pre else pre[string[:4]]
    suff = {'ane': 2, 'ene': 0, 'yne': -2}[string[-3:]]
    return (carb, 2*carb+suff)