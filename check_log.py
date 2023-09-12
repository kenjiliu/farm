from farm_trans_data import days_ago

def checklog(logfile):
	readlog = open(logfile, 'r')
	lines = readlog.readlines()
	for line in lines:
		log = line.find(days_ago(0))
		if log == 0:
			readlog.close()
			return True