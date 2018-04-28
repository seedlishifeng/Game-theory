import random
import numpy as np
'''
I can use the matrix to express the relationship between A and B

'''
  #both of A and B keep silence
  #both of A and B expose each other
  #one of them keep silence and the other expose
M= [[1.0,1.0],[0.0,10.0],[10.0,0.0],[5.0,5.0]]

T = 1000 # keep the even 1000 times
'''
they know the times is 1000, set t =  so at the last time they will expose each other

'''

def Justify(A):
    L = len(A)
    count =0
    State = 0
    num = random.randint(1, L)
    while(num==1):
        if num==1:
            count = count +1
            continue
        else:
            State = num
            break
    return count,State

def Run(A):
    Change,First=Justify(A)
    Next = Change +1
    Record =np.zeros([T,2])
    sum1 = 0.0
    sum2 = 0.0
    for i in range(Change):
        Record[i][0]= M[len(A)-1][0]
        Record[i][1]= M[len(A)-1][1]
    for i in range(Next-1 ,T):
        Record[i][0] = M[len(A)-1][0]
        Record[i][1] = M[len(A)-1][1]
    for i in range(T):
        sum1=sum1+Record[i][0]
    for i in range(T):
        sum2=sum2+Record[i][1]

    A_average= sum1/T
    B_average= sum2/T
    return A_average,B_average

a,b=Run(M)
print(a)
print(b)

