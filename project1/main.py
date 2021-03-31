# to run: pipenv run python redactor.py --input '*.txt' \ --names --dates --phones \ --concept 'kids' \ --output 'files/' \ --stats stderr

import argparse # dunder thing
import re # readData()
import glob

projURL = "https://github.com/yut4916/cs5293sp21-project1.git"

def main(docList):
    print("Initiating Project 1...")

    args = parser.parse_args()
    
    for doc_i in docList:

        doc = open(doc_i, "r")

        print(doc.read())

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

        doc.close()

def redactNames(doc):
    print("Redacting names...")



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
    parser.add_argument("-c", "--concept", type=str)
    parser.add_argument("-o", "--output", type=str, 
                        help="Directory to write redacted files to")
    parser.add_argument("-s", "--stats", type=str)
    
    args = parser.parse_args()
    if args.input:
        docList = glob.glob(args.input)
        print(docList)
        main(docList)



