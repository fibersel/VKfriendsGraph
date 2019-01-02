import config
import requests 
import igraph as ig
from plotly import offline
import plotly.plotly as py
import plotly.graph_objs as go





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
		return 'id:{} links:{}\n'.format(self.user_id, self.links)


def GraphPlot(data, labels):
	G = ig.Graph(edges=[(node.user_id, dest) for node in data for dest in node.links])
	layt = G.layout('kk', dim=3)
	N = len(layt)
	Xn=[layt[k][0] for k in range(N)]# x-coordinates of nodes
	Yn=[layt[k][1] for k in range(N)]# y-coordinates
	Zn=[layt[k][2] for k in range(N)]# z-coordinates
	Xe = []	
	Ye = []
	Ze = []
	for k in range(N-1):
    		Xe += [layt[k][0], layt[k + 1][0], None] 
    		Ye += [layt[k][1], layt[k + 1][1], None]
    		Ze += [layt[k][2], layt[k + 1][2], None]
	
	trace1 = go.Scatter3d(x = Xn,
                    y = Yn,
                    z = Zn,
                    mode='markers',
                    marker=dict(symbol='circle',
                             size=6,
                             colorscale='Viridis',
                             line=dict(color='rgb(50,50,50)', width=0.5)
                             ),
                    text=labels,
                    hoverinfo='text')
	
	trace2 = go.Scatter3d(x = Xe,
                    y = Ye,
                    z = Ze,
                    mode='lines',
               	    line=dict(color='rgb(1,1,1)', width=1),
                    hoverinfo='none')	
	
	axis=dict(showbackground=False,
          	showline=False,
          	zeroline=False,
          	showgrid=False,
          	showticklabels=False,
          	title=''
        )

	layout = go.Layout(
		 title="Network",
		 width=1000,
		 height=1000,
		 showlegend=False,
		 scene=dict(
		     xaxis=dict(axis),
		     yaxis=dict(axis),
		     zaxis=dict(axis),
		 ),
		 margin=dict(
		 t=100
	         ),
	    	hovermode='closest',
	    	annotations=[
		   dict(
		   showarrow=False,
		    xref='paper',
		    yref='paper',
		    x=0,
		    y=0.1,
		    xanchor='left',
		    yanchor='bottom',
		    font=dict(
		    size=14
		    )
		    )
		],)

	data=[trace1, trace2]
	fig=go.Figure(data=data, layout=layout)

	offline.plot(fig)




def DataProcessing(V, data):
	hs = {V[i]: i for i, _ in enumerate(V)}
	for item in data:
		item.user_id = hs[item.user_id]
		item.links = [hs[link] for link in item.links]
	return data


def makeNode(user_id, json, V):
	return Node(user_id=user_id, links=[item['id'] for item in  json['response']['items'] if item['id'] in V])


def main():
	user_id = input()
	r1 = requests.get('https://api.vk.com/method/users.get?user_id={}&v={}&access_token={}'.format(user_id, v, access_token))
	username = r1.json()['response'][0]['first_name'] + ' ' +  r1.json()['response'][0]['last_name']
	query = 'friends.get?user_id={}&v={}&access_token={}&fields=city'
	r = requests.get(api_url + query.format(user_id, v, access_token))
	V = [user_id] + [item['id'] for item in r.json()['response']['items']]
	labels =[username] + [item['first_name'] + item['last_name'] for item in r.json()['response']['items']]	
	root =  makeNode(user_id=user_id, json=r.json(), V=V)
	count = r.json()['response']['count']
	print('root user{} has been considered, number of friends:{}'.format(user_id, count)) 
	data = [root]
	ctr = 0
	for user_id in root.links:
		r = requests.get(api_url + query.format(user_id, v, access_token))
		if 'error' not in r.json():
			data.append(makeNode(user_id=user_id, json=r.json(), V=V))
		ctr += 1
		print('user{} has been cosidered, counter{}'.format(user_id, ctr)) 
	data = DataProcessing(V, data)
	GraphPlot(data, labels)


if __name__=='__main__':
	main()


