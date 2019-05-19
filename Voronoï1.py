# Voronoi

import tkinter as tk
from math import *
from time import*
import random as rd

rayon = 5
dist = 10000
points = list()
triangles = list()
mardi=True

def onClick(event):
    global mardi
    if mardi:
        print(event.x, event.y)
        fen.cv.create_oval(event.x-rayon, event.y-rayon, event.x+rayon, event.y+rayon, width=1, fill="green",outline="black")
        points.append((event.x,event.y))
    else:
        print(event.x, event.y)
        fen.cv.create_oval(event.x-rayon, event.y-rayon, event.x+rayon, event.y+rayon, width=1, fill="green",outline="black")
        points.append((event.x,event.y))
        print(points)
        fen.cv.delete(tk.ALL)
        triangles[:]=[]
        for i in range(3,len(points),1):
            fen.cv.create_oval(points[i][0]-rayon, points[i][1]-rayon, points[i][0]+rayon, points[i][1]+rayon, width=1, fill="green",outline="black")
        Calculer()

def Distance(A,B):
    return int(sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2))

def cercle_circonscrit(A,B,C):
    Y=((B[0]**2+B[1]**2 - (A[0]**2+A[1]**2)),(C[0]**2+C[1]**2 - (A[0]**2+A[1]**2)))
    A = ((B[0]-A[0] ,B[1]-A[1]),(C[0]-A[0] ,C[1]-A[1]))
    detA = A[0][0]*A[1][1]-A[1][0]*A[0][1]
    invA = ((A[1][1],-A[0][1]),(-A[1][0],A[0][0]))
    X = ((1/2)*(1/detA)*(invA[0][0]*Y[0]+invA[0][1]*Y[1])),((1/2)*(1/detA)*(invA[1][0]*Y[0]+invA[1][1]*Y[1]))
    return X

def Calculer():

    global L
    if L!=[]:
        for i in range(len(L)):
            points.append((L[i][0],L[i][1]))
    for a in range (len(points)):
        for b in range (a + 1,len(points)):
            for c in range (b + 1,len(points)):
                pointDansCercle = False
                x = 0
                while not(pointDansCercle) and x < len(points):
                    centre = cercle_circonscrit(points[a],points[b],points[c])
                    pointDansCercle =  Distance(centre,points[x]) < Distance(centre,points[a])
                    x = x + 1
                if not(pointDansCercle) and mardi:
                    triangles.append((points[a],points[b],points[c],centre))
                    rayon2 = Distance(centre,points[a])
                    fen.cv.create_oval(centre[0]-rayon, centre[1]-rayon, centre[0]+rayon, centre[1]+rayon, width=0, fill="white")
                    fen.cv.create_oval(centre[0]-rayon2, centre[1]-rayon2, centre[0]+rayon2, centre[1]+rayon2, width=1, fill='', outline="orange")
                    fen.cv.create_line(points[a][0], points[a][1], points[b][0], points[b][1], width=1, fill="red")
                    fen.cv.create_line(points[a][0], points[a][1], points[c][0], points[c][1], width=1, fill="red")
                    fen.cv.create_line(points[b][0], points[b][1], points[c][0], points[c][1], width=1, fill="red")
                elif not(pointDansCercle) and not mardi:
                    triangles.append((points[a],points[b],points[c],centre))
                    rayon2 = Distance(centre,points[a])
                    #fen.cv.create_oval(centre[0]-rayon, centre[1]-rayon, centre[0]+rayon, centre[1]+rayon, width=0, fill="white")
                    #fen.cv.create_oval(centre[0]-rayon2, centre[1]-rayon2, centre[0]+rayon2, centre[1]+rayon2, width=1, fill='', outline="orange")
                    fen.cv.create_line(points[a][0], points[a][1], points[b][0], points[b][1], width=2, fill="blue")
                    fen.cv.create_line(points[a][0], points[a][1], points[c][0], points[c][1], width=2, fill="blue")
                    fen.cv.create_line(points[b][0], points[b][1], points[c][0], points[c][1], width=2, fill="blue")
    
    for v in range (len(triangles)):
        for w in range (v + 1,len(triangles)):
            diff = list(set(triangles[v]).symmetric_difference(triangles[w]))
            if len(diff)==4 and mardi:
                fen.cv.create_line(triangles[v][3][0], triangles[v][3][1], triangles[w][3][0], triangles[w][3][1], width=4, fill="green")
            elif len(diff)==4 and not mardi:
                fen.cv.create_line(triangles[v][3][0], triangles[v][3][1], triangles[w][3][0], triangles[w][3][1], width=3, dash=(20), fill="green")
    print("END")

def Reset():
    fen.cv.delete(tk.ALL)
    points[4:]=[]
    triangles[:]=[]
    print(points,triangles)
    global L, mardi
    L=[]
    mardi=True


L=[]
def alea():
    global L
    for i in range(5):
        P=[rd.randint(50,850),rd.randint(50,550)]
        if L!=[]:
            valide=True
            for k in range(len(L)):
                if abs(L[k][0]-P[0])<20 and abs(L[k][1]-P[1])<20:
                    valide=False
            if valide:
                L=L+[P]
            else:
                print("pt ",(i+len(L))," and ",(k+len(L)),"exception(points trop proches)")                  
        else:
            L=[P]
        for i in range(len(L)):
            fen.cv.create_oval(L[i][0]-5,L[i][1]-5,L[i][0]+5,L[i][1]+5,fill="green",outline="black")
    print(L)    
    return(L)
    





#methode balayage



    
def voronoi():
    pas = eval(fen.rep1.get())
    global L

    if points!=[]:
        for i in range(3,len(points),1):
            L=L+[[points[i][0],points[i][1]]]
        print(L)
                
    P=[]
    tag=fen.cv.create_line(0,0,0,600,fill='cyan',width=5)
    for i in range (0,900,pas):
        for j in range (0,600,pas):
            S=[i,j]
            distance1=100000
            distance2=100000
            for k in range (len(L)):
                if Distance(L[k],S)<distance1:
                    distance1=Distance(L[k],S)
                    P=L[k]
            for m in range (len(L)):
                if Distance(L[m],S)<distance2 and L[m]!=[P[0],P[1]] and m==0:
                    distance2=Distance(L[m],S)
                    P=P+L[m]
                if Distance(L[m],S)<distance2 and L[m]!=[P[0],P[1]] and m!=0:
                    distance2=Distance(L[m],S)
                    P=P+L[m]
                    del P[2]
                    del P[2]
            if distance1==distance2:
                co=fen.cv.coords(tag)
                if co[0]<S[0]:
                  for j in range(int(S[0]-co[0])):
                    fen.cv.move(tag,1,0)
                fen.cv.create_oval(S[0]-2.5,S[1]-2.5,S[0]+2.5,S[1]+2.5,fill='black')
                fen.update()
    fen.cv.move(tag,400,0)
    print("END")
    




#methode hossam

def hossam():
    global mardi
    mardi=False
    

#interface global

def init_UI():
    fen.title("Voronoi")

    fen.cv = tk.Canvas(fen, bg="light pink", height=600, width=900)
    fen.cv.pack()
    fen.cv.bind("<Button-3>", onClick)

    fen.btnQuitter = tk.Button(fen,bg="red",width=20, text="Quitter", command = fen.destroy).pack(side="right")
    fen.btnReset = tk.Button(fen,fg="blue",width=20,bg="light blue", text="Reset", command = Reset).pack(side="right")  
    fen.btnAlea = tk.Button(fen, text="Generation aleatoire",fg="blue",width=20,bg="light blue", command = alea).pack(side="left")
    fen.btnCalculer = tk.Button(fen, text="Calculer(1)",fg="blue",width=20,bg="light blue", command = Calculer).pack(side="left")
    fen.btnVoro = tk.Button(fen, text="balayage(2)",fg="blue",width=20,bg="light blue", command = voronoi).pack(side="left")
    fen.pas = tk.Label(fen,text='pas = ',fg='blue')
    fen.pas.pack(side="left")
    fen.rep1 = tk.Entry(fen,bg="light blue",fg="red")
    fen.rep1.pack(side="left")
    fen.btnhossam = tk.Button(fen, text="Delaunay(3)",fg="blue",width=20,bg="light blue", command = hossam).pack(side="left")

    points.append((-dist,-dist))
    points.append((dist,-dist))
    points.append((-dist,dist))
    points.append((dist,dist))

    return fen


if __name__ == '__main__':
    fen = tk.Tk()
    fen = init_UI()
    fen.mainloop()