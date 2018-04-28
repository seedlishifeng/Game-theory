def linear_program(A):
    min=0
    for i in range(len(A)):
        for j in range(len(A[0])):
           if A[i][j]<min:
               min=A[i][j]
    if min<0:
        add_num=-min
        for i in range(len(A)):
            for j in range(len(A[0])):
                A[i][j]=A[i][j]+add_num
    else:
        add_num=0
    table = [[0 for j in range(len(A[0])+2)] for i in range(len(A)+2)]

    for i in range(len(A)+2):
        for j in range(len(A[0])+2):
            if i==0:
                table[i][j]='y'+str(j)
            elif j==0:
                table[i][j]='x'+str(i)
            elif i==len(A[0])+1 and j==len(A)+1:
                table[i][j]=0
            elif i==len(A)+1:
                table[i][j]=-1
            elif j==len(A[0])+1:
                table[i][j]=1
            else:
                table[i][j]=A[i-1][j-1]
    table[len(A)+1][len(A[0])+1]=0
    #print(table)
    while True:
        min_last_row=0
        pivot_y=-1
        for i in range(1,len(A[0])+1):
            if table[len(A)+1][i]<min_last_row:
                min_last_row=table[len(A)+1][i]
                pivot_y=i
        if min_last_row>=0:
            break
        min_ratio=sys.maxsize
        pivot_x=-1
        #print("yy",pivot_y)
        for i in range(1,len(A)+1):
            if table[i][pivot_y]<0:
                ratio=sys.maxsize
            elif table[i][pivot_y]==0:
                ratio=sys.maxsize
            else:
                ratio=table[i][len(A[0])+1]/table[i][pivot_y]
            if ratio<min_ratio:
                min_ratio=ratio
                pivot_x=i
        next_table= [[0 for j in range(len(A[0])+2)] for i in range(len(A)+2)]
        pivot=table[pivot_x][pivot_y]
        #print(pivot)
        #print(pivot_x)
        for i in range(1,len(A) + 2):
            for j in range(1,len(A[0]) + 2):
                if i==pivot_x and j==pivot_y:
                    next_table[i][j]=1/pivot
                elif i==pivot_x and j!=pivot_y:
                    next_table[i][j]=table[i][j]/pivot
                elif j==pivot_y and i!=pivot_x:
                    next_table[i][j]=table[i][j]/(0-pivot)
                elif i!=pivot_x and j!=pivot_y:
                    if i==len(A)+1 and j==len(A[0])+1:
                        print(table[i][j],table[i][pivot_y],table[pivot_x][j],pivot)
                    next_table[i][j]=table[i][j]-(table[i][pivot_y]*table[pivot_x][j])/pivot
        for i in range(1,len(A)+1):
            if i==pivot_x:
                next_table[i][0]=table[0][pivot_y]
            else:
                next_table[i][0]=table[i][0]
        for i in range(1,len(A[0])+1):
            if i==pivot_y:
                next_table[0][i]=table[pivot_x][0]
            else:
                next_table[0][i]=table[0][i]
        table=next_table
        #print(table)
    p=[]
    q=[]
    value=(1/table[len(A)+1][len(A[0])+1])-add_num
    temp1=0
    temp2=0
    y_list=[]
    x_list=[]

    for i in range(1,len(A)+1):
        if table[i][0] == "y"+str(i):
            q[i]=table[i][len(A[0])+1]
            temp1=temp1+table[i][len(A[0])+1]
    #print(q)

    temp1 = 1 / temp1

    for i in range(len(q)):
        q[i]=q[i]*temp1
    for i in range(1,len(A[0])+1):
        if table[0][i] == "x"+str(i):
            p[i]=table[len(A)+1][i]
            temp2=temp2+table[len(A)+1][i]
    #print(p)

    temp2=1/temp2
    for i in range(len(p)):
        p[i]=p[i]*temp2
    return p,q,value
