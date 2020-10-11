import numpy as np
import time

class Game:
	"""docstring for Game"""
	def __init__(self, vision, controller):
		self.vision = vision
		self.controller = controller
		self.state = 'Menu'

	def can_see_object(self, template, threshold_=0.9):
		matches = self.vision.find_templates(template, threshold=threshold_)
		return np.shape(matches)[1] >= 1

	def click_object(self, template, offset=(0,0), click = True, scaling = False, threshold = 0.9):
		if not scaling :
			matches = self.vision.find_templates(template, None, threshold = threshold)
		else :
			matches = self.vision.scaled_templates(template, None, threshold = threshold)
		
		if len(matches[0]):
			x = matches[1][0] + offset[0]
			y = matches[0][0] + offset[1]
			print('X : {0} , Y : {1}'.format(x,y))
			self.controller.set_mouse_position(x,y)
			if(click):
				self.controller.left_mouse_click()
		time.sleep(0.2)
		return matches


	def test_db(self):
		return self.can_see_object('test_db')

	def dice_sel(self):
		return self.can_see_object('dice')

	def stage_not_clear(self):
		return self.can_see_object('u_star')

	def combat_state(self):
		return self.can_see_object('types')

	def end_combat(self):
		return self.can_see_object('end')

	# Check first if object is avalaible ?
	def run(self, state = 'Menu', sel = 'quest'):
		self.state = state;

		while True : 
			# Menu Selection
			if(self.state == 'Menu'):
				self.click_object('depart', scaling = True , offset = (50,50),threshold = 0.7)
				self.vision.refresh_frame();
				time.sleep(0.3)
				self.click_object(sel, scaling = True, offset = (50,50), threshold = 0.6)
				if(len(self.click_object('terre', scaling=True, click = False , threshold = 0.6)[0]) > 0):
					self.state = 'Selection'
					print(self.state)

			# Stage Selection
			if(self.state == 'Selection'):
				self.vision.refresh_frame();
				pos = self.click_object('stage_sel', scaling = True, click = False)
				if(len(pos[0]) > 0):
					x = pos[1][0] ; y = pos[0][0];
					if(self.stage_not_clear()) :
						self.controller.set_mouse_position(x,y)
						time.sleep(0.5)
						self.controller.left_mouse_click();
						self.vision.refresh_frame();
						self.state = 'Difficulty'
					elif(not self.stage_not_clear()):
						time.sleep(0.5)
						self.controller.left_mouse_drag((x + 50 , y),( x + 50, y - 50))
						time.sleep(1)

			# Difficulty Selection
			if(self.state == 'Difficulty'):
				self.click_object('stage_nc', scaling = False, click = True, offset = (50,50))
				time.sleep(0.7)
				self.controller.left_mouse_click();
				self.vision.refresh_frame();
				time.sleep(0.2);
				if(len(self.click_object('start',scaling = False, click = True, offset = (10,10))[0]) > 1) :
					self.state = 'Combat'

			# Dice Selection
			if (self.state == 'Dices'):
				self.click_object('dice', scaling = True, click = True, offset = (20,-20))
				time.sleep(2)
				self.vision.refresh_frame();
				if((len(self.click_object('gauche',scaling = True, click = True, offset = (10,10))[0]) > 1)  or (len(self.click_object('droite',scaling = True, click = True, offset = (10,10))[0]) > 1) ) :
						print('Arrow selection')
						time.sleep(1)
						self.vision.refresh_frame();
				if(self.combat_state()):
					self.state = 'Combat'

			# Combat State
			if(self.state == 'Combat'):
				self.click_object('ki', scaling = False, click = True, offset = (0,-180),threshold = 0.8)
				time.sleep(1)
				self.vision.refresh_frame();
				if(len(self.click_object('KO', scaling = False, click = True, offset = (0,0),threshold = 0.8)[0] > 1)):
						self.vision.refresh_frame();
						time.sleep(1)
						self.controller.left_mouse_click();
				if(self.end_combat()):
					self.click_object('end', offset = (150,150), click = True)
					time.sleep(0.5)
					if(self.dice_sel()):
						self.state = 'Dices'
					else : 
						self.controller.left_mouse_click();
						self.vision.refresh_frame()
			

			# Dicing state

			#



		#if(self.state == 'Selection')
	def test(self):
		self.click_object('types', scaling = False, click = False, offset = (0,200),threshold = 0.7)
		print(self.can_see_object('u_star',threshold_ = 0.8))
		



			