# modified from http://stackoverflow.com/a/26781642/1492614

from __future__ import absolute_import
from __future__ import division

def humanize_time(amount, units = 'seconds'):    

	def process_time(amount, units):

		INTERVALS = [   1, 60, 
						60*60, 
						60*60*24, 
						60*60*24*7, 
						60*60*24*7*4, 
						60*60*24*7*4*12, 
						60*60*24*7*4*12*100,
						60*60*24*7*4*12*100*10]
		NAMES = [('second', 'seconds'),
				 ('minute', 'minutes'),
				 ('hour', 'hours'),
				 ('day', 'days'),
				 ('week', 'weeks'),
				 ('month', 'months'),
				 ('year', 'years'),
				 ('century', 'centuries'),
				 ('millennium', 'millennia')]

		result = []

		unit = list(map(lambda a: a[1], NAMES)).index(units)
		# Convert to seconds
		amount = amount * INTERVALS[unit]

		for i in range(len(NAMES)-1, -1, -1):
			a = amount // INTERVALS[i]
			if a > 0: 
				result.append( (a, NAMES[i][1 % a]) )
				amount -= a * INTERVALS[i]

		return result

	rd = process_time(int(amount), units)
	cont = 0
	for u in rd:
		if u[0] > 0:
			cont += 1

	buf = ''
	i = 0
	for u in rd:
		if u[0] > 0:
			buf += "%d%s" % (u[0], u[1][0])
			cont -= 1
		i += 1

	return buf
