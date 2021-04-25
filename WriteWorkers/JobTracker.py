from pymongo import MongoClient
from datetime import datetime

class JobTracker:
	def __init__(self):
		self.mongo_connect=MongoClient('mongodb://%s:%s@10.10.1.146:27017' % ("root", "CLCFVSItr1"))

	def markPushingJob(self,uuid,status):
		job_db=self.mongo_connect['jobs']
		job_col=job_db["jobs"]
		st = dict()
		st['status'] = status
		st['timestamp'] = str(datetime.now())
		jobDoc = list(job_col.find({"jobId":uuid}))
		if len(jobDoc) != 0:
				jobDoc = jobDoc[0]
				jobDoc['logs'].append(st)
				newvalues={"$set":jobDoc}
				job_col.update_one({"jobId":uuid},newvalues)
				return {'detail':'Updated job successfully'}
		else:
			job_dict = {"jobId":uuid,"logs":[st]}
			job_col.insert_one(job_dict)

	def getJobStatus(self,uuid):
		job_db=self.mongo_connect['jobs']
		job_col=job_db["jobs"]
		mongo_fetch_query={'jobId':uuid}
		fetched_doc=job_col.find(mongo_fetch_query)
		fetched_doc=list(fetched_doc)
		if len(fetched_doc)==0:
			return {"status":400,"message":"Job not found"}
		else: 
			job = fetched_doc[0]
			del job['_id']
			return {"status":200,"job":job}