import hashedindex
from collections import Counter

class InvertedIndex:
	def __init__(self):
		self.index=hashedindex.HashedIndex()

	def add_sport_action(self,sport,action,video):
		self.index.add_term_occurrence(sport,video)
		self.index.add_term_occurrence(action,video)

	def get_sport(self,sport):
		try:
			res=dict(self.index.get_documents(sport))
		except:
			return None
		return res

	def get_sport_activity(self,sport,activity):
		try:
			term1 = dict(self.index.get_documents(sport))
			term2 = dict(self.index.get_documents(activity))
		except:
			return None
		final_dict = dict(term1.items() & term2.items()) 
		return final_dict

if __name__=="__main__":
	index = InvertedIndex()
	index.add_sport_action('cricket','bowling','video1.mp4')
	index.add_sport_action('cricket','batting','video2.mp4')
	index.add_sport_action('cricket','fielding','video3.mp4')
	index.add_sport_action('cricket','bowling','video4.mp4')
	index.add_sport_action('swimming','freestyle','video5.mp4')
	index.add_sport_action('swimming','breaststroke','video6.mp4')

	print('All videos in which sport is CRICKET and action is BOWLING')
	print(index.get_sport_activity('cricket','bowling'))

	print('All CRICKET videos')
	print(index.get_sport('cricket'))

	print('All SWIMMING videos')
	print(index.get_sport('swimming'))

	print('All SWIMMING videos where person is doing freestyle')
	print(index.get_sport_activity('swimming','freestyle'))

	print('All RUGBY videos')
	print(index.get_sport('rugby'))