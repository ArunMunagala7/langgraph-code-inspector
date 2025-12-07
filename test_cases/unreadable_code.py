# Test Case: Unreadable Code - Poor Style
# Expected Quality: D-
# Expected Bugs: 3


def f(x,y,z):
    a=x+y
    b=a*z
    if a>10:c=a*2
    else:c=a/2
    d=[i for i in range(100) if i%2==0 and i%3==0 and i%5==0]
    return b+c+sum(d)

def g(l):
    r=[]
    for i in l:
        if type(i)==int:
            r.append(i*2)
        elif type(i)==str:
            r.append(i.upper())
    return r

x=f(5,10,2)
y=g([1,2,"hello",3,"world"])
