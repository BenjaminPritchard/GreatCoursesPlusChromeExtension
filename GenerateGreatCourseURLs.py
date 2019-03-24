# 
# GenerateGreatCourseURLs.py
#
# load in JSON file description of the great courses, extracted from:
#  https://www.thegreatcoursesplus.com/allcourses
# 
# Then use google custom search engine API request to search for each course on Google, 
# to locate the corresponding Great Courses URL for the course.
#
# Update the JSON to include the URL, then dump the results back out to disk
#
# This is used as part of the Great Courses Plus Google Chrome Plugin that I am developing, and is 
# sort of just a one-off type script, so not much real error checking is done...
# 
# Benjamin Pritchard / Kundalini Software
#
# 23-March-2018     Version 1.0     Initial Release
#


import json
import urllib.parse
import urllib.request

def QueryGoogle(course):
    
        print("Querying Google for %s" % course["COURSE_TITLE"])
    
        # create the query string
        SearchString = urllib.parse.quote(course["COURSE_TITLE"])
        
        # grab my google credentials from a file, to make sure I don't accidently upload them
        # to github
        with open('c:\kundalini\keys\google_cs_credentials.txt') as fp:  
            fp.readline()                         # first line is comments    
            GoogleAPIKey = fp.readline().rstrip()
            CX = fp.readline().rstrip()

        URL = 'https://www.googleapis.com/customsearch/v1?q=' + SearchString + '&cx=' + CX + '&key=' + GoogleAPIKey
        
        # make the request
        contents = urllib.request.urlopen(URL).read()

        # parse the returned JSON
        JSON = json.loads(contents)
        course["f"] = (JSON["items"][0]["link"])

print("Reading and parsing course JSON...")
# grab the course data from disk...
with open('Course.JSON') as json_file:  
    data = json.load(json_file)

# and ask google for each URL in tern...
counter = 0
for course in data:
    if  ("GREATCOURSEURL" in course): 
        print("URL already present; skipping course %s" % course["COURSE_TITLE"])
        x = 1  
    else:
        try:
            @QueryGoogle(course)
            print("need to query for %s" % (course["COURSE_TITLE"]))
            counter += 1
        except:
            print("error occurred for course %s" % course["COURSE_TITLE"])    

print("%d total courses processed! " % counter)
    
# dump the output (which will include the Great Course URL!!) back out to disk...
print("dump .JSON back to disk...")
# with open('courseOutput.JSON', 'w') as output_json_file:  
#     json.dump(data, output_json_file, indent=4)
