import time
#from threading import Thread
from tkinter import *
import random

"""class Timer(Thread):
    def __init__(self, callback, fps=60):
        Thread.__init__(self)
        self.callback = callback
        self.should_stop = False
        self.fps = fps
    def run(self):
        while True:
            time.sleep(1/self.fps)
            self.callback()
            if self.should_stop: break
    def stop(self):
        self.should_stop = True
"""
WinWidth = 400
WinHeight = 400
ObjWidth = 20
ObjHeight = 20
Width = WinWidth // ObjWidth
Height = WinHeight // ObjHeight
BackColor = 'pink'
RockColor = 'black'
SnakeColor = 'black'
FoodColors = ['white','yellow','green','blue']


root = Tk()
canvas = Canvas(root,width=WinWidth,height=WinHeight)
canvas.pack()
canvas.focus_set()


class MakeMap:
    def __init__(self, bEmpty,x,y):
        self.Empty = bEmpty
        self.x = x
        self.y = y
        
    def isEmpty(self):
        return self.Empty
    
    def setEmpty(self, bEmpty):
        self.Empty = bEmpty

Map = [[MakeMap(True,x,y) for y in range(Height)] for x in range(Width)]

def returnGrids(x,y):
    left = (x) * ObjWidth
    top = y * ObjHeight
    right = (x+1) * ObjWidth
    bottom = (y+1) * ObjHeight
    return left, top, right, bottom


def makeRocks(x,y,Dir=1,Len=10):     # 0,1 = 上下, 左右
    if Dir == 0:
        for i in range(Len):
            canvas.create_rectangle(returnGrids(x,y+i),fill=RockColor)
            Map[x][y+i].setEmpty(False)
    if Dir == 1:
        for i in range(Len):
            canvas.create_rectangle(returnGrids(x+i,),fill=RockColor)
            Map[x+i][y].setEmpty(False)

def makeFood(Len=1):    # 0,1,2,3 --> scores = 1,2,5,10
    x = random.randrange(0,Width)
    y = random.randrange(0,Height)
    sco = random.randrange(0,4)
    global scores
    left,top,right,bottom = returnGrids(x,y)
    if sco == 0:
        dot=canvas.create_rectangle(left,top,right,bottom,fill='white')
    elif sco == 1:
        dot=canvas.create_rectangle(left,top,right,bottom,fill='green')
    elif sco == 2:
        dot=canvas.create_rectangle(left,top,right,bottom,fill='blue')
    else:
        dot=canvas.create_rectangle(left,top,right,bottom,fill='red')
    time.sleep(10)
    canvas.delete(dot)
    
def drawMap(Map):
    for Col in Map:
        for Grid in Col:
            left,top,right,bottom = returnGrids(Grid.x, Grid.y)
            if Grid.isEmpty():                
                canvas.create_rectangle(left,top,right,bottom, fill=BackColor)

class FoodPoints:
    def __init__(self):
        while True:
            x = random.randrange(0,Width)
            y = random.randrange(0,Height)
            if Map[x][y].isEmpty():
                self.x,self.y = x,y
                break
        self.ind = random.choice([0,0,0,0,1,1,1,2,2,3])
        self.appearFood()
        if self.ind == 0: self.score = 1
        elif self.ind == 1: self.score = 2
        elif self.ind == 2: self.score = 5
        elif self.ind == 3: self.score = 10
        
    def appearFood(self):
        left,top,right,bottom = returnGrids(self.x,self.y)
        self.Id = canvas.create_rectangle(left,top,right,bottom,fill=FoodColors[self.ind])
        
    def disappearFood(self):
        canvas.delete(self.Id)
        
    def update(self):
        self.disappearFood()
        self.__init__()
        

class SnakeSeg:
    def __init__(self,x=5,y=5,Direction=0,FramePerStep=30):
        x = x % Width
        y = y % Height
        self.x = x
        self.y = y
        self.Id = canvas.create_rectangle(returnGrids(self.x,self.y),fill=SnakeColor)
        self.Direction = Direction
        self.FramePerStep = 30
        
    def getPos(self):
        return self.x, self.y

    def setPos(self,x,y):
        x = x % Width
        y = y % Height
        self.x = x
        self.y = y

    def occupy(self):
        x,y = self.getPos()
        Map[x][y].setEmpty(False)

    def release(self):
        x,y = self.getPos()
        Map[x][y].setEmpty(True)

class Snake:
    def __init__(self,x=5,y=5,Len=5,Direction=0,FramePerStep=15):
        self.Len = Len
        self.Direction = Direction  # 0,1,2,3 --> 上右下左
        self.FramePerStep = FramePerStep
        self.body = [0] * self.Len
        self.body[0] = SnakeSeg(x,y,self.Direction,self.FramePerStep)
        for i in range(1,self.Len):
            if self.Direction == 0:
                self.body[i] = SnakeSeg(x,y+i,self.Direction,self.FramePerStep)
            elif self.Direction == 1:
                self.body[i] = SnakeSeg(x-i,y,self.Direction,self.FramePerStep)
            elif self.Direction == 2:
                self.body[i] = SnakeSeg(x,y-i,self.Direction,self.FramePerStep)
            else:
                self.body[i] = SnakeSeg(x+i,y,self.Direction,self.FramePerStep)
        self.x = self.body[0].x
        self.y = self.body[0].y
        self.keybuf = []
        self.occupy()
        self.bCanSetDirection = True
        self.GameScore = 0
        self.isAlive = True
        
    def occupy(self):
        for i in range(self.Len):
            x,y = self.body[i].getPos()
            Map[x][y].setEmpty(False)

    def release(self):
        for i in range(self.Len):
            x,y = self.body[i].getPos()
            Map[x][y].setEmpty(True)

    def getPos(self):
        return self.body[0].x, self.body[0].y
    
    def getHeadNextStep(self):
        x,y = self.body[0].getPos()
        if self.Direction == 0: y -= 1
        elif self.Direction == 1: x += 1
        elif self.Direction == 2: y += 1
        else: x -= 1
        x = x % Width
        y = y % Height
        return x,y

    def canMove(self):
        x,y = self.getHeadNextStep()
        if x < 0 or x >= Width: return False
        if y < 0 or y >= Height: return False
        if not Map[x][y].isEmpty(): return False
        return True

    def gameOver(self):
        self.isAlive = False
        Message(root,text='Game Over',width=WinWidth,justify=CENTER).pack()
            
    
    def setPos(self,x,y):
        self.body[0].x = x
        self.body[0].y = y

    def haveFood(self):
        x,y = self.getHeadNextStep()
        #if Food.x == 0 : print(x,y)
        if x == Food.x and y == Food.y: return True
        else: return False
            
    def Move(self):
        if not self.canMove(): self.gameOver()
        else:
            if self.isAlive:
                while True:
                    if self.haveFood():
                        #print('eating')
                        newHead = SnakeSeg(Food.x,Food.y,self.Direction,self.FramePerStep)
                        self.Len += 1
                        self.body.insert(0,newHead)
                        self.x,self.y = self.body[0].x,self.body[0].y
                        self.occupy()
                        self.bCanSetDirection = True
                        self.GameScore += Food.score
                        #print(Food.score)
                        global result
                        result.set(self.GameScore)
                        #print(Food.x,Food.y)
                        Food.update()
                        #print(Food.x,Food.y)
                    else: break
                xUnit = []
                yUnit = []
                for i in range(self.Len):               
                    x,y = self.body[i].getPos()
                    xUnit.append(x)
                    yUnit.append(y)
                    if i == 0:
                        #print(self.Direction)
                        X,Y = self.getHeadNextStep()
                        #print(X,Y)
                    else:
                        X,Y = xUnit[i-1],yUnit[i-1]
                    #print(X,Y)
                    self.body[i].release()
                    left,top,right,bottom = returnGrids(X,Y)
                    #print(left,top,right,bottom)
                    canvas.coords(self.body[i].Id,left,top,right,bottom)
                    self.body[i].setPos(X,Y)
                    self.body[i].occupy()
                    # print(xUnit,yUnit)
        self.bCanSetDirection = True
        if self.keybuf:
            self.processDirection()

            
    def setDirection(self,Direction):
        #print('callback ',Direction)
        self.keybuf.append(Direction)
        self.processDirection()
       # print(self.Direction)


    def processDirection(self):
        if not self.bCanSetDirection: return
       # print('can set')
        if self.keybuf:
            #print('processing set',len(self.keybuf))
            if not (self.Direction + self.keybuf[0]) % 2 == 0 :
                self.Direction = self.keybuf[0]
                self.keybuf.pop(0)
                self.bCanSetDirection = False
              #  print(len(self.keybuf))
            else:
                self.keybuf.pop(0)
                    
                

    def getFramePerStep(self):
        return self.FramePerStep


            
            
        
def update():
    obj.Move()
    if obj.isAlive :
        canvas.after(obj.FramePerStep * 1000 // fps,update)

            
        
        
            

drawMap(Map)
obj = Snake(x=10,y=10,Len=4,FramePerStep=5)
result = IntVar()
result.set('0')
label = Label(root, textvariable=result) 
label.pack(side=BOTTOM)

Food = FoodPoints()
FramePassed = 0
"""
def TimerFunc():
    global FramePassed
    FramePassed += 1
    if FramePassed >= obj.getFramePerStep():
        FramePassed = 0
        obj.Move()
        """
canvas.bind('<Up>',lambda X:obj.setDirection(0))
canvas.bind('<Right>',lambda X:obj.setDirection(1))
canvas.bind('<Down>',lambda X:obj.setDirection(2))
canvas.bind('<Left>',lambda X:obj.setDirection(3))
fps = 60
canvas.after(obj.FramePerStep * 1000 // fps,update)

#GameTimer = Timer(TimerFunc)
#GameTimer.start()
#def atexit():
 #   GameTimer.stop()
  #  time.sleep(0.1) # 这个时间用来等待Timer退出。
  #  root.destroy()
#root.protocol('WM_DELETE_WINDOW',atexit)
root.mainloop()

        




    

        

