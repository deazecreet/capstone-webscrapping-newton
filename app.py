from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
get_url = requests.get('https://www.coingecko.com/en/coins/ethereum/historical_data?start_date=2022-01-01&end_date=2023-03-29#panel')
soup = BeautifulSoup(get_url.content,"html.parser")

#Scrapping
list_tanggal = []
row_length = len(table.find_all('th', attrs={'scope':'row', 'class':'font-semibold text-center'}))

for i in range(0, row_length):
    tanggal = table.find_all('th', attrs={'scope':'row', 'class':'font-semibold text-center'})[i].text
    list_tanggal.append(tanggal)
    
increment = 1
list_volume = []
while len(list_volume) != 60:
    volume = table.find_all('td', attrs={'class':'text-center'})[increment].text.strip()
    list_volume.append(volume)
    increment += 4

#change into dataframe
df = pd.DataFrame({"Date":list_tanggal, "Volume ($)":list_volume})

#insert data wrangling here
df["Date"] = pd.to_datetime(df["Date"])
df["Volume ($)"] = df["Volume ($)"].str.replace("$", "")
df["Volume ($)"] = df["Volume ($)"].str.replace(",", "")
df["Volume ($)"] = df["Volume ($)"].astype('int64')

df = df.sort_values("Date")
df.reset_index(drop=True, inplace=True)

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df["Volume ($)"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	sns.set(rc={'figure.figsize':(20,9)})
	sns.lineplot(data=df, x="Date", y="Volume ($)")
	plt.xticks(fontsize=15)
	plt.show()
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)