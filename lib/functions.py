import requests
from bs4 import BeautifulSoup
import pandas as pd

class FoozBall():

	def __init__(self):
		pass


	def data_info():
		print(
		'''
			Columns
			_______
			Yr   - Year
			Lg   - League
			Tm   - Team
			W    - Wins
			L    - Losses
			T    - Ties
			DF   - Division Finish
			PO   - Playoffs
			PF   - Points For
			PA   - Points Against
			PD   - Point Differential
			HDC  - Head Coach
			AV   - Approximate Value / Most valuable Player
			PAS  - Top Passer
			RSH  - Top Rusher
			REC  - Top Receiver
			OPR  - Offensive Point Ranking
			OYR  - Offensive Yard Ranking
			DPR  - Deffensive Point Ranking
			DYR  - Deffensive Yard Ranking
			T/G  - Takeaway / Giveaway ratio ranking
			PDR  - Point Differential Ranking
			YDR  - Yard Differential Ranking
			TT   - Total Teams
			MoV  - Margin of Victory
			SoS  - Strength of Schedule
			SRS  - Simple Rating System
			OSRS - Offensive quality relative to average (SRS)
			DSRS - Defensive quality relative to average (SRS)

			Simple Rating System
			____________________
			SRS = MoV + SoS = OSRS + DSRS
		'''
			)


	def get_data(self, url):
		'''
		Requests data from a website using requests.
		Html data is parsed using BeautifulSoup.
		Returns data as a pandas data frame.
		'''

		r = requests.get(url)
		content = r.content
		r.close()

		soup = BeautifulSoup(content, 'lxml')
		table_soup = soup.findAll('tr')
		cols = [th.get_text() for th in table_soup[1].findAll('th')]

		year = []
		data = []

		# extracting data from html table
		for i in range(2,len(table_soup)):
			y = [th.get_text() for th in table_soup[i].findAll('th')]
			d = [td.get_text() for td in table_soup[i].findAll('td')]
			year.append(y)
			data.append(d)

		year = pd.Series(year, name='year')
		data = pd.DataFrame(data, columns = cols[1:])
		self.raw_data = pd.concat((year, data), axis=1)

		return self.raw_data

	def column_clean(self):
		'''
		Condensing two header columns into one.
		'''

		columns = [
		'Yr', 'Lg', 'Tm', 'W', 'L', 'T', 'DF', 'PO', 'PF',\
		'PA','PD','HDC', 'AV', 'PAS', 'RSH', 'REC', 'OPR', 'OYR',\
		'DPR', 'DYR', 'T/G', 'PDR', 'YDR', 'TT', 'MoV', 'SoS',\
		'SRS', 'OSRS', 'DSRS'
		]

		self.raw_data.columns = columns

		print('Columns have been cleaned.')


	def clean(self, num_only=False):


		# Table data on the webpage has breaks
		# Using a mask to find the null values that are the table break
		break_mask = self.raw_data['Tm'].isnull()
		breaks = self.raw_data[break_mask].index
		break_rows = [row for row in breaks]
		data = self.raw_data.drop(break_rows,axis=0)

		# Removing the year values from the nested list

		data['Yr'] = data['Yr'].apply(lambda x: int(x[0]))

		return data
