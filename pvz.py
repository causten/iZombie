

TICSPERSECOND  = 3
STEPSPERBLOCK  = 3
BITESPERSECOND = 2

class zombie():

	def __init__(self, zb, blockpos):
		self.zb = []
		self.zb = zombiesTable[zb]
		self.xpos = STEPSPERBLOCK*blockpos 
		self.name = zb

	def printStats(self):
		print(self.name, 'Speed=',self.zb[0], ", Damage=", self.zb[1], ", Helmet=", self.zb[2], ", Shield=", self.zb[3], "Blockpos", self.xpos)

	def walk(self, tics):
		if (tics%self.zb[0]) == 0:
			self.xpos-=1

	def getPos(self):
		return self.xpos

	def attacked(self, attack):

		if self.zb[2] > 0:
			self.zb[2] -= attack 

			# IF the plant hit hard enough to knock off the helmet and more
			# then add teh extra damage to the body
			if self.zb[2] < 0: 
				self.zb[1] += self.zb[2]
		
		else:
			self.zb[1] -= attack

		if self.zb[1] <= 0 : 
			print(self.name,'is dead')

	def isHealthy(self):
		healthy = False
		if self.zb[1] > 0:
			healthy = True

		return healthy

	def onMap(self):
		onboard = False
		if self.xpos > 0:
			onboard = True
		return onboard

	# Is there a plant in front of me?
	def canBite(self, p):

		# Am I infront of a plant and can it be eaten
		if ((self.xpos) == p.xpos+STEPSPERBLOCK) and (p.p[3] > 0):
			#print ("can bite", p.name)
			return True
		return False




class plant():

	def __init__(self, p, blockpos):
		self.p = []
		self.p = plantTable[p]
		self.name = p
		self.xpos = STEPSPERBLOCK*blockpos

	def shoot(self, tic):
		attack = 0
		
		if ((tic%TICSPERSECOND) == 0):
			attack = self.p[2]

		# Some plants are one and done.  Need to clear them off the map
		if self.p[4] == 1 :
			self.p = plantTable['blank']
			self.name = 'blank'

		return attack

	def canShoot(self, zb):
		# where is the zombie
		# where am I
		# if close enough then we can
		zpos = zb.getPos()
		if (zpos >= self.xpos) and (zpos < (self.xpos+(self.p[1]*3))):
			return True
		return False

	def bitten(self, zb, tics):
		if (tics%BITESPERSECOND) == 0:
			print (self.name, 'is bitten')
			self.p[3] -= 1

		if self.p[3] == 0:
			self.xpos = 0
			print (self.name, 'is dead')

		

# http://en.uncyclopedia.co/wiki/Plants_vs_Zombies_war_%28Walkthrough%29/List_of_zombies
zombiesTable = {		# Speed, Body, Helmet, Shield, cost
	'normal' : [6, 10, 0,  0, 100],
	'cone' 	 : [6, 10, 18, 0, 125],
	'bucket' : [6, 10, 60, 0, 150], 
	'imp'    : [3, 6,  0,  0,  50], 
	'helmet' : [3, 10, 70, 0, 175] 
}

plantTable = { # Attack Speed, attack range,  Damage, body damage, single attack?
	'sun'        : [0, 1, 0,   4,   0],
	'peashooter' : [1, 8, 1,   4,   0],
	'wallnut'    : [0, 1, 0,   72,  0],
	'tallnut'    : [0, 1, 0,   144, 0],
	'spikeweed'  : [1, 1, 1,   0,   0],
	'squash'     : [1, 1, 300, 0,   1],
	'potatoe'    : [1, 1, 300, 0,   1],
	'mushroom'   : [1, 4, 1,   4,   0],
	'venus'      : [1, 1, 300, 0,   1],
	'torch'		 : [0, 1, 2,   4,   0],
	'blank'		 : [0, 1, 0,   0,   0]
}

def gameOn(players):

	playon = False

	for val in players:
		if val.onMap() and val.isHealthy(): 
			playon = True
			break

	return playon


mapTable = []
#mapTable = ['peashooter','squash','spikeweed', 'wallnut']
mapTable = ['peashooter','wallnut','spikeweed']

z1 = zombie('helmet', 5)
z2 = zombie('bucket', 4)


p = []
x=0
for i in mapTable:
	p.append(plant(i,x))
	x+=1


players = []
players = [z1]

gametics = 0
while(gameOn(players)):
#while(gametics < 100):
		
	for z in players:
		if not z.isHealthy():
			continue

		z.printStats()

		bitting = False
		for plants in p:
			if z.canBite(plants):
				plants.bitten(plants, gametics)
				bitting = True

		# cant eat and walk at the same time
		if bitting == False:
			z.walk(gametics)


		for plants in p:
			if plants.canShoot(z):
				z.attacked(plants.shoot(gametics))

	gametics += 1

	




