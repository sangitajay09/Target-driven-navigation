
import ai2thor.controller
import collections
import heapq
import time
class obn:
	def __init__(self):
		self.dict1=collections.defaultdict(int)
		self.controller = ai2thor.controller.Controller()
		self.controller.reset('FloorPlan3')
        
		self.event = self.controller.step(dict(action='GetReachablePositions'))
		for i in self.event.metadata['actionReturn']:
			self.dict1[i['x'],i['z']]=float('inf')
        
		self.dict1[self.event.metadata['agent']['position']['x'],
		self.event.metadata['agent']['position']['z']]=0
		#print(self.dict1)        
		#print(self.agentx,self.agentz)
		self.queue=[]
		self.queue.append((self.event.metadata['agent']['position']['x'],
		self.event.metadata['agent']['position']['z']))
		self.queue1=set()
		self.queue1.add((self.event.metadata['agent']['position']['x'],
		self.event.metadata['agent']['position']['z']))
		self.heap=[]  
		self.dict2=collections.defaultdict(list)
		self.A=""
		self.B=""
		self.C=""
		self.D=""		 
		#print(self.queue1)
	def d_grid(self):
		#print(self.dict1)
		pass
		#print(self.dict2[(0.25,-1.25)])
    
	def dfs(self):
		distance1=0
		count=0 
		#print(self.dict2)
		while self.queue:
			count+=1            
			#print(distance1,self.queue)
			distance=0.25
			#distance1+=0.25
			x,y= self.queue.pop(0)
			distance1=self.dict1[(x,y)]+0.25
			self.queue1.add((x,y))
			#print(self.queue1)									
			if len(self.queue1)==len(self.dict1):
    			     break
			if (x+distance,y) in self.dict1 and (x+distance,y) not in self.queue1:
    			     
    			     if self.dict1[(x+distance,y)]>distance1:
                        
    			     	self.dict1[(x+distance,y)]=distance1
    			     	self.dict2[(x+distance,y)]=self.dict2[(x,y)].copy()
    			     	if (x,y) not in self.dict2[x+distance,y]:
    			     		self.dict2[(x+distance,y)].append((x,y))
                             
    			     		#self.dict2[(x+distance,y)].append((x,y))
    			     		#print(self.dict2)

    			     	#print(self.dict1[(x+distance,y)],x+distance,y,self.dict2[(0.25,-1.25)],self.dict2) 
    			     	   			     		         			                          
    			     self.queue.append((x+distance,y))
    			     #self.queue1.append((x+distance,y))                    
			if (x-distance,y) in self.dict1 and (x-distance,y) not in self.queue1:
    			    # print(x,y,x-distance,y)
    			     if self.dict1[(x-distance,y)]>distance1:
                        
    			     	self.dict1[(x-distance,y)]=distance1
    			     	self.dict2[(x-distance,y)]=self.dict2[(x,y)].copy()
    			     	if (x,y) not in self.dict2[(x-distance,y)]:
    			     		self.dict2[(x-distance,y)].append((x,y))
    			     	#print(self.dict1[(x-distance,y)],x,y,self.dict2[(0.25,-1.25)],self.dict2) 
    			     		         			                          
    			     self.queue.append((x-distance,y))
    			     #self.queue1.append((x-distance,y))
			if (x,y-distance) in self.dict1 and (x,y-distance) not in self.queue1:
    			     if self.dict1[(x,y-distance)]>distance1:
                        
    			     	self.dict1[(x,y-distance)]=distance1
    			     	self.dict2[(x,y-distance)]=self.dict2[(x,y)].copy()
    			     	if (x,y) not in self.dict2[(x,y-distance)]:
    			     		self.dict2[(x,y-distance)].append((x,y))
    			     	#print(self.dict1[(x,y-distance)],x,y,self.dict2[(0.25,-1.25)],self.dict2[(x,y-distance)],self.dict2) 
    			     		         			                          
    			     self.queue.append((x,y-distance))
    			     #self.queue1.append((x,y-distance))
			if (x,y+distance) in self.dict1 and (x,y+distance) not in self.queue1:
    			     if self.dict1[(x,y+distance)]>distance1:
                        
    			     	self.dict1[(x,y+distance)]=distance1
    			     	self.dict2[(x,y+distance)]=self.dict2[(x,y)].copy()
    			     	if (x,y) not in self.dict2[(x,y+distance)]:
    			     		self.dict2[(x,y+distance)].append((x,y))
    			     	#print(self.dict1[(x,y-distance)],x,y-distance,self.dict2[(0.25,-1.25)],self.dict2) 
    			     		         			                          
    			     self.queue.append((x,y+distance))

    			     #self.queue1.append((x,y+distance))
			#print(self.dict2)
			#if count==3:
    			#     break

        
	def ini_objects(self,inp):
		#for o in self.event.metadata['objects']:
		#	print(o['objectType'])
         
		self.event=self.controller.step(dict(action='Initialize', gridSize=0.25))	
        
		for o in self.event.metadata['objects']:
			if o['objectType']==inp:
    			     self.event = self.controller.step(dict(action='GetReachablePositions'))
    			     x= self.closest_position(o['position'],self.event.metadata['actionReturn'])             
    			     print(x)
    			     
    			     heapq.heappush(self.heap,(self.dict1[(x["x"],x["z"])],(o['position']['x'],o['position']['z']),(x["x"],x["z"]),inp))
	def closest_position(self,object_position,reachable_positions):
        
		out = reachable_positions[0]
		min_distance = float('inf')
		for pos in reachable_positions:
            # NOTE: y is the vertical direction, so only care about the x/z ground positions
			dist = sum([(pos[key] - object_position[key]) ** 2 for key in ["x", "z"]])
			if dist < min_distance:
    			     min_distance = dist
    			     out = pos
		return out        
	def get_next(self):
		dist,rco,gridco,name=heapq.heappop(self.heap)	
		self.dict2[gridco].append(gridco)
		#print(self.heap)        
		#print(self.dict2[gridco],name)	
		        
		i,j=self.dict2[gridco][0]		        
		for i1,j1 in self.dict2[gridco][1:]:
			if i1>i:
    			     i=i1        
    			     self.event = self.controller.step(dict(action=self.B))
			if i1<i:
    			     i=i1        

    			     self.event = self.controller.step(dict(action=self.A))
			if j1<j:
    			     j=j1        

    			     self.event = self.controller.step(dict(action=self.C))
			if j1>j:
    			     j=j1        
            
    			     self.event = self.controller.step(dict(action=self.D))
                
		time.sleep(3)
		self.event = self.controller.step(dict(action="RotateRight")) 
		time.sleep(3)           
		self.event = self.controller.step(dict(action="RotateRight"))
		time.sleep(3)
		self.event = self.controller.step(dict(action="RotateRight"))
		time.sleep(3)
		self.event = self.controller.step(dict(action="RotateRight"))    			     	        
	def x_round(self,x,y):
		
		x=round(x*4)/4
		y=round(x*4)/4  
		while(True):
			if (x,y) in self.dict1:
    			     return (x,y)
			else:
    			     return self.nearest(x,y)   
	def checkxy(self):
		x=self.event.metadata['agent']['position']['x']
		y=self.event.metadata['agent']['position']['z'] 
		self.event = self.controller.step(dict(action='MoveLeft')) 
		x1=self.event.metadata['agent']['position']['x']
		y1=self.event.metadata['agent']['position']['z'] 
		print(x,x1,y1,y)
		if x1>x:
			self.B='MoveLeft'
			self.A='MoveRight'
		if x1<x:
			self.B='MoveRight'
			self.A='MoveLeft'            
		if y1>y:
			self.D='MoveLeft'
			self.C='MoveRight'
		if y1<y:
			self.D='MoveRight'
			self.C='MoveLeft'
		self.event = self.controller.step(dict(action='MoveRight')) 
		x=self.event.metadata['agent']['position']['x']
		y=self.event.metadata['agent']['position']['z'] 
		self.event = self.controller.step(dict(action='MoveAhead'))  
		x1=self.event.metadata['agent']['position']['x']
		y1=self.event.metadata['agent']['position']['z']          
		if y1>y:
			self.C='MoveBack'
			self.D='MoveAhead'  
		if y1<y:
			self.C='MoveAhead'
			self.D='MoveBack' 
		if x1>x:
			self.A='MoveBack'
			self.B='MoveAhead'
		if x1<x:
			self.A='MoveAhead'
			self.B='MoveBack'
		self.event = self.controller.step(dict(action='MoveBack'))   
		print(self.A,self.B,self.C,self.D)        
	def nearest(self,x,y):
			x1=x+0.25
			y1=y+0.25
			x2=x-0.25
			y2=y-0.25
			if (x1,y1) in self.dict1:
    			     return (x1,y1) 
			elif (x2,y2) in self.dict1:
    			     return (x2,y2)
			else:
    			     return (x,y)                 
            
   			            
		#res = self.dict1.get((x,y)) or self.dict1[min(self.dict1.keys(), key = lambda key: abs(key-(x,y)))]
#list1=['Fridge','Microwave','Bread','Potato','Knife','Toaster','CoffeeMachine','Microwave','Sink','Bottle','Fork','Pan','Lettuce','Plate','Apple','Pot']			
list1=['Fridge']
obj=obn()
#obj.d_grid()
obj.dfs()
obj.d_grid()
for i in list1:
    
    obj.ini_objects(i)
    
obj.checkxy()
obj.get_next()

    
#obj.d_grid()



