# Project 0 for Text Analytics
Written by Katy Yut
March 31, 2021

## How to Install and Use This Package
To run: pipenv run python redactor.py --input '\*.txt' \
                    --names --dates --phones \
                    --concept 'kids' \
                    --output 'files/' \
                    --stats stderr

## Assumptions


## Function Descriptions


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

### General Notes
* sudo apt install pipenv -- used this command to give me permission to install pipenv
	+ note: sudo su changes me to the super user, all powerful omniscient being. be careful (type "exit" in command line to become mortal)
	+ note: this is just for installing system files
* pipenv install packageName -- install a python package into virtual python environment
* tmux kill-session -t 0 -- kill a tmux session (0 is the window ID)
* Idea: if I have time, I'd like to add an option to redact curse words, but instead of blocking out the whole word, I just want to replace the vowels with an asterisk (\*). 

## Testing
To run: pipenv run pytest


# Citations
Throughout the project my dad, Greg Yut, helped me understand the nuts and bolts, presumably all the stuff I should've known prior to taking this class but didn't learn because I'm not a C S student (i.e. Linux syntax/quirks, troubleshooting tips, etc). 

While troubleshooting, I used the following resources:
- [Python File Open](https://www.w3schools.com/python/python_file_open.asp)
