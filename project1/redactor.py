# to run: pipenv run python redactor.py --input '*.txt' \ --names --dates --phones \ --concept 'kids' \ --output 'files/' \ --stats stderr

import argparse # dunder thing
import re # readData()
import glob
import spacy
from spacy.tokens import Token
from spacy.matcher import Matcher

projURL = "https://github.com/yut4916/cs5293sp21-project1.git"

nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)

# Define curse getter
curseWords = ("ass", "bitch", "cock", "crap", "cunt", "damn", "fuck", "hell", "piss", "shit", "slut", "twat", "whore")    
curse_getter = lambda token: token.text in curseWords
Token.set_extension("is_curse", getter=curse_getter)

# Define patterns for matching
phonesPattern = [{"IS_DIGIT": True, "OP": "+"}]

def replace_ner(mytxt):
    clean_text = mytxt
    doc = nlp(mytxt)
    for ent in reversed(doc.ents):
        clean_text = clean_text[:ent.start_char] +ent.label_ + clean_text[ent.end_char:]
    return clean_text
                             

def main(docList):
    print("Initiating Project 1...")
    print("Redacting the following documents:\n", docList)

    args = parser.parse_args()
    
    statsDir = args.stats

    for doc_i in docList:

        doc = open(doc_i, "r")
        doc = doc.read()
        print(doc)
        print(type(doc))
        #doc = normalize(doc)

        # Test replace_ner() function thing
        redacted = replace_ner(doc)
        print(redacted)


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

        #doc.close()

def normalize(doc):
    # Remove special charaters/whitespace
    #doc = re.sub(r'[^a-zA-Z\s]', '', doc, re.I|re.A)

    # Convert everything to lowercase
    doc = doc.lower()
    doc = doc.strip() # not sure what this does, but it's in the textbook
    
    # Tokenize
    doc_sp = nlp(doc)
    
    # Remove stop words
    #stop_words = nlp.Defaults.stop_words
    #filtered_tokens = [token for token in doc_sp if token not in stop_words]

    # Re-create normalized document from filtered tokens
    #docNorm = ' '.join(filtered_tokens)
    
    #print(filtered_tokens)
    #print(type(filtered_tokens))

    # Return normalized document
    return doc_sp

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
    
    curseIndex = []

    for token in doc:
        if token._.is_curse:
            #print(re.sub(r'[aeiou]+', "*", token))
            print(token.i)
            curseIndex.append(token.i)
    
    print("Curse words have been redacted")

if __name__ == '__main__':
    epilog = "\nFor full information, see:\n" + projURL
    parser = argparse.ArgumentParser(epilog=epilog)
             
    # Set up arguments
    parser.add_argument("-i", "--input", type=str, required=True,
                        help="Glob for valid text file(s)")
    parser.add_argument("-n", "--names", type=bool)
    parser.add_argument("-g", "--genders", type=bool)
    parser.add_argument("-d", "--dates", type=bool)
    parser.add_argument("-p", "--phones", type=bool)
    parser.add_argument("-x", "--curses", type=bool)
    parser.add_argument("-c", "--concept", type=str)
    parser.add_argument("-o", "--output", type=str, 
                        help="Directory to write redacted files to")
    parser.add_argument("-s", "--stats", type=str,
                        help="Directory/file to which to write summary stats of redaction process")
    
    args = parser.parse_args()
    if args.input:
        docList = glob.glob(args.input)
        main(docList)



