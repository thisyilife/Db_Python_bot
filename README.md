Bot made with Python and OpenCV to perform basic tasks in a Android game (unnamed here for obvious reasons), 
inspired by https://www.tautvidas.com/blog/2018/02/automating-basic-tasks-in-games-with-opencv-and-python/
The game is executed via an emulator on computer in order to have the bot recognize the pattern.
The bot is based on a state machine following the game state:
	- Menu State :
		Selection of the game mode.
			
	- Level Selection :
		Scrolling to get to an uncompleted level.
		
	- Navigation State : 
		Choose randomly a dice to progress in the level.

	- Combat State : 
		Pick randomly a "bubble" to complete the combat.
		
Further details will be given, currently the bot only complete a level without going to a new one.
More features will be added in the near future.
