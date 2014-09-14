import json
import codecs
from datetime import datetime
from pprint import pprint

with open('investevent.json') as data:
	sql = file('investevent.sql', 'w');
	index = 0
	while True:

		line = data.readline()
		if len(line) == 0:
			break
		INSERT_TEMPLATE = 'INSERT INTO investevent(`id`'
		index = index + 1

		# if index == 5000:
		# 	break

		line = json.loads(line, "utf-8")
		values = []

		for key in line.keys():

			value = line[key]

			if type(value) is list:
				value = ','.join(value)

			if key in ['date']:
				raw_date_string = value.split(' ')[0] + '/01'
				try:
					value = datetime.strptime(raw_date_string, '%Y/%m/%d').strftime('%Y-%m-%d')
				except ValueError:
					value = 'NULL'

			if key in ['phase']:
				value = (value.split(' ')[1])[2:]

			if key in ['url']:
				value = 'http://chuangyepu.com' + value

			if key not in ['images']:
				values.append(value)
				INSERT_TEMPLATE += ', `' + key + '`'

		INSERT_TEMPLATE += ') values(' + `index`

		for value in values:
			INSERT_TEMPLATE += ', "' + value.strip() + '"'
		INSERT_TEMPLATE += ');\n'
		sql.write(INSERT_TEMPLATE.encode('utf-8'))

	sql.close()
	data.close()