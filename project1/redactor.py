# to run: pipenv run python redactor.py --input '*.txt' \ --names --dates --phones \ --concept 'kids' \ --output 'files/' \ --stats stderr

import argparse # dunder thing
import re # readData()
import glob
import spacy
#import nltk

projURL = "https://github.com/yut4916/cs5293sp21-project1.git"

nlp = spacy.load("en_core_web_sm")

def main(docList):
    print("Initiating Project 1...")
    print("Redacting the following documents:\n", docList)

    args = parser.parse_args()
    
    for doc_i in docList:

        doc = open(doc_i, "r")
        doc = doc.read()
        print(doc)
        print(type(doc))
        doc = normalize(doc)

        #if args.names: # then redact names
        #    redactNames(doc)

        #if args.genders: # then redact gender
        #    redactGenders(doc)

        #if args.dates: # then redact dates
        #    redactDates(doc)

        #if args.phones: # then redact phone numbers
        #    redactPhones(doc)

        #if args.concept: # then redact all sentences relating to the concept provided
        #    redactConcepts(doc, concepts)

        if args.curses: # then redact all vowels in curse words
            redactCurses(doc)

        doc.close()

def normalize(doc):
    # Remove special charaters/whitespace
    doc = re.sub(r'[^a-zA-Z\s]', '', doc, re.I|re.A)

    # Convert everything to lowercase
    doc = doc.lower()
    doc = doc.strip() # not sure what this does, but it's in the textbook

    # Tokenize
    doc = nlp(doc)
    for token in doc:
        print(token.text)
    
    # Remove contractions


    # Remove stop words
    filtered_tokens = [token for token in tokens if token not in stop_words]

    # Re-create normalized document from filtered tokens
    docNorm = ' '.join(filtered_tokens)

    # Return normalized document
    return docNorm

def redactNames(doc):
    print("Redacting names...")

    # Replace any/all characters within a name with the full block (█) character 

    print("Names have been redacted")



def redactGenders(doc):
    print("Redacting genders...")

    

    print("Genders have been redacted")


def redactDates(doc):
    print("Redacting dates...")
    

    
    print("Dates have been redacted")


def redactPhones(doc):
    print("Redacting phone numbers...")



    print("Phone numbers have been redacted")


def redactConcepts(doc, concepts):
    for c in concepts:
        print("Redacting concept '" + c + "'...")


    print("Concepts have been redacted")

def redactCurses(doc):
    print("Redacting curse words...")
    
    curseWords = ["ass", "bitch", "cock", "crap", "cunt", "damn", "fuck", "hell", "piss", "shit", "slut", "twat", "whore"]
    
    for token in doc:
        if token in curseWords:
            print(re.sub(r'[aeiou]+', "*", token))

    print("Curse words have been redacted")

if __name__ == '__main__':
    epilog = "\nFor full information, see:\n" + projURL
    parser = argparse.ArgumentParser(epilog=epilog)
             
    # Set up arguments
    parser.add_argument("-i", "--input", type=str, required=True,
                        help="Glob for valid text file(s)")
    parser.add_argument("-n", "--names", type=str)
    parser.add_argument("-g", "--genders", type=str)
    parser.add_argument("-d", "--dates", type=str)
    parser.add_argument("-p", "--phones", type=str)
    parser.add_argument("-x", "--curses", type=str)
    parser.add_argument("-c", "--concept", type=str)
    parser.add_argument("-o", "--output", type=str, 
                        help="Directory to write redacted files to")
    parser.add_argument("-s", "--stats", type=str)
    
    args = parser.parse_args()
    if args.input:
        docList = glob.glob(args.input)
        main(docList)



