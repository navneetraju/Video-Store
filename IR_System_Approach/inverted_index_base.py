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

