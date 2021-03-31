# to run: pipenv run python project0/main.py --incidents https://www.normanok.gov/sites/default/files/documents/2021-02/2021-02-21_daily_incident_summary.pdf

import argparse # dunder thing
import PyPDF2 # readData()
import re # readData()
import sqlite3 # createDB()
import urllib.request # fetchData()

def main(url):
    
    #print("Initiating Project 0...")
    
    #url = "https://www.normanok.gov/sites/default/files/documents/2021-02/2021-02-21_daily_incident_summary.pdf"
    
    # Download data
    fetchData(url)

    # Extract data
    incidents = readData()
    
    # Create our SQLite database
    db = createDB()

    # Insert data
    populateDB(incidents)

    # Run the requested query
    countNature()

def fetchData(url):
    #print("Fetching data...")
    
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17" 
    data = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read()

    # Write the pdf data to a temp file
    tmp_file = open("/tmp/data.pdf", "wb")
    tmp_file.write(data)

    #print("Data has been fetched!")

def readData():
    #print("Reading the PDF...")

    fp = open("/tmp/data.pdf", "rb")

    # Set the cursor of the file back to the begining
    fp.seek(0)

    # Read the PDF
    pdfReader = PyPDF2.pdf.PdfFileReader(fp)
    page_count = pdfReader.getNumPages()
    #print(f"Page count: ", page_count)

    # Get the first page
    #page1 = pdfReader.getPage(0).extractText()
    #print(f"page 0 text: ", page1)
    
    # Initialize list for clean data
    cleanData = []

    # Loop through each page of the pdf and extract the rows
    for i in range(page_count):
        page_i = pdfReader.getPage(i).extractText()
        #print("Page ", i+1, ":\n", page_i)

        # Clean up the data using regex
        dirtyMatch = re.findall(r'([0-9/: ]*)\n([0-9]{4}-[0-9]{8})\n(.*)(\n(.*))?\n(.*)\n(\w*)\n', page_i)
        
        for k in range(len(dirtyMatch)):
            tuple_k = dirtyMatch[k]
            
            if tuple_k[4]:                                                  # if the address overflows
                addr = tuple_k[2] + tuple_k[4]                              # paste the 2 pieces together
                cleanTuple = tuple_k[0:2] + (addr,) + tuple_k[5:7]          # put the tuple back together

                # Add cleaned tuple to list of data
                cleanData.append(cleanTuple)
            else:                                                           # otherwise,
                cleanTuple = tuple_k[0:3] + tuple_k[5:7]                    # just make a tuple without the empty slots

                # Add cleaned tuple to list of data
                cleanData.append(cleanTuple)
    
    #print(cleanData)

    return cleanData

def createDB():
    #print("Creating a database...")
    
    # Create connection object that represents the database
    con = sqlite3.connect('normanpd.db')
    
    # Create a cursor object
    cur = con.cursor()

    # Delete table if it already exists
    cur.execute('DROP TABLE IF EXISTS incidents')

    # Create table
    cur.execute('''
                    CREATE TABLE incidents (
                        incident_time TEXT,
                        incident_number TEXT,
                        incident_location TEXT,
                        nature TEXT,
                        incident_ori TEXT
                    )
                ''')

    # Save (commit) the changes
    con.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    con.close()

def populateDB(incidents):
    #print("Populating database...")

    # Connect to our database
    con = sqlite3.connect('normanpd.db')

    # Create cursor
    cur = con.cursor()

    # TESTING w/ some fake data
    #incidents = [('2/21/2021 0:12', '2021-00010177', '2543 W MAIN ST', 'Disturbance/Domestic', 'OK0140200'),
    #             ('2/21/2021 0:20', '2021-00010178', '2543 W MAIN ST', 'Traffic Stop', 'OK0140200'),
    #             ('2/21/2021 0:12', '2021-00010179', '2543 W MAIN ST', 'Drunk Driver', 'OK0140200'),
    #             ('2/21/2021 0:12', '2021-00010179', '2543 W MAIN ST', 'Drunk Driver', 'OK0140200'),]

    # Insert many rows of data, each with 5 values
    cur.executemany("INSERT INTO incidents VALUES (?,?,?,?,?)", incidents)

    # Don't forget to save and close, dummy!!!!
    con.commit()
    con.close()

def countNature():
    #print("Counting incidents by nature...")
    # Ultimately, we want to:
        # Group incidents by nature
        # Count number of times each nature occurred
        # Alphabetize by nature
        # Separate fields with pipe (|)

    # Let's write some SQL
    con = sqlite3.connect('normanpd.db')
    cur = con.cursor()

    cur.execute('''
                    SELECT nature, count(nature)
                    FROM incidents 
                    GROUP BY (nature)
                    ORDER BY nature
                ''')
    
    # Extract our list of natures and print in nice format
    natureList = cur.fetchall()
    
    # Loop through each item in the list
    for i in range(len(natureList)):
        # Grab the ith tuple from the list
        tuple_i = natureList[i]
        # Grab the nature from the tuple
        nature = tuple_i[0]
        # Grab the count from the tuple
        count = tuple_i[1]
        # Print the nature and count, separated by a pipe
        print(f"{nature}|{count}")

    con.commit()
    con.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, 
                         help="Incident summary url.")
             
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)



