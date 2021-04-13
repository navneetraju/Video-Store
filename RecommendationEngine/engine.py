
from Neo4jConnection import Neo4jConnection
import Constants
import properties
import logging
from cache import timed_lru_cache
logging.basicConfig(format='%(asctime)s %(message)s',level=properties.LOG_LEVEL)

class QueryEngine:

    def __init__(self):
        self.conn = Neo4jConnection(uri=properties.NEO4J_SERVER_URL, user=properties.NEO4J_SERVER_USERNAME, pwd=properties.NEO4J_SERVER_PASSWORD)

    @timed_lru_cache(300)
    def get_recommendation(self,videoId,start_frame,end_frame,dbName):

        recommendation_query = Constants.NEO4J_RECOMMENDATION_QUERY(videoId,start_frame,end_frame)

        try:
            results =  self.conn.query(recommendation_query,db=dbName)
            logging.info("Recommendation Provided")
            return [dict(video['p2']) for video in results]
        except:
            logging.error('ERROR providing recommendation')
            return 0




