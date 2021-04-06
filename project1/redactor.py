# to run: pipenv run python redactor.py --input '*.txt' \ --names --dates --phones \ --concept 'kids' \ --output 'files/' \ --stats stderr

import argparse # dunder thing
import re # regular expressions
import glob
import spacy
from spacy.tokens import Doc, Span, Token
from spacy.matcher import Matcher

# Global setup (idk if this is allowed)
nlp = spacy.load("en_core_web_sm")

def buildNLP():
    # Define curse getter
    curseWords = ["ass", "bitch", "cock", "crap", "cunt", "damn", "fuck", "hell", "piss", "shit", "slut", "twat", "whore"]    
    cursePattern1 = [{"LEMMA": {"IN": curseWords}}]
    # note: patterns 2-14 find regex match of each word in curseWords if has anything before or after
    # also, i am absolutely certain there's a way to automate this replication, but i could not figure it out
    cursePattern2 = [{"TEXT": {"REGEX": "\s?\S*" + curseWords[0] + "\S*\s?"}}]
    cursePattern3 = [{"TEXT": {"REGEX": "\s?\S*" + curseWords[1] + "\S*\s?"}}]
    cursePattern4 = [{"TEXT": {"REGEX": "\s?\S*" + curseWords[2] + "\S*\s?"}}]
    cursePattern5 = [{"TEXT": {"REGEX": "\s?\S*" + curseWords[3] + "\S*\s?"}}]
    cursePattern6 = [{"TEXT": {"REGEX": "\s?\S*" + curseWords[4] + "\S*\s?"}}]
    cursePattern7 = [{"TEXT": {"REGEX": "\s?\S*" + curseWords[5] + "\S*\s?"}}]
    cursePattern8 = [{"TEXT": {"REGEX": "\s?\S*" + curseWords[6] + "\S*\s?"}}]
    cursePattern9 = [{"TEXT": {"REGEX": "\s?\S*" + curseWords[7] + "\S*\s?"}}]
    cursePattern10 = [{"TEXT": {"REGEX": "\s?\S*" + curseWords[8] + "\S*\s?"}}]
    cursePattern11 = [{"TEXT": {"REGEX": "\s?\S*" + curseWords[9] + "\S*\s?"}}]
    cursePattern12 = [{"TEXT": {"REGEX": "\s?\S*" + curseWords[10] + "\S*\s?"}}]
    cursePattern13 = [{"TEXT": {"REGEX": "\s?\S*" + curseWords[11] + "\S*\s?"}}]
    cursePattern14 = [{"TEXT": {"REGEX": "\s?\S*" + curseWords[12] + "\S*\s?"}}]
    
    # Define patterns for matching
    genderDict = ["he", "her", "hers", "herself", "him", "himself", "his", "she", "aunt", 
            "brother", "brother-in-law", "daughter", "daughter-in-law", "father", "father-in-law", 
            "granddaughter", "grandson", "half brother", "half sister", "husband", "mother", 
            "mother-in-law", "nephew", "niece", "sister", "sister-in-law", "son", "son-in-law", 
            "stepbrother", "stepdaughter", "stepfather", "stepmother", "stepsister", "stepson", 
            "uncle", "wife", "boy", "man", "gentleman", "woman", "girl", "lady", 
            "mr", "mrs", "ms", "miss", "sir", "ma'am", "girlfriend", "boyfriend"]
    genderPattern = [{"LEMMA": {"IN": genderDict}}]
    patterns = [{"label": "GENDER", "pattern": genderPattern},
                {"label": "CURSE", "pattern": cursePattern1},
                {"label": "CURSE", "pattern": cursePattern2},
                {"label": "CURSE", "pattern": cursePattern3},
                {"label": "CURSE", "pattern": cursePattern4},
                {"label": "CURSE", "pattern": cursePattern5},
                {"label": "CURSE", "pattern": cursePattern6},
                {"label": "CURSE", "pattern": cursePattern7},
                {"label": "CURSE", "pattern": cursePattern8},
                {"label": "CURSE", "pattern": cursePattern9},
                {"label": "CURSE", "pattern": cursePattern10},
                {"label": "CURSE", "pattern": cursePattern11},
                {"label": "CURSE", "pattern": cursePattern12},
                {"label": "CURSE", "pattern": cursePattern13},
                {"label": "CURSE", "pattern": cursePattern14}]
    ruler = nlp.add_pipe("entity_ruler")
    ruler.add_patterns(patterns)

def main(docList):
    print("Initiating Project 1...")
    print("Redacting the following documents:\n", docList)

    args = parser.parse_args()
    
    # Initiate stats file
    if args.stats:
        statsDir = args.stats
        statsFile = open(statsDir, "w")
        statsFile.close()
    
    # Run functions to generate custom NLP
    buildNLP()

    for doc_i in docList:
        print("Redacting " + doc_i + "...")

        # Write doc_i header for stats file 
        if args.stats:
            statsFile = open(args.stats, "a")
            statsFile.write("\nSummary of redactions for document '" + doc_i + "':\n")
            statsFile.close()
        
        # Open ith file
        txt = open(doc_i, "r")
        txt = txt.read()
        #doc = nlp(txt)
        #print("Original document:\n" + doc.text)
        #print(type(doc))
        
        redacted = txt # initialize
        if args.names: # then redact names
            redacted = redactNames(redacted)

        if args.genders: # then redact gender
            redacted = redactGenders(redacted)
            #print(redacted)

        if args.phones: # then redact phone numbers
            redacted = redactPhones(redacted)
            #print(redacted)
        
        if args.dates: # then redact dates
            redacted = redactDates(redacted)
            #print(redacted)

        if args.concept: # then redact all sentences relating to the concept provided
            redactedC = redactConcepts(txt, concepts)

        if args.curses: # then redact all vowels in curse words
            redacted = redactCurses(redacted)
        
        #print(redacted)

        # Write redacted files
        outDir = args.output
        with open(outDir + doc_i + ".redacted", "w") as txtRedacted:
            txtRedacted.write(redacted)
        txtRedacted.close()

    print("Redaction process complete. Check '.redacted' files for output and '" + args.stats + "' for redaction summary stats.")

def redactNames(txt):
    #print("Redacting names...")

    # Named Entity Recognition
    # doc.ents = named entities https://spacy.io/usage/linguistic-features
    redactedTxt = txt
    doc = nlp(txt)
    
    # Define "name"
    nameEnts = ("PERSON")

    # Keep track of stats
    args = parser.parse_args()
    statsDir = args.stats
    numRedactions = len([ent for ent in doc.ents if ent.label_ in nameEnts])
    stats = "Total names redacted: " + str(numRedactions) + "\n" 
    if args.stats:
        with open(statsDir, "a") as statsFile:
            statsFile.write(stats)
        statsFile.close()
    
    for ent in reversed(doc.ents):
        if ent.label_ in nameEnts:
            # create a sequence of blocks as long as the text to be redacted.
            first = ent.start_char # index of start of redaction
            last = ent.end_char # index of end of redaction
            sharpie = "█"*(last - first)
        
            # new text is everything before the redaction plus the blocks plus everything after the redaction.
            # splice using colon
            redactedTxt = redactedTxt[:first] + sharpie + redactedTxt[last:]

    #print("Names have been redacted")
    return redactedTxt

def redactGenders(txt):
    #print("Redacting genders...")
    
    # Named Entity Recognition
    redactedTxt = txt
    doc = nlp(txt.lower())
    
    # Keep track of stats
    args = parser.parse_args()
    statsDir = args.stats
    numRedactions = len([ent for ent in doc.ents if ent.label_ == "GENDER"])
    stats = "Total gendered terms redacted: " + str(numRedactions) + "\n" 
    if args.stats:
        with open(statsDir, "a") as statsFile:
            statsFile.write(stats)
        statsFile.close()
    
    for ent in reversed(doc.ents):
        if ent.label_ == "GENDER":
            # create a sequence of blocks as long as the text to be redacted.
            first = ent.start_char # index of start of redaction
            last = ent.end_char # index of end of redaction
            sharpie = "█"*(last - first)
        
            # new text is everything before the redaction plus the blocks plus everything after the redaction.
            # splice using colon
            redactedTxt = redactedTxt[:first] + sharpie + redactedTxt[last:]

    #print("Genders have been redacted")
    return redactedTxt

def redactDates(txt):
    #print("Redacting dates...")
    
    # Named Entity Recognition
    redactedTxt = txt
    doc = nlp(txt)
    
    # Keep track of stats
    args = parser.parse_args()
    statsDir = args.stats
    numRedactions = len([ent for ent in doc.ents if ent.label_ == "DATE"])
    stats = "Total dates redacted: " + str(numRedactions) + "\n" 
    if args.stats:
        with open(statsDir, "a") as statsFile:
            statsFile.write(stats)
        statsFile.close()
    
    for ent in reversed(doc.ents):
        if ent.label_ == "DATE":
            # create a sequence of blocks as long as the text to be redacted.
            first = ent.start_char # index of start of redaction
            last = ent.end_char # index of end of redaction
            sharpie = "█"*(last - first)
        
            # new text is everything before the redaction plus the blocks plus everything after the redaction.
            # splice using colon
            redactedTxt = redactedTxt[:first] + sharpie + redactedTxt[last:]

    #print("Dates have been redacted")
    return redactedTxt

def redactPhones(txt): # txt = string
    #print("Redacting phone numbers...")
    sharpie = "█"*10
    subTuple = re.subn(r'(\+\d{1,2}\s)?(\(?\d{3}\)?[\s.-]?)?\d{3}[\s.-]?\d{4}', sharpie, txt)
    cleanTxt = subTuple[0]
    nsubs = subTuple[1]
    
    # Keep track of stats
    args = parser.parse_args()
    statsDir = args.stats
    stats = "Total phone numbers redacted: " + str(nsubs) + "\n" 
    if args.stats:
        with open(statsDir, "a") as statsFile:
            statsFile.write(stats)
        statsFile.close()

    #print("Phone numbers have been redacted")
    return cleanTxt

def redactConcepts(doc, concepts):
    for c in concepts:
        print("Redacting concept '" + c + "'...")


    print("Concepts have been redacted")

def redactCurses(txt):
    #print("Redacting curse words...")
    
    # Named Entity Recognition
    redactedTxt = txt
    doc = nlp(txt)
    
    # Keep track of stats
    args = parser.parse_args()
    statsDir = args.stats
    numRedactions = len([ent for ent in doc.ents if ent.label_ == "CURSE"])
    stats = "Total curse words redacted: " + str(numRedactions) + "\n" 
    if args.stats:
        with open(statsDir, "a") as statsFile:
            statsFile.write(stats)
        statsFile.close()
    
    for ent in reversed(doc.ents):
        if ent.label_ == "CURSE":
            # replace vowels with asterisks using regex
            scrubbed = re.sub(r'[aeiou]+', "*", ent.text)
        
            # new text is everything before the redaction plus the blocks plus everything after the redaction.
            # splice using colon
            first = ent.start_char # index of start of redaction
            last = ent.end_char # index of end of redaction
            redactedTxt = redactedTxt[:first] + scrubbed + redactedTxt[last:]
    
    #print("Curse words have been redacted")
    return redactedTxt

if __name__ == '__main__':
    projURL = "https://github.com/yut4916/cs5293sp21-project1.git"

    # Set up argument parsing
    epilog = "\nFor full information, see:\n" + projURL
    parser = argparse.ArgumentParser(epilog=epilog)
             
    # Set up arguments
    parser.add_argument("-i", "--input", type=str, required=True,
                        help="Glob for valid text file(s)")
    parser.add_argument("-n", "--names", type=bool,
                        help="Whether or not peoples' names should be redacted")
    parser.add_argument("-g", "--genders", type=bool,
                        help="Whether or not gendered terms should be redacted")
    parser.add_argument("-d", "--dates", type=bool,
                        help="Whether or not dates should be redacted")
    parser.add_argument("-p", "--phones", type=bool,
                        help="Whether or not phone numbers should be redacted")
    parser.add_argument("-x", "--curses", type=bool,
                        help="Whether or not curse words should be redacted")
    parser.add_argument("-c", "--concept", type=str,
                        help="Topic(s) for which to redact entire sentences")
    parser.add_argument("-o", "--output", type=str, required=True, 
                        help="Directory to write redacted files to")
    parser.add_argument("-s", "--stats", type=str,
                        help="File and/or directory to which to write summary stats of redaction process")
    
    args = parser.parse_args()
    if args.input:
        docList = glob.glob(args.input)
        main(docList)


