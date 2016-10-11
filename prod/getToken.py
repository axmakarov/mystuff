import json,requests
def GetToken(login,serviceType):
	if serviceType not in ['Metrika','Direct']:
		print 'Invalid service type'
		return None
	url = 'http://192.168.10.37:35678/TokenManagerService'
	payload = {'method':'GetToken','params':{'login':login,'serviceType':serviceType}}
	r = requests.post(url,json.dumps(payload))
	data = json.loads(r.text)
	if len(data.keys()) == 1:
		print 'Invalid login'
		return None
	return data['result']['token']