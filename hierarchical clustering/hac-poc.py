print "Welcome to HAC-POC..."

class Point:
        
    def _init_(self,x,y):
        self.x = x
        self.y = y
        
    def setX(self,x):
        self.x = x
        
    def setY(self,y):
        self.y = y
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def show(self):
        print "X = ", self.x, " and Y = ", self.y
        
    
points = []

p1 = Point(2,3)
p1.show()

points.append(Point(1,2))
points.append(Point(1,5))
points.append(Point(2,6))
points.append(Point(3,1))
points.append(Point(3,8))

for p in points:
    p.show()
