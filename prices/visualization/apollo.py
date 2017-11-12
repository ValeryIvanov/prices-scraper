import pprint
from pymongo import MongoClient
from plotly.offline import plot
import plotly.figure_factory as ff


client = MongoClient('mongodb://192.168.99.100:32777/')
db = client['scrapy-mongodb']
collection = db['apollo_copy']
prices = []
for product in collection.find():
    prices.append(product['price'])

fig = ff.create_distplot(hist_data=[prices], group_labels=['distplot'])
plot(fig, filename='Basic Distplot')
