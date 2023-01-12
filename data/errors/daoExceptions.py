class dataManipulationError(Exception):
	def __init__(self, message):
		self.message = message

class notPodcastOwnerError(Exception):
	def __init__(self, message):
		self.message = message