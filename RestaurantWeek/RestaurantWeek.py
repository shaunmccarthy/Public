# A nice simple python script for downloading the Yelp ratings for 
# all the restaurants in restaurant week this year
from urllib import urlopen
import re
import time


# How to identify a restaurant on the restaurant week page
patFinderRestaurants = re.compile("class=\"listingTitle\">(.*?)</a>");

# How to find the rating for the first result on Yelp that matches the title
# passed in to search
patYelpSearchFirstRating = re.compile("<i class=\"star-img stars_.*?\" title=\"(.*?)\">")
#patYelpSearchResult = re.compile("<span class=\"indexed-biz-name\">1\. \t<a class=\"biz-name\" href=\"(.*?)\"")

# Download the webpage listing all the restaurant week pages
webpage = urlopen('http://www.nycgo.com/restaurantweek').read()

# Create a list of all the restaurants

# Find all the restaurants
findRestaurants = re.findall(patFinderRestaurants,webpage)

# a file to write the results out to
f = open('C:\\temp\\rweek.csv', 'w')

# Uncomment to override results to just one restaurant for debugging
#findRestaurants = ["Tulsi"];

# Cycle through the restaurants, searching for them on yelp and getting their
# ratings
for restaurant in findRestaurants:
    # Search for the restaurant on Yelp
    searchResults = urlopen('http://www.yelp.com/search?find_desc=' + restaurant + '&find_loc=new+york%2C+ny&ns=1').read()

    # Find the rating in the result
    ratings = re.findall(patYelpSearchFirstRating, searchResults)

    # If we found a rating, write it out to the file
    if (len(ratings) >= 1):
        f.write("\"" + restaurant + "\"'" + ratings[0] + "\n")
        print restaurant + "\t" + ratings[0]
    else:
        print "Unable to find " + restaurant
        continue

    # Wait 5 seconds so we don't get tagged as a script
    time.sleep(5)

f.close()
raw_input("Done")