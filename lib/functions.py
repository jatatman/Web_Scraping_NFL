import requests
from bs4 import BeautifulSoup
import pandas as pd

class FoozBall():

	def __init__(self):
		pass


	def data_info():
		print('''
			Columns
			_______
			Year
			W
			L
			T
			PF
			PA
			PD
			Pts
			Yds

			''')


	def get_data(self, url):

		r = requests.get(url)
		content = r.content
		r.close()

		soup = BeautifulSoup(content, 'lxml')
		table_soup = soup.findAll('tr')
		cols = [th.get_text() for th in table_soup[1].findAll('th')]

		year = []
		data = []

		for i in range(2,len(table_soup)):
			y = [th.get_text() for th in table_soup[i].findAll('th')]
			d = [td.get_text() for td in table_soup[i].findAll('td')]
			year.append(y)
			data.append(d)

		year = pd.Series(year, name='year')
		data = pd.DataFrame(data, columns =cols[1:])
		self.raw_data = pd.concat((year, data), axis=1)

		return self

	def clean(self, num_only=False):

		# Table data on the webpage has breaks
		# Using a mask to find the null values that are the table break
		break_mask = self.raw_data['Tm'].isnull()
		breaks = self.raw_data[break_mask].index
		break_rows = [row for row in breaks]
		data = self.raw_data.drop(break_rows,axis=0)

		columns = ['Year', 'League', 'Team', 'Div_Finish', 'Playoffs', 'Points_For', 'Points_Against', 'Point_Difference',
		'Coaches', 'MVP', 'Passer', 'Rusher', "Reciever', "]



		# Removing the year values from the nested list
		
		data['year'] = data['year'].apply(lambda x: int(x[0]))

		str_cols = ['Lg', 'Tm', 'Div. Finish', \
					'Playoffs', 'Coaches', 'AV', \
					'Passer', 'Rusher', 'Receiver'
					]
		num_cols = [col for col in data.columns if col not in str_cols]


		str_df = data[str_cols]
		num_df = data[num_cols]
		num_df = num_df.applymap(lambda x: float(x))

		if num_only:
			return num_df
		else:
			return pd.concat((num_df,str_df))



