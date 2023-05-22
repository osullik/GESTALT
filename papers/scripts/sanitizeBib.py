# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Author Kent O'Sullivan | github.com/osullik
# TO USE: 																						#
#	Environment: 																				#
#		Python 3 																				#
#		requires the bibtexparser package														#
#	Command line args: 																			#
#		-b, --bibFile = the fileName of the bib file you want to sanitize 						#
#		-f, --fields  = the fields you want sanitized (defaults: comment, file and groups)		#
#		example: sanitizeBib.py -b test.bib -f file comment groups 								#
#	Outputs: 																					#
#		Overwrites the input file 																#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # #
# Prelims                     #
# # # # # # # # # # # # # # # #

import argparse

try:
	import bibtexparser
	from bibtexparser.bwriter import BibTexWriter
except ModuleNotFoundError:
	print("Looks like you need to install bibtexparser friend, try:")
	print("pip install bibtexparser")
	exit()

# # # # # # # # # # # # # # # #
# Functions                   #
# # # # # # # # # # # # # # # #

def sanitize(bibFile, dirtyFields):
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	# sanitize removes the contents of designated dirty fields from a given bib file 				#
	# Input args: 																					#
	#	bibFile 		- string 	- the file name (fully qualified path if not in same directory) #
	#	dirtyFields		- list		- the list of fields to Output									#
	# Output: 																						#
	#	bib_database	- bibDatabase - the sanitized database 										#
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

	deletionRecord = {}														# Used to count the number of records modified
	
	print("Looking for file:", bibFile)

	try:
		with open(bibFile) as dirtyFile:										# Load in the file to be sanitized
			bib_database = bibtexparser.load(dirtyFile)							# as a bibtex database object
	except FileNotFoundError:
		print(bibFile,"not found, check the path and try again")
		exit()

	print("Sanitizing bib file:", bibFile)

	print("Number of entries in the bib file:", len(bib_database.entries))	


	for entry in bib_database.entries:										# step through all database entries

		for field in dirtyFields:											# Check if the entry has a dirty field

			if field in entry.keys() and entry[field] != '': 								

				entry[field] = ""											# Delete the content of the field (but leave the key so you can see what was deleted)

				if field in deletionRecord.keys(): 							# Update the counts of deletions
					deletionRecord[field] += 1
				else:
					deletionRecord[field] = 1

			else: 
				pass

	if len(deletionRecord.keys()) == 0:										# Handle situation where nothing found
		print("Nothing found to sanitize")
	else:

		print("Sanitized:")														

		for key in deletionRecord.keys():									# Step through each field to be deleted and give the count
			print(key, deletionRecord[key])

	return bib_database														# return the sanitized database


# # # # # # # # # # # # # # # #
# Main                        #
# # # # # # # # # # # # # # # #

if __name__ =='__main__':

	argparser = argparse.ArgumentParser()									# initialize the argParser

	argparser.add_argument(	"-b", "--bibFile", 								# command line triggers for the bibFile
							help="The .bib file you want sanitized",		
							type=str, 
							required=True)									# user MUST input
	
	argparser.add_argument(	"-f", "--fields", 								# command line triggers for fields to input
							nargs="+", 										# accept 1 or more args
							help="The fields you want sanitized",			
							default=["groups", "comment", "file"])			# If no input provided, just clear three default
	
	flags = argparser.parse_args()											# populate variables from command line arguments
	bibFile = flags.bibFile												
	dirtyFields = flags.fields

	cleanBibDB = sanitize(bibFile, dirtyFields) 							# sanitize the database

	writer = BibTexWriter()													# Used to 

	with open(bibFile, 'w') as cleanFile:									# Over-write the source file
	    cleanFile.write(writer.write(cleanBibDB))