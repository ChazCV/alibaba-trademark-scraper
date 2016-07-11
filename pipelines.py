import csv


class AliCsvWriter(object):

    def __init__(self):
		"""Create a CSV file to store the scraped data."""
		
        outfile = 'alibaba_results.csv'
		self.csvwriter = csv.writer(open(outfile, 'a'), lineterminator = '\n')
       
    def process_item(self, item, baba):
		"""Format the rows of data to be written to the CSV file."""
		
        row = [item['brand'], "00", item['hits'][0], item['in_title'],
			   item['rel_cat_1'], item['rel_hits_1'][0],
			   item['rel_in_title_1'], item['rel_cat_2'],
			   item['rel_hits_2'][0], item['rel_in_title_2']]			   
        self.csvwriter.writerow(row)
        return row