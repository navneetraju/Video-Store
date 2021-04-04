import requests
import Constants
import properties
import json
import isodate
import time

class YoutubeDataAPI:
	def __getVideoDuration(self,videoId):
		request = Constants.YOUTUBE_DATA_API_BASE_PATH.format(videoId,properties.GOOGLE_API_KEY)
		res = requests.get(request)
		res = res.json()
		iso_duration = res['items'][0]['contentDetails']['duration']
		return isodate.parse_duration(iso_duration).seconds

	def getFinalYoutubeURL(self,videoURL,start_frame):
		#duration = self.__getVideoDuration(videoId)
		fps = 30
		start_head = time.strftime("%Mm%Ss", time.gmtime(round(start_frame/fps,2)))
		return videoURL+"#t="+start_head
