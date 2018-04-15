import numpy as np

def int_to_coord(n):
	return [n/10, n%10]

def coord_to_int(c):
	return (c[0]*10 + c[1])

#the number of possible state values
K = 100
matrix = []
freep = 0
obs = []
ROW = 10
COL = 10
pie = []
NO_TOWERS = 4
gtower = [[0,0],[0,9],[9,0],[9,9]]
emip = []

def free_space(i,j):
    count = 0
    if i-1 >= 0:
        if matrix[i - 1, j] == 1:
                count += 1
    if i+1 <=  9:
        if matrix[i + 1, j] == 1:
                count += 1
    if j-1 >= 0:
            if matrix[i, j - 1] == 1:
                count += 1
    if j+1 <= 9:
        if matrix[i, j + 1] == 1:
                count += 1
    return count

def trans_prob(x1,y1,x2,y2):

    if matrix[x2,y2] == 0:
        return 0
    if x1==x2 and y1==y2:
        return 0
    if x1 != x2 and y1 != y2:
        return 0
    if abs(x2 -x1) > 1 or abs(y2 -y1) >1:
        return 0
    freespaces = free_space(x1, y1)
    return float(1)/freespaces

def cal_freep():
    count = 0
    for i in range(0,ROW):
        for j in range(0,COL):
            if(matrix[i][j] == 1):
                count = count+1
    return count

def pie_init():
    pi = []
    global freep
    global matrix
    for i in range(0,ROW):
        for j in range(0,COL):
            if matrix[i][j] == 1:
                pi.append(float(1)/freep)
            else:
                pi.append(0)
    return pi

def emission_prob(tower, pos):
    d = np.linalg.norm(np.array(tower)-np.array(pos))
    if d == 0:
        return float(1)
    return float(1)/(d*6)

def cal_emip():
    entry = 1
    emi = []
    for i in range(0,ROW):
        for j in range(0,COL):
            entry = emission_prob((0,0),(i,j))
            entry = entry*emission_prob((0,9),(i,j))
            entry = entry*emission_prob((9,0),(i,j))
            entry = entry*emission_prob((9,9),(i,j))
            emi.append(entry)
    return emi 
def valid_for_state(state,tower, val):
    d = np.linalg.norm(np.array(int_to_coord(state)) - np.array(tower))
    if val >= round(0.7*d,1) and val <= round(1.3*d,1):
        return True
    return False

#given a state and an observed tuple, what is the probability of picking the value in given_obs
def B(state,given_obs):
    global gtower
    global NO_TOWERS
    global emip
    for i in range(0,NO_TOWERS):
        if valid_for_state(state,gtower[i], given_obs[i]) == False:
                         return 0
    return emip[state]

def find_max(itr, state, T1, T2):
    mx = 0
    maxk = -1
    global obs
    for k in range(0,ROW*COL):
        [x1,y1] = int_to_coord(k)
        [x2,y2] = int_to_coord(state)
        temp = T1[itr-1][k]*trans_prob(x1,y1,x2,y2)*B(state,obs[itr])
        if temp > mx:
            mx = temp
            maxk = k
    return (mx,maxk)
                         
def viterbi():
    global obs
    global ROW
    global COL
    T1 = []
    T2 = []                                   
    t1 = []
    t2 = []
    for i in range(0,ROW*COL):
        t1.append(pie[i]*B(i,obs[1]))
        t2.append(0)
    T1.append(t1)
    T2.append(t2)
    for i,d in enumerate(obs):
                  if i == 0:
                        continue
                  t1 = []
                  t2 = []
                  for j in range(0,ROW*COL):
                        (mx,maxk) = find_max(i,j, T1, T2)
                        t1.append(mx)
                        t2.append(maxk)
                  T1.append(t1)
                  T2.append(t2)
    z = [-1]*len(obs)
    z[len(obs)-1] = np.argmax(T1[len(obs)-1])
    for i in reversed(range(1,len(obs))):
                  z[i-1] = T2[i][z[i]]
    path = []
    for ele in z:
        path.append(int_to_coord(ele))
    return path
                         
def main():
    global matrix
    global obs
    global pie
    global emip
    matrix = np.array([[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],[1,1,0,0,0,0,0,1,1,1],[1,1,0,1,1,1,0,1,1,1],[1,1,0,1,1,1,0,1,1,1],[1,1,0,1,1,1,0,1,1,1],[1,1,0,1,1,1,0,1,1,1],[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1] ])
    #print matrix
    obs = np.array([[6.3,5.9,5.5,6.7], [5.6, 7.2, 4.4, 6.8], [7.6,9.4,4.3,5.4], [9.5,10.0,3.7,6.6], [6.0,10.7,2.8,5.8], [9.3,10.2,2.6,5.4],[8.0,13.1,1.9,9.4], [6.4,8.2,3.9,8.8], [5.0,10.3,3.6,7.2], [3.8,9.8,4.4,8.8], [3.3,7.6,4.3,8.5]])
    global freep
    freep = cal_freep()
    pie = pie_init()
    emip = cal_emip()
    print "Trajecotory of the Robot in the grid world:"
    print viterbi()
    

if __name__ == '__main__':
    main()



