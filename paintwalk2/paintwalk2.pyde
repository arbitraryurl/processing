frame_size = 2480 *2

def setup():
    global img
    global frame_size
    size(frame_size,frame_size)
    frameRate(300)
    background(255)
 
#paint is tuple ((center_x,center_y), radius)
          
class walker:
    global img, frame_size
    def __init__(self,paint):
        self.sx = random(0, frame_size) #generate points outside circle
        self.sy = random(0,frame_size)
        self.x = -1000 #set starting location offscreen
        self.y = -1000
        self.t = 0
        self.perp_x = -1000
        self.perp_y = -1000
        self.paint = paint
        self.left = True
        self.right = False
        self.count = 0
        self.step_flag = False
        self.sep = random(5,10)
        self.pace = int(random(10,20))
        #self.drift = random(-0.005,0.005)
        self.drift = randomGaussian() * 0.005
        self.out = False
        
        randomRadius = random(0,paint[0][1]/2) #generate random point within circle
        randomAngle = random(0,2*PI)
        #self.inCircleX = (randomRadius * cos(randomAngle)) + paint[0][0][0]
        #self.inCircleY = (randomRadius * sin(randomAngle)) + paint[0][0][1]
        self.inCircleX = random(0,frame_size)
        self.inCircleY = random(0,frame_size)
        
        self.a = (self.inCircleX - self.sx) #generate parametric slopes <a,b> for line passing through (sx,sy) and point in circle
        self.b = (self.inCircleY - self.sy)
        
        self.wet_flag = False
        self.paint_level = 0
        #self.stickiness = random(10,20)  #higher values of stickiness make the paint fade quicker
        self.stickiness = constrain((randomGaussian()*2) + 8, 0.05, 100)
        
    def update(self):
        
        vector_mag = mag(self.a,self.b)    #used to normalized the vectors    
            
        self.x = self.sx + (self.a/vector_mag) * self.t 
        self.y = self.sy + (self.b/vector_mag) * self.t 
        self.t += 1 ### speed of center agent
        
        for ele in self.paint:
            if (sq(self.x - ele[0][0]) + sq(self.y - ele[0][1])) < sq(ele[1]/2): # if current location inside the circle
                self.wet_flag = True
                self.paint_level = 255
            
        if self.paint_level > 0:
            self.paint_level -= self.stickiness * 0.075 ###
        if self.x <0 or self.y <0 or self.x > frame_size or self.y > frame_size:
            self.out = True
            
        self.count +=1 
        
    def step(self):
        if self.count % self.pace == True: #if the # of elapsed time steps % the individual's pace is 0
            
            sep = self.sep + random(-1,1)
            r = 4
            
            #generate normal vectors
            if self.right == True:        
                perp_a = 1
                perp_b = -self.a / self.b
                perp_mag = mag(perp_a,perp_b)
                                    
            if self.left == True:            
                perp_a = -1
                perp_b = self.a / self.b
                perp_mag = mag(perp_a,perp_b)                
            
            #generate point on normal vector +- some random offset    
            self.perp_x = self.x + perp_a/perp_mag * sep + random(-r,r)
            self.perp_y = self.y + perp_b/perp_mag * sep + random(-r,r)
               
            #switch the foot
            self.left = not self.left
            self.right = not self.right
            
            #set the step flag to True
            self.step_flag = True
            
            # if self.drift > 0.5:
            #     theta = -0.1
            # if self.drift < 0.5:
            #     theta = 0.1
            
            theta = self.drift
            
            #r = random(0,10)
            if self.wet_flag:
                #rotate the movement vector by theta
                rot_a = self.a * cos(theta) - self.b * sin(theta)
                rot_b = self.a * sin(theta) + self.b * cos(theta)
                #set the offset to the current point
                self.sx = self.x
                self.sy = self.y
                #set the movement vector to the rotated vector
                self.a = rot_a
                self.b = rot_b
                #reset the timestamp
                self.t=0
            
        else:
            self.step_flag = False
        



    def d(self):
        
        stroke(0)
        fill(0)
            
        #circle(self.x, self.y, 5)
        
        if self.wet_flag and not self.out:
            stroke(255-self.paint_level,0,0)
            fill(255-self.paint_level,0,0)
        else:
            noFill()
            noStroke()
        
        if self.step_flag:
            #circle(self.perp_x, self.perp_y, 10)
            rectMode(CENTER)
            square(self.perp_x,self.perp_y,1)
            
            
def keyPressed():
    if key == 's':
        saveFrame("line-######.png")

spots = []
for i in range(8):
    th = PI/4 * i
    x = 1000 * cos(th) + frame_size/2
    y = 1000 * sin(th) + frame_size/2
    spots.append(((x,y),400))
    
#spots = [((frame_size/2, frame_size/2),100), ((frame_size/2+200, frame_size/2+200),100)]
w = []
for i in range(4000):
    w.append(walker(spots))

def draw():
    global w
    #circle(540,540,100)
    for ele in w:
        ele.update()
        ele.step()
        ele.d()
    
    
    
    
