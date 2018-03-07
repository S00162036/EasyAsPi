import csv
def WriteToCSV(weightIn, heightIn, coinIn) :
	with open('LocalCoinData.csv', 'a') as csvfile:
	    writer = csv.writer(csvfile)
	    writer.writerow([{"Weight":weightIn,"Height":heightIn,"CoinValue":coinIn}])