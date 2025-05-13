a=0     # 0-1--1-2
b=0     # 1-0--1-1
for i in range(0, 10):
    if b==0 :
        print(a)
        b=b+1
    else :
        c=a+b
        print(c)
        b=a
        a=c