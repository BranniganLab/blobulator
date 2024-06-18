import pandas as pd
import numpy as np
import json

def pathogenic_snps(variant_file):
	"""Takes json file as input, filters the missense snps and stores its information in json format"""
	resid = []
	xrefs = []
	clinicalSignificances = []
	genomicLocation = []
	alternativeSequence = []
	for each_line in variant_file:
		try:
			try:
				sig_list = each_line['clinicalSignificances'].split(',')
			except AttributeError:
				sig_list = each_line['clinicalSignificances'][0]['type']

			if ('Pathogenic' in sig_list) or ('Disease' in sig_list) or ('pathogenic' in sig_list) or ('disease' in sig_list):
				for item in each_line['xrefs']:
					if item['name'] == 'dbSNP' and each_line['begin'] not in resid and each_line['alternativeSequence'] != "*" and each_line['alternativeSequence'] != "=" and len(each_line['alternativeSequence']) == 1 and len(each_line['genomicLocation']) > 0:
						xrefs.append(item)
						resid.append(each_line['begin'])
						genomicLocation.append(each_line['genomicLocation'])
						alternativeSequence.append(each_line['alternativeSequence'])

		except KeyError:
			pass
	df = pd.DataFrame(list(zip(resid, xrefs, genomicLocation, alternativeSequence)), 
               columns =['resid', 'xrefs', 'genomicLocation', 'alternativeSequence']) 
	chart_data = df.to_dict(orient="records")
	return json.dumps(chart_data, indent=2)