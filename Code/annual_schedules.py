# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 06:47:50 2023

@author: le279259
"""




#------------------------------------------------------------------------------
# Basic version, which fails at certification.
#------------------------------------------------------------------------------

# Sample code.
import urllib.request

opener = urllib.request.FancyURLopener({})
url = "http://stackoverflow.com/"
f = opener.open(url)
content = f.read()
# OSError: [Errno socket error] [Errno socket error] [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: certificate has expired (_ssl.c:1123)



#------------------------------------------------------------------------------
# Version that gets around certificate issue.
#------------------------------------------------------------------------------



# Solution from here:
# https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error.
import urllib.request as urlrq
import certifi
import ssl

url = "http://stackoverflow.com/"
resp = urlrq.urlopen(url, context=ssl.create_default_context(cafile=certifi.where()))


print(resp)





# Another example to get at the contents of the response object:
# https://stackoverflow.com/questions/6591801/how-do-i-get-inside-python-http-client-httpresponse-objects#:~:text=The%20function%20HTTPresponse.read%20%28%29%20reads%20the%20http.client.HTTPResponse%20object,response%20%3D%20urllib.request.urlopen%20%28some_request%29%20body%20%3D%20response.read%20%28%29
url = "http://stackoverflow.com/"
response_object = urlrq.urlopen(url, context=ssl.create_default_context(cafile=certifi.where()))

# Print the contents line by line 
for line in response_object:
    print(line)



# Try again with the NCAA football schedule for one year.
url = 'https://www.sports-reference.com/cfb/years/2021-schedule.html'
response_object = urlrq.urlopen(url, context=ssl.create_default_context(cafile=certifi.where()))

# Print the contents line by line 
for line in response_object:
    print(line)



#------------------------------------------------------------------------------
# Read an html file and write it to a file.
#------------------------------------------------------------------------------



import os
# Find out the current directory.
os.getcwd()
# Change to a new directory.
drive_path = 'C:\\Users\\le279259\\OneDrive - University of Central Florida\\Documents\\'
git_path = 'Research\\NoQuarter\\NCAA_football_quarters\\'
os.chdir(drive_path + git_path + '')
# Check that the change was successful.
os.getcwd()

# Output will be saved in a folder for regression analysis.
data_schedule_folder = 'Research\\NoQuarter\\NCAA_football_quarters\\Data\\WebData\\Schedules\\' 

# Set path to file for schedule.
schedule_file_name = '2021-schedule.html'
schedule_file_path = drive_path + data_schedule_folder + schedule_file_name 


# Read the NCAA football schedule for one year.
url = 'https://www.sports-reference.com/cfb/years/2021-schedule.html'
response_object = urlrq.urlopen(url, context=ssl.create_default_context(cafile=certifi.where()))



with open(schedule_file_path, 'wb') as output_file:
    for line in response_object:
        output_file.write(line)



# Print the contents line by line 
for line in response_object:
    print(line)



#------------------------------------------------------------------------------
# Loop over years to obtain all the schedules.
#------------------------------------------------------------------------------

# year_list = range(2022, 2010, -1)
year_list = range(2010, 1990, -1)

for year in year_list:
    
    # Set the url for the schedule.
    url = 'https://www.sports-reference.com/cfb/years/' + str(year) + '-schedule.html'
    
    # Read the NCAA football schedule for this year.
    response_object = urlrq.urlopen(url, context=ssl.create_default_context(cafile=certifi.where()))
        
    # Set path to file for schedule.
    schedule_file_name = str(year) + '-schedule.html'
    schedule_file_path = drive_path + data_schedule_folder + schedule_file_name 
    
    
    # Write to an html file on the hard drive.
    with open(schedule_file_path, 'wb') as output_file:
        for line in response_object:
            output_file.write(line)




#------------------------------------------------------------------------------
# Parsing game-specific pages.
#------------------------------------------------------------------------------

# Look for strings of the form
# href="/cfb/boxscores/2019-08-29-bowling-green-state.html"
# or
# <a href="/cfb/boxscores/1991-08-28-georgia-tech.html">



#------------------------------------------------------------------------------
# Get the hrefs from a single page.
#------------------------------------------------------------------------------

year = 2022

# Set path to html file for schedule.
schedule_file_name = str(year) + '-schedule.html'
schedule_file_path = drive_path + data_schedule_folder + schedule_file_name 


# Get the contents of the html file.
file = open(schedule_file_path, 'r')
schedule_file_content = file.read()
file.close()


# Get the hyperlinks for the games.
from bs4 import BeautifulSoup


# Parse the HTML.
soup = BeautifulSoup(schedule_file_content, 'html.parser')



# Find all the anchor tags with "href"
# Then extract the ones relating to scores in each game.
max_game_count = 1000
game_count = 0
for link in soup.find_all('a'):
    
    # Get text of address.
    # print(link.get('href'))
    url_text = link.get('href')
    
    # Get address pertaining to a game.
    # Contains the string "boxscores" 
    # and the date, which might be in the next year.
    if ('boxscores' in url_text 
        and (str(year)in url_text
             or str(year + 1)in url_text)
        and game_count <= max_game_count):
        game_count = game_count + 1
        print(url_text)
    


#------------------------------------------------------------------------------
# Get addresses for all games in the annual scedules.
#------------------------------------------------------------------------------



import pandas as pd


# Initialize a data frame of scores from these games.
game_links_full = pd.DataFrame(columns = 
                      ['year', 'url_suffix'])


# year_list = range(2022, 2020, -1)
year_list = range(2022, 1990, -1)


for year in year_list:
    
    print("Collecting links for games in " + str(year) + ".")
    
    # Set path to html file for schedule.
    schedule_file_name = str(year) + '-schedule.html'
    schedule_file_path = drive_path + data_schedule_folder + schedule_file_name 
    
    
    # Get the contents of the html file.
    file = open(schedule_file_path, 'r')
    schedule_file_content = file.read()
    file.close()
    
    
    # Parse the HTML.
    soup = BeautifulSoup(schedule_file_content, 'html.parser')
    
    # Initialize a data frame of links for the games in this year.
    max_game_count = 1000
    game_count = 0
    game_links_sub = pd.DataFrame(columns = 
                          ['year', 'url_suffix'], 
                          index = range(max_game_count))
    
    
    # Find all the anchor tags with "href"
    # Then extract the ones relating to scores in each game.
    row_num = 0
    for link in soup.find_all('a'):
        
        # Get text of address.
        url_text = link.get('href')
        
        # Get address pertaining to a game.
        # Contains the string "boxscores" 
        # and the date, which might be in the next year.
        if ('boxscores' in url_text 
            and (str(year)in url_text
                 or str(year + 1)in url_text)
            and game_count <= max_game_count):
            game_count = game_count + 1
            
            # Record the addresses in the data frame.
            # print(url_text)
            game_links_sub['url_suffix'][row_num] = url_text
            row_num = row_num + 1
            
    # Append the year that the game was held.
    game_links_sub['year'] = year

    # Append nonempty rows into the full dataset. 
    game_links_full = game_links_full.append(game_links_sub[0:game_count])


game_links_sub.columns
game_links_sub.describe()
game_links_sub.value_counts()

len(game_links_sub)





game_links_full.columns
game_links_full.describe()

len(game_links_full)


game_links_full[0:10]



game_links_full.value_counts()




# Set path to csv file for links in schedule.
game_links_file_name = 'game_links.csv'
schedule_file_path = drive_path + data_schedule_folder + game_links_file_name 

game_links_full.to_csv(schedule_file_path)




#------------------------------------------------------------------------------
# Loop over years to obtain all the games in each of the schedules.
#------------------------------------------------------------------------------

# First attempt:
# After about 30 files.
# HTTPError: Too Many Requests

# Get some sleep in between requests.
import time
import random

for i in range(10):
    
    seconds_of_sleep = random.lognormvariate(mu = 0.3, sigma = 0.5)
    print("Sleeping for " + str(seconds_of_sleep) + " seconds.")
    
    time.sleep(seconds_of_sleep)
    print(i)




# Output will be saved in a folder for regression analysis.
data_game_folder = 'Research\\NoQuarter\\NCAA_football_quarters\\Data\\WebData\\Games\\' 


# Set path to html files for games.
game_file_name = str(year) + '-schedule.html'
game_file_path = drive_path + data_schedule_folder + game_file_name 


# year_list = range(2022, 2010, -1)
# year_list = range(2010, 1990, -1)
year_list = range(2022, 2021, -1)

# year = 2022
for year in year_list:
    
    
    # Get the subset of games for the year.
    game_links_year = game_links_full['url_suffix'][game_links_full['year'] == year]
    
    
    # Loop over the games in a season.
    # game_num = 0
    for game_num in range(len(game_links_year)):
        
        game_link = game_links_year[game_num]
            
        
        # Set the url for the schedule.
        url = 'https://www.sports-reference.com' + game_link
        
        # Get some sleep in between requests.
        seconds_of_sleep = random.lognormvariate(mu = 0.3, sigma = 0.5)
        time.sleep(seconds_of_sleep)
        
        
        # Read the NCAA football scores for this game.
        response_object = urlrq.urlopen(url, context = ssl.create_default_context(cafile = certifi.where()))
            
        
        # Set path to file for game.
        data_game_folder_yr = data_game_folder + str(year) + '\\'
        game_file_name = game_link.replace('/cfb/boxscores/', '')
        game_file_path = drive_path + data_game_folder_yr + game_file_name 
        
        
        # Write to an html file on the hard drive.
        with open(game_file_path, 'wb') as output_file:
            for line in response_object:
                output_file.write(line)





