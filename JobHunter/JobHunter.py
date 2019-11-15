# This script pulls from a job website and stores positions into a database. If there is a new posting it notifies the user.
# CNA 330 Fall 2019
# Samuel Lee ussameul88@gmail.com
# Working with Brandon, Emily
# Got help from Robin

import mysql.connector
import json
import urllib.request
import time
from datetime import datetime
import os
# import sys, not needed


# Connect to database
# You may need to edit the connect function based on your local settings.


def connect_to_sql():
    conn=mysql.connector.connect ( user = 'admin', password = 'CDwlsXsRRM3Xxk1F',
                                   host = '127.0.0.1', port = 3309,
                                   database = 'cna330' )
    return conn


# Create the table structure
def create_tables(cursor, table):
    ## Add your code here. Starter code below
    cursor.execute('''CREATE TABLE IF NOT EXISTS job_hunt (id INT PRIMARY KEY auto_increment, Type varchar(10), Title varchar(100), Description text CHARSET utf8,
        Job_id varchar(50), Created_at DATE, Company varchar(100), Location varchar(50), How_to_apply varchar(300)); ''')# Robin Help with this

    return


# Query the database.
# You should not need to edit anything in this function
def query_sql(cursor, query):
    cursor.execute(query)
    return cursor


def add_new_job(cursor, jobdetails):
    # extract all required columns
    type=jobdetails['type']
    created_at=time.strptime(jobdetails['created_at'], "%a %b %d %H:%M:%S %Z %Y" )
    company=jobdetails['company']
    location=jobdetails['location']
    title=jobdetails['title']
    description=jobdetails['description']
    how_to_apply=jobdetails['how_to_apply']
    job_id=jobdetails['id']
    query=cursor.execute (
        "INSERT INTO job_hunt(Type, Title, Description, Job_id, Created_at, Company, Location, How_to_apply" ") " 
        "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", (type, title, description, job_id, created_at, company, location, how_to_apply))
    return query_sql(cursor, query)  # line 43 to 57 copied from robin


# Add a new job

# Check if new job
def check_if_job_exists(cursor, jobdetails):
    job_id=jobdetails['id']
    query="SELECT * FROM job_hunt WHERE Job_id = \"%s\"" % job_id
    return query_sql(cursor, query)


# copy from Robin
# Deletes job
def delete_job(cursor, jobdetails):
    job_id=jobdetails['id']
    query="DELETE FROM job_hunt WHERE Job_id = \"%s\"" % job_id
    return query_sql(cursor, query)


# copy from Robin

# Grab new jobs from a website
def fetch_new_jobs(arg_dict):
    # Code from https://github.com/RTCedu/CNA336/blob/master/Spring2018/Sql.py
    query="https://jobs.github.com/positions.json?"+"location=seattle"  ## Add arguments here
    jsonpage=0
    try:
        contents=urllib.request.urlopen(query)
        response=contents.read()
        jsonpage=json.loads(response)
    except:
        pass
    return jsonpage


# Load a text-based configuration file, not function needed per Zak
"""def load_config_file(filename):
    argument_dictionary=0
    # Code from https://github.com/RTCedu/CNA336/blob/master/Spring2018/FileIO.py
    rel_path=os.path.abspath ( os.path.dirname ( __file__ ) )
    file=0
    file_contents=0
    try:
        file=open ( filename, "r" )
        file_contents=file.read ()
    except FileNotFoundError:
        print ( "File not found, it will be created." )
        file=open ( filename, "w" )
        file.write ( "" )
        file.close ()

    ## Add in information for argument dictionary
    return argument_dictionary"""


# Main area of the code.
def jobhunt(arg_dict, cursor):
    # Fetch jobs from website
    jobpage = fetch_new_jobs(arg_dict)  # Gets github website and holds the json data in it as a list
    # use below print statement to view list in json format
    # print(jobpage)
    add_or_delete_job(jobpage, cursor)

def add_or_delete_job(jobpage, cursor):
    # Add your code here to parse the job page
    for jobdetails in jobpage:  # EXTRACTS EACH JOB FROM THE JOB LIST
        # Add in your code here to check if the job already exists in the DB
        check_if_job_exists(cursor, jobdetails)
        is_job_found=len(cursor.fetchall()) > 0
        if is_job_found:
            # DELETE JOB
            # EXTRA CREDIT: Add your code to delete old entries
            now=datetime.now()
            job_date=datetime.strptime(jobdetails['created_at'], "%a %b %d %H:%M:%S %Z %Y")
            if (now-job_date).days > 30:
                print("Delete job: "+jobdetails["title"]+" from "+jobdetails["company"]+", Created at: "+jobdetails["created_at"]+", JobID: "+jobdetails['id'])
                delete_job(cursor, jobdetails)
        else:
            # INSERT JOB
            # Add in your code here to notify the user of a new posting
            print("New job is found: "+jobdetails["title"]+" from "+jobdetails["company"]+", Created at: "+jobdetails["created_at"]+", JobID: "+jobdetails['id'])
            add_new_job(cursor, jobdetails)


# Copied from Robin's from line 120 to 138

# CRUD Create, Read, Update, Delete
# ISUD Insert Select, Update, Delete

# https://www.computerhope.com/issues/ch001721.htm
# https://stackoverflow.com/questions/18366554/how-to-search-for-word-in-text-file-and-print-part-of-line-with-python
# Got a hint from m = re.search(r'(color\=.+?(?= )|color\=.+?$)', line)
# if m:
#    text = m.group() # Matched text here
# looked at youtube video https://www.youtube.com/watch?v=Dkiz0z3bMg0
# https://www.guru99.com/python-regular-expressions-complete-tutorial.html


## Add your code here to parse the job page
#   for jobdetails in jobpage:
#        print(jobdetails)  # Robin help with this

## Add in your code here to check if the job already exists in the DB

## Add in your code here to notify the user of a new posting

## EXTRA CREDIT: Add your code to delete old entries


# Setup portion of the program. Take arguments and set up the script
# You should not need to edit anything here.
def main():
    # Connect to SQL and get cursor
    conn=connect_to_sql()
    cursor=conn.cursor()
    create_tables(cursor, "job_hunt")
    # Load text file and store arguments into dictionary
    arg_dict=0
    while (1):
        jobhunt(arg_dict, cursor)
        time.sleep(3600)  # Sleep for 1h


if __name__ == '__main__':
    main()
