# to run: pipenv run python redactor.py --input '*.txt' \ --names --dates --phones \ --concept 'kids' \ --output 'files/' \ --stats stderr

import argparse # dunder thing
import re # regular expressions
import glob
import spacy
from spacy.tokens import Doc, Span, Token
from spacy.matcher import Matcher

projURL = "https://github.com/yut4916/cs5293sp21-project1.git"

nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)

# Define curse getter
curseWords = ("ass", "bitch", "cock", "crap", "cunt", "damn", "fuck", "hell", "piss", "shit", "slut", "twat", "whore")    
curse_getter = lambda token: token.text in curseWords
curse_setter = lambda token: re.sub(r'[aeiou]+', "*", token.text)
has_curse_getter = lambda obj: any([t.text in curseWords for t in obj])
Token.set_extension("is_curse", getter=curse_getter, setter=curse_setter)
Doc.set_extension("has_curse", getter=has_curse_getter)

# Define patterns for matching

def main(docList):
    print("Initiating Project 1...")
    print("Redacting the following documents:\n", docList)

    args = parser.parse_args()
    
    if args.stats:
        statsDir = args.stats
        statsFile = open(statsDir, "w")
    
    for doc_i in docList:
        txt = open(doc_i, "r")
        txt = txt.read()
        doc = nlp(txt)
        print(doc)
        print(type(doc))
        #doc = normalize(doc)

        # Redact using named entities
        #redacted = redactEntities(txt)
        #print(redacted)


        if args.names: # then redact names
            redacted = redactNames(txt)

        if args.genders: # then redact gender
            redactedG = redactGenders(doc)
            print(redactedG)

        if args.phones: # then redact phone numbers
            redacted = redactPhones(redacted)
            #print(redacted)
        
        if args.dates: # then redact dates
            redacted = redactDates(redacted)
            print(redacted)

        if args.concept: # then redact all sentences relating to the concept provided
            redactedC = redactConcepts(txt, concepts)

        if args.curses: # then redact all vowels in curse words
            redactedX = redactCurses(redacted)

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


def redactEntities(txt): # txt = string
    # Named Entity Recognition
    # doc.ents = named entities https://spacy.io/usage/linguistic-features
    redactedTxt = txt
    doc = nlp(txt)
    
    # Keep track of stats
    args = parser.parse_args()
    statsDir = args.stats
    stats = []
    
    for ent in reversed(doc.ents):
        # create a sequence of blocks as long as the text to be redacted.
        first = ent.start_char # index of start of redaction
        last = ent.end_char # index of end of redaction
        sharpie = "█"*(last - first)
        
        # new text is everything before the redaction plus the blocks plus everything after the redaction.
        # splice using colon
        redactedTxt = redactedTxt[:first] + sharpie + redactedTxt[last:]

        # be sure to keep track of what we're redacting
        removed = ent.label_
        stats.append(removed)
    
    if args.stats:
        with open(statsDir, "a") as statsFile:
            statsFile.writelines("%s\n" % stat for stat in stats)
        statsFile.close()

    return redactedTxt


def redactNames(txt):
    print("Redacting names...")

    # Named Entity Recognition
    # doc.ents = named entities https://spacy.io/usage/linguistic-features
    redactedTxt = txt
    doc = nlp(txt)
    
    # Keep track of stats
    args = parser.parse_args()
    statsDir = args.stats
    stats = []
    
    # Define "name"
    nameEnts = ("PERSON")

    for ent in reversed(doc.ents):
        if ent.label_ in nameEnts:
            # create a sequence of blocks as long as the text to be redacted.
            first = ent.start_char # index of start of redaction
            last = ent.end_char # index of end of redaction
            sharpie = "█"*(last - first)
        
            # new text is everything before the redaction plus the blocks plus everything after the redaction.
            # splice using colon
            redactedTxt = redactedTxt[:first] + sharpie + redactedTxt[last:]

            # be sure to keep track of what we're redacting
            removed = ent.label_
            stats.append(removed)
    
    if args.stats:
        with open(statsDir, "a") as statsFile:
            statsFile.writelines("%s\n" % stat for stat in stats)
        statsFile.close()
    
    print("Names have been redacted")

    return redactedTxt

def redactGenders(doc):
    print("Redacting genders...")

    genderDict = ("he", "her", "hers", "herself", "him", "himself", "his", "she", "aunt", 
            "brother", "brother-in-law", "daughter", "daughter-in-law", "father", "father-in-law", 
            "granddaughter", "grandson", "half brother", "half sister", "husband", "mother", 
            "mother-in-law", "nephew", "niece", "sister", "sister-in-law", "son", "son-in-law", 
            "stepbrother", "stepdaughter", "stepfather", "stepmother", "stepsister", "stepson", 
            "uncle", "wife", "boy", "man", "gentleman", "woman", "girl", "lady", 
            "mr", "mrs", "ms", "miss", "sir", "ma'am", "girlfriend", "boyfriend")

    print("Genders have been redacted")


def redactDates(txt):
    print("Redacting dates...")
    
    # Named Entity Recognition
    # doc.ents = named entities https://spacy.io/usage/linguistic-features
    redactedTxt = txt
    doc = nlp(txt)
    
    # Keep track of stats
    args = parser.parse_args()
    statsDir = args.stats
    stats = []
    
    for ent in reversed(doc.ents):
        if ent.label_ == "DATE":
            # create a sequence of blocks as long as the text to be redacted.
            first = ent.start_char # index of start of redaction
            last = ent.end_char # index of end of redaction
            sharpie = "█"*(last - first)
        
            # new text is everything before the redaction plus the blocks plus everything after the redaction.
            # splice using colon
            redactedTxt = redactedTxt[:first] + sharpie + redactedTxt[last:]

            # be sure to keep track of what we're redacting
            removed = ent.label_
            stats.append(removed)
    
    if args.stats:
        with open(statsDir, "a") as statsFile:
            statsFile.writelines("%s\n" % stat for stat in stats)
        statsFile.close()

    print("Dates have been redacted")
    
    return redactedTxt


def redactPhones(txt): # txt = string
    print("Redacting phone numbers...")
    sharpie = "█"*10
    cleanTxt = re.sub(r'(\+\d{1,2}\s)?(\(?\d{3}\)?[\s.-]?)?\d{3}[\s.-]?\d{4}', sharpie, txt)

    print("Phone numbers have been redacted")
    return cleanTxt

def redactConcepts(doc, concepts):
    for c in concepts:
        print("Redacting concept '" + c + "'...")


    print("Concepts have been redacted")

def redactCurses(txt):
    print("Redacting curse words...")
    redactedTxt = txt
    doc = nlp(txt)
    
    # Keep track of stats
    args = parser.parse_args()
    statsDir = args.stats
    stats = []
    
    for token in reversed(doc):
        if token._.is_curse:
            token._.set("is_curse")

            tokenIndex = token.i
            scrubbed = re.sub(r'[aeiou]+', "*", doc[tokenIndex].text)
            with doc.retokenize() as retokenizer:
                retokenizer.merge(doc[tokenIndex+1:])
                redactedTxt = doc[0:tokenIndex].text + scrubbed + " " + doc[tokenIndex+1:].text

            # be sure to keep track of what we're redacting
            removed = token
            stats.append(removed)
    
    if args.stats:
        with open(statsDir, "a") as statsFile:
            statsFile.writelines("%s\n" % stat for stat in stats)
        statsFile.close()

    print(redactedTxt)
    print("Curse words have been redacted")
    return redactedTxt

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



