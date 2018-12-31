import config
import requests 

v = config.v
access_token = config.access_token
api_url = config.api_url


class Node:
	def __init__(self, user_id, links, name = None, surname = None):
		self.user_id = user_id
		self.name = name
		self.surname = surname
		self.links = links

	def __repr__(self):
		return 'id:{} links:{}'.format(self.user_id, self.links)

def main():
	user_id = input()
	query = 'friends.get?user_id={}&v={}&access_token={}'
	r = requests.get(api_url + query.format(user_id, v, access_token))
	root =  [Node(user_id = user_id, links = [ item for item in  r.json()['response']['items'] ])] 
	data = [root]			
	print(data)


if __name__=='__main__':
	main()


