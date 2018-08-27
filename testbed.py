sent_len=6



class Word():
	def __init__(self):
		self.word='sampleWord'
		self.pos='samplePOS'


sent=[]
for x in range(0,6):
	new_word=Word()
	sent.append(new_word)

for word in sent:
	print(word)
ok_lst=['c,a,r,s','b,o,a,t']
word1="a,r"

if any(word1 in s for s in ok_lst): #word1 in enumerate(ok_lst):
	print "OK"
else:
	print "NO"

						for i, item in enumerate(wordWOPOS):
							if i%2 ==0:
								entry="("+item+")"
								contextWoParens.extend(entry)
							else:
								contextWoParens.extend(item)

# class Rocket():
#     # Rocket simulates a rocket ship for a game,
#     #  or a physics simulation.
    
#     def __init__(self):
#         # Each rocket has an (x,y) position.
#         self.x = 0
#         self.y = 0
        
#     def move_up(self):
#         # Increment the y-position of the rocket.
#         self.y += 1
        
# # Create a fleet of 5 rockets, and store them in a list.
# my_rockets = []
# for x in range(0,5):
#     new_rocket = Rocket()
#     my_rockets.append(new_rocket)

# # Show that each rocket is a separate object.
# for rocket in my_rockets:
#     print(rocket)

