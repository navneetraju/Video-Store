from inverted_index_base import *
from clip_vid import *
from query_parser import *

'''
Use this file for integration of all modules and system testing.
Each module has to be written in a seperate .py file and imported as above
This helps code maintenance and debugging.
'''

if __name__ =="__main__":
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