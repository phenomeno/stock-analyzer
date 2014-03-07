#what is this for again?
#!/usr/bin/env python

#returns pearson coefficient and 2-tailed p value
# p coefficient measures how correlated from -1, 1.
#0 is no correlation, -1 is negatively correlated, 1 is positively correlated
#2-tailed p value gives probability of not correlated (0 to 1)
from scipy.stats import pearsonr
#cross correlation: takes product of two random variables and then the integral of it
#when peaks or dips align they create peaks in the cross correlation
from scipy.signal import correlate
from numpy import linspace, sin, cos, pi, array
import csv
import dateutil
from datetime import datetime

# a is a set of data
# 0-1 normalization, or feature scaling, or data normalization
# brings the distance between data to an approximately proportionate range
def normalize(a):
	b = []
	for x in a:
		b.append((x-min(a)) / (max(a)-min(a)))
	return b
	
def totimestamp(t):
	epoch = datetime(1970, 1, 1)
	#this gives a range of dates
	diff = t-epoch
	#how many days in between t and 1970* hours* seconds + extra seconds
	#aka how much time has passed in seconds from 1970
	return diff.days * 24 * 3600 + diff.seconds
	
def load_stock(name):
	data = []
	#way to open a file, process contents, and close it
	#sample use
	"""
	with open("x.txt") as f:
    data = f.read()
    do something with data
    """
    # %s is the string formatter !!
	with open('./stocks/%s.csv' % (name)) as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			# need to convert date types to python date type
			t = dateutil.parser.parse(row[0])
			# add to the data [] with how much time has passed in seconds from 1970
			# and the stock price as a float
			# i guess the info comes in rows???
			data.append([ totimestamp(t), float(row[1]) ])
	return data
	
def load_commodity(name):
	data = []
	with open('./commodities/%s.csv' % (name)) as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			t = dateutil.parser.parse(row[0])
			data.append([ totimestamp(t), float(row[1]) ])
	return data



aapl = load_stock('AAPL')
# grabs all of the the timedata into one list
# grabs the lowest value so the oldest date
start_t = min(map(lambda x: x[0], aapl))

bac = load_stock('BAC')
# throws out dates that are earlier than 1970
bac = filter(lambda x: x[0] >= start_t, bac)

xom = load_stock('XOM')
xom = filter(lambda x: [0] >= start_t, xom)

sd = load_stock('SD')
sd = filter(lambda x: x[0] >= start_t, sd)

rdsa = load_stock('RDS-A')
rdsa = filter(lambda x: x[0] >= start_t, rdsa)

oil = load_commodity('OIL')
oil = filter(lambda x: x[0] >= start_t, oil)

figure()
title('Graph of the relationship between stocks and commodities')

plot(map(lambda x: x[0], aapl), map(lambda x: x[1], aapl), '--m', label = 'AAPL')
plot(map(lambda x: x[0], bac), map(lambda x: x[1], bac), '--k', label = 'BAC')
plot(map(lambda x: x[0], xom), map(lambda x: x[1], xom), '--g', label = 'XOM')
plot(map(lambda x: x[0], sd), map(lambda x: x[1], sd), '--b', label = 'SD')
plot(map(lambda x: x[0], rdsa), map(lambda x: x[1], rdsa), '--c', label = 'RDS/A')
plot(map(lambda x: x[0], oil), map(lambda x: x[1], oil), '--r', label = 'OIL')
legend(loc='upper right')

locs, _ = yticks()