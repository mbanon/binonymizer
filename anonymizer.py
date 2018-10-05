#!/usr/bin/env python


#anonymizer.py: Entry point.
#Wraps the anonymizer-core.py, preparing the input and processing the output. 
#Takes the entry file (raw src-trg, tmx...), parallelizing if needed,
#and extracting the source and the target sentences,
#generating (in the case of tmx files) a raw parallel corpus,
#that will be input to the anonymizer-core.
#hen the anonymizer-core.py finishes, builds the annotated TMXs (if the entry was a TMX file)



#We need to decide if we paralelize at lines/tus scope (in case of few files with a lot of lines)
#or at document scope (in case of a lot of files with few lines) 