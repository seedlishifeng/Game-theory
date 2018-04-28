import numpy

file1 = open('source-node-id','r')
file2 = open('desitnation-node-id','r')
def filelist(filename,N):
    fr = open(filename)
    array = fr.readlines()
    num = len(array)
    returnMat = numpy.zeros((num,N))
    index = 0
    for line in array:
        line = line.strip()
        linelist = line.split(' ')
        returnMat[index,:] = linelist[0:N]
        index +=1
    return returnMat
Node = filelist('source-node-id',1)
Edge = filelist('desitnation-node-id',2)
Nodes = [0]*len(Node)
Edges = [[0] * 2] * len(Edge)
for i in range(len(Node)):
    Nodes[i]=int(Node[i])
print(Nodes)
print(Edge)
def matrix(node,edge):
    Graph = numpy.zeros([len(node),len(node)])
    for i in range(len(node)):
        for j in range(len(node)):
            for k in range(len(edge)):
                if edge[k][0]==float(i) and edge[k][1]==float(j):
                    Graph[i][j]=1.0
                if edge[k][0]==float(j) and edge[k][1]==float(i):
                    Graph[i][j]=1.0
    return Graph
t = matrix(Nodes,Edge)
print(t)
def process(M):
    t = len(M)
    tmp = [0]*t
    for i in range(t):
        sum = 0.0
        for j in range(t):
            sum = M[i][j] + sum
        tmp[i]= int(sum)
    return tmp
print(process(t))
table=[0]*len(Nodes)
def confusion(M,node,tab):
    t = len(M)
    for i in range(t):
        if M[node][i] !=0.0 and tab[node]==tab[i]:
            return False
    return True

def g_function(M,tab):
    t= len(tab)
    tmp = process(M)
    for i in range(t):
        if tmp[i]==0:
            tab[i]=1
        if tmp[i]==1:
            tab[i]=1
    k =t
    while(k>0):
        for i in range(t):
            if tab[i]==0:
                tab[i]=  tab[i]+1
                if confusion(M,i,tab)==False:
                    tab[i]=tab[i]+1
        break
    return tab
#l=g_function(t,table)
#print(l)
