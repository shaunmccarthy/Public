# To Get Netflix Ratings:
#var jq = document.createElement('script');
#jq.src = "//ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js";
#document.getElementsByTagName('head')[0].appendChild(jq);// ... give time for script to load, then type.
#jQuery.noConflict();
#$(".cell-title a").each(function(i,val) { console.log($(val).text() +'\t' + $(val).parent().parent().parent().find(".sbmfrt").text().replace('You rated this movie: ','').trim()) });

# A script that imports a CSV file of movie ratings and sets them on 
# IMDB
import re
import csv
import cookielib
import urllib
import urllib2
import sys


# Install this module by: pip install requests
# See http://stackoverflow.com/questions/4750806/how-to-install-pip-on-windows
import requests

site = "http://www.imdb.com"

# The path to the cookies text (populate with https://chrome.google.com/webstore/detail/cookietxt-export/lopabhfecdfhgogdbojmaicoicjekelh/related?hl=en after logging in)
cj = cookielib.MozillaCookieJar('cookies.txt')
cj.load()

def setRating(movie, rating):
    # Url pattern
    searchUrl = site + "/find?q=" + movie + "&s=tt&exact=true"
    print "Searching page for '" + movie + "': " + searchUrl
    searchResults = requests.get(searchUrl, cookies=cj).text

    # Open the first result
    firstResult = re.search("<a href=\"/title/(.*?)/", searchResults)

    if (firstResult):
        # open the page
        movieUrl = site + "/title/" + firstResult.group(1) + "/"
        print "Downloading page for '" + movie + "': " + movieUrl
        moviePage = requests.get(movieUrl, cookies=cj).text 

        # assert that we are logged in
        loggedIn = re.search("Shaun McCarthy", moviePage, re.IGNORECASE)
        if (not loggedIn):
            print "Cookie didn't log you in"
            sys.exit(0)

        # Check to see if we have already rated this movie
        currentRating = re.search("<span class=\"value\">(.*?)</span>", moviePage, re.IGNORECASE)
        if (not currentRating):
            print "Couldn't find rating for '" + movie + "'"
            return

        if (currentRating.group(1) <> '-'):
            print "'" + movie + "' already has a rating: " + currentRating.group(1)
            return

        # find the data-auth value
        dataAuth = re.search("data-auth=\"(.*?)\"", moviePage)

        ratingData = {'auth':dataAuth.group(1).encode('ascii','ignore'), 'tconst': firstResult.group(1).encode('ascii','ignore'), 'rating': rating, 'tracking_tag': 'title-maindetails'}

        ratingResult = requests.post(site + '/ratings/_ajax/title', data=ratingData, cookies=cj).text

        if (ratingResult != "{\"status\":200}"):
            print "Unexpected result for rating of movie '" + movie + "':\n" + ratingResult
            return

        print "Successfully rated '" + movie+ "': " + str(rating)
        #data-auth="



# Read in the IMDB ratings to populate
with open('ratings.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        # Search IMDB for the movie
        setRating(row[0], row[2])

raw_input("Done")
sys.exit(0)
