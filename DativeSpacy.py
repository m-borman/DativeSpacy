"""
THIS SCRIPT INTENDS TO SEARCH CORPUS DOCUMENTS FOR PREPOSITIONAL DATIVE VERBS
USING POS AND CERTAIN WORDS.

"""

########################################
# This script is intended to extract the contexts of target words from text files
# From its working directory, a few folders are used to hold text files that:
#	provide the target words (cwd/InputLemmas)
#	provide the corpora which will be analyzed (cwd/WLP_Corpus Files and cwd/WLP_TestFiles)
#	provide a destination for the contexts in which the target words appeared in the corpora
#		(cwd/OutputWords)
#	
# 
#
#####################
### Start program ###
#####################
### Import packages



"""
NEEDS:
-classes for each word in a sent
-output file
	-each entry should have the word and its POS in ()

Steps-
	read files
	look for verbs
	capture next 6 words/POS
	feed that into one class for each word?
	go through conditions of each instance of the class
	if conditions met, append that "sentence" to the output file

"""



import re
import sys
import os
import glob
import time

### Initialization of corpora
cwd = os.getcwd()
CORPORA_FILES = cwd + "/WLP_CorpusFiles"
TEST_FILES = cwd + "/WLP_TestFiles"
WORKING_FILES=CORPORA_FILES

window=5 #sets window - eg window=5 would grab the 5 words before and after target word



GEN_WORDS = False

### Structure of corpus documents
LEN_LINE = 5
WORD_INDEX = 2
LEMMA_INDEX = 3
POS_INDEX = 4
SPECIAL_POS_INDEX = 3
SPECIAL_WORD_INDEX = 2
SEP_CHAR = "\t"

WLP_WORD_INDEX = 0
WLP_LEMMA_INDEX = 1
WLP_POS_INDEX = 2

### Need to skip certain characters due to nature of raw text
SKIP_CHARS = ["@", ",", "(", ")", "-", "--", ":", "'s", "\"", "\'", "/", "<p>", "<", ">", "#"]
### ### We do not want to skip ".", ";", or "?" characters as those indicate the ends
### ### of sentences.
PREP_TAGS = ["if", "ii", "io", "iw"]
NOUN_TAGS = ["nn1", "nn", "nn2", "nna", "nnb", "nnl1", "nnl2", "nno", "nno2", "nnt1", "nnt2", "nnu", "nnu1", "nnu2", "np", "np1", "np2", "npd1", "npd2", "npm1", "npm2", "pn", "pn1", "pnqo", "pnqs", "pnqv", "pnx1", "ppge", "pph1", "ppho1", "ppho2", "pphs1", "pphs2", "ppio1", "ppio2", "ppis1", "ppis2"]
DET_TAGS = ["at", "at1", "da", "da1", "da2", "dar", "dat", "db", "db2", "dd", "dd1", "dd2", "ddq", "ddqge", "appge"]
VERB_TAGS = ["vv0", "vvd", "vvg", "vvn", "vvz", "vd0", "vdd", "vdg", "vmk", "vvi"]
ADJ_TAGS = ["jj", "jjr", "jjt", "jk"]  ##### REVIEW THESE!!!!!!!!!!

TARGET_INDEX=LEMMA_INDEX


TAG_LIST=["PREP_TAGS", "NOUN_TAGS",]




### Custom file opening function
def openFile(filename, characteristic, new = False):
	count = 0
	filenameTemp = filename
	if (new == True):
		filetype = filename[-4:]
		filename = filename[:-4]
		while os.path.exists(filenameTemp):
			filenameTemp = filename + "_" + str(count) + filetype
			count += 1
	returnedFile = open(filenameTemp, characteristic)
	return returnedFile

# def createEmoFiles(emoWordList):
# 	currDir = os.getcwd()
# 	if not os.path.exists(currDir + "/OutputWords"):
# 		os.makedirs(currDir + "/OutputWords")
# 	for word in emoWordList:
# 		outputFile = open(currDir+"/OutputWords/"+word+'.txt', 'a')
# 		corpusFiles=os.listdir(WORKING_FILES)
# 		corpusFiles=str(corpusFiles)+'\n'
# 		outputFile.write(corpusFiles)
# 		outputFile.close()
LegalSyntaxList=[]
### Need to create files for each word. The following function creates a txt file for each word in wordList
### and then saves the path to that txt file in the array for the target noun.
def getLegalSyntax(LegalSyntaxFile):
	with open(LegalSyntaxFile,'rb') as inFile:
		for line in inFile:
			LegalSyntaxList.append(line.rstrip('\r\n'))
	# print "emoOutList="+str(emoOutList)
	print "LEGAL="+str(LegalSyntaxList)

# def getEmoWords(emoWordList):
# 	emoOutList=[]
# 	with open(emoWordList,'rb') as inFile:
# 		for line in inFile:
# 			emoOutList.append(line.rstrip('\r\n'))
# 	# print "emoOutList="+str(emoOutList)
# 	return emoOutList

### Begin analysis of corpora
def generateDocuments(corpora, LegalSyntaxList): #used to have emoWordList too
	
	startTime=time.time()
	for corpus_file in glob.glob(corpora + '/*.txt'): 
		doc = [[]]
		docDict = {}
		filename=corpus_file.split("Files")[-1]
		with open(corpus_file) as corpus:  # Open each corpus
			doc[0] = re.split(r'\t+', corpus.readline().strip().lower()) # Read in first line of document; make sure inputs are sanitized
			for lineIndex,nextLine in enumerate(corpus):			 
				nextLine = re.split(r'\t+', nextLine.strip().lower())
				nextLine.append(filename)
				nextLine.append(lineIndex)
				docDict[lineIndex]=nextLine

				doc.append(nextLine)
			endTime=time.time()
			loadTime=str(endTime-startTime)
			print str(filename)+" loaded in "+loadTime+" seconds"
			searchTgt(doc, docDict, LegalSyntaxList, SKIP_CHARS)


def searchTgt(doc, docDict, LegalSyntaxList, SKIP_CHARS):
# 	###Each word in the corpus is read in as a dictionary pair with an index (#) as its key.  
# 	###This function scans a corpus doc and when it finds a word that's also in the word list,
# 	### it searches for the surrounding words by their indices relative to the matching word.
# 	### The function also excludes any results that are in the SKIP_CHARS list defined above
	startTime=time.time()
	wlpLen=5
	regLen=7
	context = []
	sentLen=8
	maxIndex= max(k for k, v in docDict.iteritems() if v != 0)
	# for curLine in doc:
	# 	WordColIndex=0
	# 	curWord=curLine[WordColIndex]
	# 	print curPOS
	outputFile=open("C:\Users\mzbor\Desktop\COCA\Scripts\Scripts\DativeSearch\Output/"+doc[2][-2], "a")  ####NEED TO REMANE THIS UNIQUE TO THE SPECIFIC FILE
	matches=[]
	for curLine in doc:
		curContext=[]
		if len(curLine)>wlpLen:
			wordColIndex=2
			lemmaColIndex=3
			POSColIndex=4
		else:
			wordColIndex=0
			lemmaColIndex=1
			POSColIndex=2			
		if len(curLine)>3 and type(curLine[-1]) == int and (curLine[-1]-maxIndex)<-5:  # MAY NEED TO ADD A CLAUSE HERE TO EXCLUSE FIRST 20 or so lines of file...

			curPOS=curLine[POSColIndex]
			output=[]
			curWord=curLine[wordColIndex]
			if curPOS in VERB_TAGS:
				# print str(curWord)+" POS:"+str(curPOS)
				tgtIndex=curLine[-1]
				sentIndices=[tgtIndex+num for num in range(0,sentLen)]  # Creates a list of the indices for the 5 words following the verb
				
				# wordsList=[docDict[item][wordColIndex], docDict[item][POSColIndex] for item in sentIndices}]
				# print wordsList

				for item in sentIndices:
					word_POS=[]
					word_POS.extend((docDict[item][wordColIndex], docDict[item][POSColIndex]))

					# curContext.append(word_POS)
					if docDict[item][POSColIndex] in VERB_TAGS:
						word_POS.extend('V')

					elif docDict[item][POSColIndex] in NOUN_TAGS:
						word_POS.extend('N')
					elif docDict[item][POSColIndex] in DET_TAGS:
						word_POS.extend('D')
					elif docDict[item][POSColIndex] in ADJ_TAGS:
						word_POS.extend('J')
					elif docDict[item][POSColIndex] in PREP_TAGS:
						word_POS.extend('P')
					else:
						word_POS.extend('X')
						break   ### IF POS not in one of the above bins, THIS ENDS THE LOGGING OF POS 
					# if word_POS.count('N') ==2:



					curContext.append(word_POS)
				
				testIndices=[i for i in range(1,9)]
				

				# print curContext
				# 	curContext.append(str(docDict[item][wordColIndex])+"/"+str(docDict[item][POSColIndex])
				sentDict=dict(zip(testIndices, curContext)) #
				# sentSyntax=[i for i in sentDict[i][2]]
				sentSyntax=[]

				for i in range (1,len(sentDict)+1):  #Gives the items in the syntax a number in order and adds it to its dictionary entry
					sentSyntax.extend(sentDict[i][2])
				# if sentSyntax[1]=="P":
				# 	break
				# for item in sentSyntax:
				# 	", ".join(map(item, sentSyntax))
				sentSyntax=",".join(sentSyntax)
				
				# print type(sentSyntax)
				# print type(sentSyntax[0])
				# sentSyntax.strip(["'"])					
				# print sentSyntax
				# print sentDict
				if any(item in sentSyntax for item in LegalSyntaxList):
					
					if sentSyntax[1]!="P":
						wordPOSlist=[]
						for item in curContext:
							for x, word in enumerate(item):
								
							
								if x==1:
									
									tempPOS=word
									tempPOS="("+word+")"
									wordPOSlist.append(tempPOS)
								if x==0:
									wordPOSlist.append(word)

						wordPOSlist=" ".join(wordPOSlist)
						wordPOSlist=wordPOSlist.replace(" (", "(")
						strippedSyntax=sentSyntax.replace(",","")

						matches.append(sentSyntax)
						output=strippedSyntax+","+wordPOSlist+'\n'
						outputFile.write(str(output))

					# print curContext
					# print sentSyntax[2:]

	timeEndFile=time.time()
	timeElapsed=str(timeEndFile-startTime)			
	print "Analyzed in:"+timeElapsed+" seconds"
				#need to find out if the the result contains any items in my list
				# if sentSyntax contains 2 N, 
				# ### JUST NOUNS!
				# #NN
				# if sentDict[2][1] in NOUN_TAGS and sentDict[3][1] in NOUN_TAGS:

				# #JNN
				# if sentDict[2][1] in ADJ_TAGS and sentDict[3][1] in NOUN_TAGS and sentDict[4][1] in NOUN_TAGS:

				# #NJN
				# if sentDict[2][1] in NOUN_TAGS and sentDict[3][1] in ADJ_TAGS and sentDict[4][1] in NOUN_TAGS:

				# #DNN
				# if sentDict[2][1] in DET_TAGS and sentDict[3][1] in NOUN_TAGS and sentDict[4][1] in NOUN_TAGS:

				# #NDN
				# if sentDict[2][1] in NOUN_TAGS and sentDict[3][1] in DET_TAGS and sentDict[4][1] in NOUN_TAGS:

				# #NPN
				# if sentDict[2][1] in NOUN_TAGS and sentDict[3][1] in PREP_TAGS and sentDict[4][1] in NOUN_TAGS:


				# #JNJN					
				# if sentDict[2][1] in ADJ_TAGS and sentDict[3][1] in NOUN_TAGS and sentDict[4][1] in ADJ_TAGS and sentDict[5][1] in NOUN_TAGS:
				# 	print "DO SUCCESS"
				# 	sentDict.append
				# #DNJN
				# if sentDict[2][1] in DET_TAGS and sentDict[3][1] in NOUN_TAGS and sentDict[4][1] in ADJ_TAGS and sentDict[5][1] in NOUN_TAGS:

				# #DNDN
				# if sentDict[2][1] in DET_TAGS and sentDict[3][1] in NOUN_TAGS and sentDict[4][1] in DET_TAGS and sentDict[5][1] in NOUN_TAGS

				# #JNDN
				# if sentDict[2][1] in ADJ_TAGS and sentDict[3][1] in NOUN_TAGS and sentDict[4][1] in DET_TAGS and sentDict[5][1] in NOUN_TAGS

				# #DJNN
				# if sentDict[2][1] in DET_TAGS and sentDict[3][1] in ADJ_TAGS and sentDict[4][1] in NOUN_TAGS and sentDict[5][1] in NOUN_TAGS


				# #NDJN
				# if sentDict[2][1] in NOUN_TAGS and sentDict[3][1] in DET_TAGS and sentDict[4][1] in ADJ_TAGS and sentDict[5][1] in NOUN_TAGS

				# if sentDict

				# print sentDict[2][1]
				# if sentDict[2][1] in DET_TAGS:
				# 	print "DO"
				# 	output.append(sentDict)
				# 	print output

###COMMENTED 5:22

				# contextDict=
				# for item, i in enumerate(curContext):
				# 	item
				# for item in curContext:


					


# 			if curWord in emoWordList:
# 				curWordFile=open("C:\Users\mzbor\Desktop\COCA\Scripts\Scripts\OutputWords/"+curWord+".txt", "a")

# 				tgtIndex=curLine[-1] #this is the index of the current word within the corpus file, assigned when the corpus file was imported


# 				bumpFor=0
# 				bumpBack=0
# 				contextIndices=[tgtIndex+num for num in range(((-window) -bumpBack) ,window+1+bumpFor)]
# 				skipIndices=[]
# 				contextCounter=0
# 				okIndices=[]

# 				for contextIndex in contextIndices:
# 					###Make a new function that recalculates the context indices?
# 					if contextIndex not in skipIndices:

# 						contextWord=docDict[contextIndex][wordColIndex]
# 						if contextWord not in SKIP_CHARS:
# 							okIndices.append(contextIndex)

# 						else:
# 							if contextIndex-tgtIndex<0:
# 								bumpBack+=1
# 								skipIndices.append(contextIndex)
# 								addedIndex=tgtIndex-window-bumpBack
# 								contextIndices.append(addedIndex)
# 							if contextIndex-tgtIndex>0:
# 								bumpFor+=1
# 								skipIndices.append(contextIndex)
# 								contextIndices.append(tgtIndex+window+bumpFor)
# 				okLabels=[]
# 				for item in okIndices:
# 					okLabels.append(docDict[item][-1])
				
# 				okIndices.sort()
# 				contextWords=[]
# 				for item in okIndices:
# 					contextWords.append(docDict[item][wordColIndex])
# 				contextWords=' '.join(contextWords)
# 				contextWords=contextWords+'\n'
# 				if len(curLine)<6:
# 					tgtLabel='none'
# 				else:
# 					tgtLabel=docDict[tgtIndex][1]
# 				tgtWord=docDict[tgtIndex][wordColIndex]
# 				corpFile=docDict[tgtIndex][-2]
# 				output=corpFile+', '+tgtLabel+', '+tgtWord+', '+contextWords
# 				curWordFile.write(output)

	# print "doc done"	


# Run the program
def main():
	if (GEN_WORDS == False):
		LegalSyntaxFile = getLegalSyntax(cwd+"/LegalSyntax/LegalSyntax.txt")

		# emoWordList = getEmoWords(cwd+"/InputLemmas/testWordList.txt")
		# createEmoFiles(emoWordList)
		generateDocuments(WORKING_FILES,LegalSyntaxList)  #Change CORPORA_FILES to another directory to analyze other files

main()
sys.exit()
