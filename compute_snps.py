import pandas as pd
import numpy as np
import json

def pathogenic_snps(varaint_file):
	"""Takes json file as input, filters the missense snps and stores its information in json format"""
	resid = []
	xrefs = []
	clinicalSignificances = []
	genomicLocation = []
	alternativeSequence = []
	for each_line in varaint_file:
		try:
			try:
				sig_list = each_line['clinicalSignificances'].split(',')
			except AttributeError:
				sig_list = each_line['clinicalSignificances'][0]['type']

			if ('Pathogenic' in sig_list) or ('Disease' in sig_list) or ('pathogenic' in sig_list) or ('disease' in sig_list):
				#print (sig_list)
				resid.append(each_line['begin'])
				xrefs.append(each_line['xrefs'][0])
				genomicLocation.append(each_line['genomicLocation'])
				alternativeSequence.append(each_line['alternativeSequence'])
		except KeyError:
			pass
	df = pd.DataFrame(list(zip(resid, xrefs, genomicLocation, alternativeSequence)), 
               columns =['resid', 'xrefs', 'genomicLocation', 'alternativeSequence']) 
	chart_data = df.to_dict(orient="records")
	return json.dumps(chart_data, indent=2)





