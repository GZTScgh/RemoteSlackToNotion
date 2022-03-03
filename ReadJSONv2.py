#Written by Colin Hanson - colin.hanson@gmail.com
# 3 March 2022

from datetime import date
import json
from operator import contains
from posixpath import split

with open("avengers-team.json", "r") as infile:             #define file
    data = json.loads(infile.read())                        #open file
    for line in data:                                       #parse each line
        print("*************** new line *****************")
       
        x = line["Text"].split(" | ")                       # use split to separate the sections delimited by the Pipe ( | ) symbol, including a space before and after. 
       
        if len(x) == 3:                                     # filtering out lines that aren't valid. Our data is quite predictable, little chance of false positives.
                                                            # Only continue evaluating lines that split into an array of 3 values.
            date = x[0]                                     # assign the first item of the array to the "date" variable
            print("Date value: ", date)
            
            LNFN = x[1].split(", ")                         # use split to separate the first and last names. Use the comma as delimiter, including a space after
            print("first name: ", LNFN[1])
            print("Last name: ", LNFN[0])
            FnameLname = LNFN[1] + " " + LNFN[0]            #Reassemble the name in the correct order, and add a space between first and last
            print("Reassembled name: ", FnameLname)
                        
            task = x[2]
            print("Task:", task)
            # with the components of the lines separated, they are ready to be used along with the code to interface with the Notion API.

            from encodings import utf_8
            import json
            import requests
            token = 'redacted'

            databaseID ='38dc0ca1b4cf41db98ae9f1b17933081'

            queryUrl = "https://api.notion.com/v1/databases/"+databaseID+"/query"


            headers = {
                "Authorization": "Bearer " + token, 
                "Accept": "application/json",
                "Notion-Version": "2022-02-22",
                "Content-Type": "application/json"
            }

            # this section is to query the database and write to a JSON file locally, not needed for writing to the database
            #response = requests.request("POST", queryUrl, json=payload, headers=headers)
            #print(response.status_code)
            #print(response.text)

            #data = response.json()
            #with open('./db2.json', 'w', encoding=None ) as f: 
            #    json.dump(data, f, ensure_ascii=False)


            def createPage(headers, UserName):                              # function to create a new entry in the Notion database

                createPageUrl = "https://api.notion.com/v1/pages"           # Notion API to create new entries in a database

                payload = {                                                 # Build the structure of the payload to inject 
                    "parent": { "database_id": databaseID },
                    "properties": {
                        "Name": {
                            "title": [
                                {
                                    "text": {
                                        "content": UserName
                                    }
                                }
                            ]
                        },
                                                                            # add additional attributes here (I can't figure out the formatting. Ouch.)
                    }
                }

                response = requests.request("POST", createPageUrl, json=payload, headers=headers)   # This is the business end of the Notion API.

                print(response.status_code)                                     # Spit out the status code
                print(response.text)                                            # spit out the response text. 

            createPage(headers,FnameLname)


        else:    
            print("the stuff in this entry isn't of interest #####################################") 
        

