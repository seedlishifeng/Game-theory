
def Nim(a,g):
    tmp =[]
    number=[]
    for i in a :
        tmp.append(bin(g[i])[2:])
    max1= max(len(tmp[0]),len(tmp[1]))
    min1= min(len(tmp[0]),len(tmp[1]))
    for i in range(max1):
        number.append(0)
    for i in range(min1):
        if tmp[0][-i-1] == tmp[1][-i-1]:
            number[-i-1]=0
        else:
            number[-i - 1] = 1
    for i in range(max1-min1):
        if len(tmp[0])==max1:
            number[-min1-1-i]=tmp[0][-i-1-min1]
        else:
            number[-min1-1-i]=tmp[1][-i-1-min1]
    return ''.join(map(str,number))
def mex(a,g):
    tmp=[]
    for i in a:
        if type(i)==list:
            tmp.append(Nim(i,g))
        else:
            tmp.append(g[i])
    for i in range(1000):
        if i in tmp:
            continue
        else:
            return i


tmp={0:0, 1:1, 2:2, 3:4}
for i in range(4,101):
        tmp[i]=[]
        for n in range(i):
            tmp[i].append(n)
        for j in range(int(i/2)):
            tmp[i].append([j+1,i-j-1])
        value = mex(tmp[i],tmp)
        tmp[i]=value
#print(tmp[100])
