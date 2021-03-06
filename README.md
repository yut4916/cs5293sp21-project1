# Project 1 for Text Analytics
Written by Katy Yut
March 31, 2021

## How to Install and Use This Package
To run: first, activate virtual environment by running "source .env/bin/activate". Then, run the following:
pipenv run python project1/redactor.py --input "input/\*.txt" 
	-n True -d True -p True -g True -x True 
	-c "family" -o "output/" -s "output/stats.txt" 

## Assumptions/Definitions
Name:
* Names are identified by the named entity recognition tool within spaCy

Date:
* Dates are also identified by the NER tool within spaCy, which captures both relative (e.g., tomorrow) and absolute (e.g. April 9th) dates

Gender:
* Includes pronouns: he, him, his, she, her, hers
* Family descriptors: brother, sister, mother/mom/mommy, father/dad/daddy, aunt, uncle, grandpa, grandma, son, daughter, etc.
* Titles: Mr., Ms., Mrs., Miss, sir, ma'am, etc.
* Nouns: boy, girl, man, woman, lady, gentleman, etc.

Phone number:
* Here is my regex: r'(\+\d{1,2}\s)?(\(?\d{3}\)?[\s.-]?)?\d{3}[\s.-]?\d{4}'
* Which matches:
	+ 0 or 1 country codes, which begin with + and have 1 or 2 digits
	+ 0 or 1 area codes, which are 3 digits long and may or may not be inside parentheses
	+ 0 or 1 whitespace/dash character
	+ 3 digits
	+ 0 or 1 whitespace/dash character
	+ 4 digits

1. Input file(s) will be in .txt format
2. The text will be in English

## Function Descriptions
### buildNLP()
Defines custom word lists for gender, curses, and concepts, turns them into patterns, and adds the patterns to the existing spacy nlp. This builds the custom component of the named entity recognition technique that I used to redact entities that didn't already exist.

### redactNames()
Runs the nlp on the given text document, loops through each named entity, checks if it's a name, and redacts it if True. Also keeps track of how many redactions there are and, if the stats argument is provided, writes the count to the stats file.  

### redactGenders()
Runs the nlp on the given text document(which has now been redacted of names, if indicated by the user), loops through each named entity, checks if it's a gendered term, and redacts it if True. Also keeps track of how many redactions there are and, if the stats argument is provided, writes the count to the stats file.  

### redactDates()
Runs the nlp on the given text document(which, just as before, has now been redacted of everything previous if indicated), loops through each named entity, checks if it's a date, and redacts it if True. Also keeps track of how many redactions there are and, if the stats argument is provided, writes the count to the stats file.  

### redactPhones()
Uses regex function re.subn() and the aforementioned phone number regex pattern to search the entire text document for matches. When it finds a match, it replaces it with ten full block characters (note: this is slightly different from the NER redaction, which uses the index of the first and last char to replace exactly the same number of characters. Regardless of how long the matching phone number was, it'll be replaced by 10 full block characters). Also keeps track of stats.

### redactConcepts()
Runs the nlp on the given text document, loops through each named entity, checks if it's a concept, and redacts it if True. The buildNLP() function has already hit the Merriam Webster thesaurus API for related words, built a dictionary, and created a pattern for matching any token whose lemma is in the dictionary. As per usual, it keeps track of redactions and writes the total to the stats file (if provided as an argument). 

### redactCurses()
Same as the other NER--runs the nlp and finds the entities labeled curses (established in buildNLP()), except this time, it only redacts the vowels, and instead of the full block character, it replaces them with an asterisk (f\*ck that's cool). 

## Approach/Steps/Inner Monologue/Project Diary
1. Setup file structure (i.e., duplicate and rename project0 directory)
	+ clean out proj0 README
	+ paste bare bones code provided in project outline
2. Revisit project goal: read in any/all .txt files provided and redact sensitive information (i.e., identify and replace with full block character)
	+ Intermediate requirements include: defining names, dates, phone numbers, concepts, etc. Rewatch lecture to see how Randy added flags. Figure out where to start and how to break it down into smaller, more manageable chunks. 
	+ Yeah ok I'm not really sure where to start, but I know I'm going to need some test data, so let's do that. I wrote a short test document and I'm starting to get my bearings.
3. Write skeleton code with the functions I'll need to complete the project.
	+ I think I'll need a function for each input flag -- i.e., redactNames(), redactGenders(), redactDates(), redactPhones(), and redactConcepts().
	+ I've included some print statements at the beginning and end of each function, so I can see when they're running. 
	+ I'll need to use the user-supplied glob to open the text file(s), which I can do with the open() function.
		- note: will apparently need to close the file when I'm done with it! (use fileVariable.close())
	+ So far, when I run it, it seems to be working just fine. I guess now I need to figure out how I'm going to do this redacting business?
4. Conceptualizing a general solution
	+ okay, so I know I'm going to need to use spacy/nltk. I guess I'll want to tokenize the text files, do some standardization techniques from class/the textbook, and then compare the cleaned text to some sort of dictionary for each of my tags.
		- need to figure out if those dictionaries exist within spacy/nltk or if I'm supposed to create/define them myself
	+ reading some basic [spacy 101](https://spacy.io/usage/spacy-101), i think that's the one I'm gonna wanna go with (at least to start).
5. Lots of different directions to go in. Some I have been exploring:
	+ best so far: Named Entity Recognition (NER) using .ents on spacy doc objects
	+ Token from spacy.tokens
	+ Matcher from spacy.matcher
	+ regex - issues w/ spacy token type and string compatibility
6. I figured out how to set up the stats file, so there's that. 
	+ it still definitely needs to be cleaned/processed though - maybe that should be done before i write it to a .txt....
7. Found a good regex for matching phone numbers on a stack overflow thread 
	+ How I found it: r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$'
	+ After my minor tweaks: r'(\+\d{1,2}\s)?(\(?\d{3}\)?[\s.-]?)?\d{3}[\s.-]?\d{4}'
8. Besides plain ol' regex for the phone numbers, I've been making decent headway with the named entity recognition technique. It works better by including an if statement to redact by each type of entity (person, date, organization, location, etc) instead of anything that registers as an entity
	+ note: for the custom named entity from a word list of gendered terms, I'll probably need to do some text normalization beforehand, since my dictionary doesn't account for pluralities, etc
	+ also, the named entities have a lot more categories than just the required names and dates. I could easily copy those functions and create additional flags for locations, organizations, etc
9. Still left to do:
	+ all of the concepts function
	+ all of writing tests
	+ flesh out/tidy up/complete README
	+ very last - record demo video
10. Successfully set up an API key with Merriam Webster, so hopefully I can figure out how to use that for the concepts flag. My plan is to grab a list of related words from their collegiate thesaurus.
	+ okay, so I figured out how to parse through the JSON that the API request returns (pain in the ass, btw. no chance that's the best way to do it)
	+ however, the related words list it's generating isn't great--even just tested on my small sample texts and a couple words, it's clearly not performing very well. some ideas to improve:
		- lemmatize the words the thesaurus returns?
		- pass the list of words through the thesaurus? would be a lot of requests and would get big fast. would also need to grab just the unique words.
		- allow the user to supply an optional list of custom words added to the redaction dictionary
	+ another thing: right now it's just redacting the specified words, like the other functions, not the whole sentence. need to figure that out too
11. Still need to figure out:
	+ how to accept multiple concept flags
	+ would also like to change the other tags from boolean. should just be able to pass the tag with no additional input
	+ requirements.txt file vs Pipfile

### General Notes
* sudo apt install pipenv -- used this command to give me permission to install pipenv
	+ note: sudo su changes me to the super user, all powerful omniscient being. be careful (type "exit" in command line to become mortal)
	+ note: this is just for installing system files
* pipenv install packageName -- install a python package into virtual python environment
* tmux kill-session -t 0 -- kill a tmux session (0 is the window ID)
* Idea: if I have time, I'd like to add an option to redact curse words, but instead of blocking out the whole word, I just want to replace the vowels with an asterisk (\*). 

# Citations
Throughout the project my dad, Greg Yut, helped me understand the nuts and bolts, presumably all the stuff I should've known prior to taking this class but didn't learn because I'm not a C S student (i.e. Linux syntax/quirks, troubleshooting tips, etc). 

While troubleshooting, I used the following resources:
- [Python File Open](https://www.w3schools.com/python/python_file_open.asp)
- [Redact Name Entities With SpaCy](https://predictivehacks.com/redact-name-entities-with-spacy/)
- [Python File Write](https://www.w3schools.com/python/python_file_write.asp)
- [Reading and Writing Lists to a File in Python](https://stackabuse.com/reading-and-writing-lists-to-a-file-in-python/)
- [Removing Stop Words from Strings in Python](https://stackabuse.com/removing-stop-words-from-strings-in-python/#usingthespacylibrary)
- [Regular expression to match standard 10 digit phone number](https://stackoverflow.com/questions/16699007/regular-expression-to-match-standard-10-digit-phone-number/16699507#16699507)
- [Named Entity Recognition NER using spaCy | NLP | Part 4](https://towardsdatascience.com/named-entity-recognition-ner-using-spacy-nlp-part-4-28da2ece57c6)
- [How to use an API with Python (Beginner???s Guide)](https://rapidapi.com/blog/how-to-use-an-api-with-python/)
- [How to Iterate Through a Dictionary in Python](https://realpython.com/iterate-through-dictionary-python/)
- [Working With JSON Data in Python](https://realpython.com/python-json/)
- [MERRIAM-WEBSTER'S COLLEGIATE?? THESAURUS](https://dictionaryapi.com/products/api-collegiate-thesaurus)

