# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 20:43:12 2023

@author: le279259
"""

###############################################################################
# Web scraping NCAA football data
###############################################################################

#------------------------------------------------------------------------------
# Example from here:
# https://www.geeksforgeeks.org/python-web-scraping-tutorial/
#------------------------------------------------------------------------------

import requests
 
# Making a GET request
r = requests.get('https://www.geeksforgeeks.org/python-programming-language/')
 
# check status code for response received
# success code - 200
print(r)
 
# print content of request
print(r.content)





#------------------------------------------------------------------------------
# Try with NCAA example
#------------------------------------------------------------------------------


# Making a GET request
ncaa_r = requests.get('https://www.sports-reference.com/cfb/boxscores/2021-08-28-fresno-state.html')
 
# check status code for response received
# success code - 200
print(ncaa_r)
 
# print content of request
print(ncaa_r.content)




#------------------------------------------------------------------------------
from bs4 import BeautifulSoup
#------------------------------------------------------------------------------


# Parsing the HTML
soup = BeautifulSoup(ncaa_r.content, 'html.parser')
print(soup.prettify())


 
s = soup.find('div', class_='entry-content')
# content = s.find_all('p')
 
# print(content)



s = soup.find('div', class_='entry-content')
 
# lines = s.find_all('p')
 
# for line in lines:
#     print(line.text)



# find all the anchor tags with "href"
for link in soup.find_all('a'):
    print(link.get('href'))





# for link in soup.find_all('a'):
#     print(link.get('tr'))



#------------------------------------------------------------------------------
# Example from here:
# https://stackoverflow.com/questions/2935658/beautifulsoup-get-the-contents-of-a-specific-table
#------------------------------------------------------------------------------


table = soup.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="scoring") 
rows = table.findAll(lambda tag: tag.name=='tr')


# Split into separate rows:
for row in rows:
    print(row)
    print()


#------------------------------------------------------------------------------
# Example from here:
# https://stackoverflow.com/questions/2010481/how-do-you-get-all-the-rows-from-a-particular-table-using-beautifulsoup
#------------------------------------------------------------------------------

for row in rows:
     cells = row.findChildren('td')
     for cell in cells:
         value = cell.string
         print("The value in this cell is %s" % value)


#------------------------------------------------------------------------------
# Revise to get quarter number:
#------------------------------------------------------------------------------


for row in rows:
     cells = row.findChildren('th')
     for cell in cells:
         value = cell.string
         print("The value in this cell is %s" % value)



#------------------------------------------------------------------------------
# Modify to collect data for a data frame.
#------------------------------------------------------------------------------

import requests

from bs4 import BeautifulSoup

# Module for organizing case data into a data frame.
import pandas as pd



# Make the GET request.
ncaa_r = requests.get('https://www.sports-reference.com/cfb/boxscores/2021-08-28-fresno-state.html')

# check status code for response received
# success code - 200
print(ncaa_r)


# Parse the HTML.
soup = BeautifulSoup(ncaa_r.content, 'html.parser')

# Get the table.
table = soup.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="scoring") 

# Get the rows from the table.
rows = table.findAll(lambda tag: tag.name=='tr')
num_rows = len(rows)





# First row has the table headers, which includes the team names.
row_num = 0
row = rows[row_num]
cells = row.findChildren('th')

# Team 1 is in the 4th element of the header.
team_1_name = cells[4].string
# Team 2 is in the 5th element of the header.
team_2_name = cells[5].string


# Initialize a data frame of scores from one game.
points_sub = pd.DataFrame(columns = 
                      ['quarter', 'time', 
                       'team1', 'team2', 
                       'score1', 'score2'], 
                      index = range(num_rows - 1))



# Loop through the remaining rows to get the data.
for row_num in range(1, num_rows):
    
    # Record the team names.
    points_sub['team1'][row_num - 1] = team_1_name
    points_sub['team2'][row_num - 1] = team_2_name
    
    # Pull the HTML code from this row of the table.
    row = rows[row_num]
    
    # Quarter is in form 'th'.
    cells = row.findChildren('th')
    # Should be only one cell.
    cell = cells[0]
    quarter_num = cell.string
    # print(quarter_num)
    points_sub['quarter'][row_num - 1] = quarter_num
    
    # Remaining entries are in form 'td'.
    
    cells = row.findChildren('td')
    # Time is in cell 0.
    cell = cells[0]
    point_time = cell.string
    points_sub['time'][row_num - 1] = point_time
    
    # Score for team 1 is in cell 3.
    cell = cells[3]
    score1 = cell.string
    points_sub['score1'][row_num - 1] = score1
    
    # Score for team 2 is in cell 4.
    cell = cells[4]
    score2 = cell.string
    points_sub['score2'][row_num - 1] = score2
    
    

#------------------------------------------------------------------------------
# Define a function to get a table of scores
# from an html request.
#------------------------------------------------------------------------------

def get_NCAA_scores_req(html_request):
    
    # Argument is a call to requests.get().
    
    
    # Parse the HTML.
    soup = BeautifulSoup(html_request.content, 'html.parser')
    
    # Get the table.
    table = soup.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="scoring") 
    
    # Get the rows from the table.
    rows = table.findAll(lambda tag: tag.name=='tr')
    # print(rows)
    # print()
    num_rows = len(rows)
    # print(num_rows)
    
    # First row has the table headers, which includes the team names.
    row_num = 0
    row = rows[row_num]
    cells = row.findChildren('th')
    
    # Team 1 is in the 4th element of the header.
    team_1_name = cells[4].string
    # Team 2 is in the 5th element of the header.
    team_2_name = cells[5].string
    
    
    # Initialize a data frame of scores from one game.
    points_sub = pd.DataFrame(columns = 
                          ['quarter', 'time', 
                           'team1', 'team2', 
                           'score1', 'score2'], 
                          index = range(num_rows - 1))
    
    # Loop through the remaining rows to get the data.
    for row_num in range(1, num_rows):
        
        # print(row_num)
        
        # Record the team names.
        points_sub['team1'][row_num - 1] = team_1_name
        points_sub['team2'][row_num - 1] = team_2_name
        
        # Pull the HTML code from this row of the table.
        row = rows[row_num]
        
        # Quarter is in form 'th'.
        cells = row.findChildren('th')
        # Should be only one cell.
        cell = cells[0]
        quarter_num = cell.string
        # print(quarter_num)
        points_sub['quarter'][row_num - 1] = quarter_num
        
        # Remaining entries are in form 'td'.
        
        cells = row.findChildren('td')
        # Time is in cell 0.
        cell = cells[0]
        point_time = cell.string
        points_sub['time'][row_num - 1] = point_time
        
        # Score for team 1 is in cell 3.
        cell = cells[3]
        score1 = cell.string
        points_sub['score1'][row_num - 1] = score1
        
        # Score for team 2 is in cell 4.
        cell = cells[4]
        score2 = cell.string
        points_sub['score2'][row_num - 1] = score2
        
        
    return(points_sub)
    


get_NCAA_scores_req(ncaa_r)


#------------------------------------------------------------------------------
# Define a function to get a table of scores
# from an html file.
#------------------------------------------------------------------------------

def get_NCAA_scores_html(html_file):
    
    # Argument is a call to requests.get().
    
    
    # Parse the HTML.
    soup = BeautifulSoup(html_file, 'html.parser')
    
    # Get the table.
    table = soup.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="scoring") 
    
    # Get the rows from the table.
    rows = table.findAll(lambda tag: tag.name=='tr')
    # print(rows)
    # print()
    num_rows = len(rows)
    # print(num_rows)
    
    # First row has the table headers, which includes the team names.
    row_num = 0
    row = rows[row_num]
    cells = row.findChildren('th')
    
    # Team 1 is in the 4th element of the header.
    team_1_name = cells[4].string
    # Team 2 is in the 5th element of the header.
    team_2_name = cells[5].string
    
    
    # Initialize a data frame of scores from one game.
    points_sub = pd.DataFrame(columns = 
                          ['quarter', 'time', 
                           'team1', 'team2', 
                           'score1', 'score2'], 
                          index = range(num_rows - 1))
    
    # Loop through the remaining rows to get the data.
    for row_num in range(1, num_rows):
        
        # print(row_num)
        
        # Record the team names.
        points_sub['team1'][row_num - 1] = team_1_name
        points_sub['team2'][row_num - 1] = team_2_name
        
        # Pull the HTML code from this row of the table.
        row = rows[row_num]
        
        # Quarter is in form 'th'.
        cells = row.findChildren('th')
        # Should be only one cell.
        cell = cells[0]
        quarter_num = cell.string
        # print(quarter_num)
        points_sub['quarter'][row_num - 1] = quarter_num
        
        # Remaining entries are in form 'td'.
        
        cells = row.findChildren('td')
        # Time is in cell 0.
        cell = cells[0]
        point_time = cell.string
        points_sub['time'][row_num - 1] = point_time
        
        # Score for team 1 is in cell 3.
        cell = cells[3]
        score1 = cell.string
        points_sub['score1'][row_num - 1] = score1
        
        # Score for team 2 is in cell 4.
        cell = cells[4]
        score2 = cell.string
        points_sub['score2'][row_num - 1] = score2
        
        
    return(points_sub)
    





##################################################
##################################################
# Loop over a list of html files to compile a table.
##################################################
##################################################



##################################################
# Import Modules.
##################################################


import os # To set working directory


##################################################
# Set Working Directory.
##################################################

# Find out the current directory.
os.getcwd()
# Change to a new directory.
drive_path = 'C:\\Users\\le279259\\OneDrive - University of Central Florida\\Documents\\'
git_path = 'Research\\NoQuarter\\NCAA_football_quarters\\'
os.chdir(drive_path + git_path + '')
# Check that the change was successful.
os.getcwd()



##################################################
# Set paths for handling files.
##################################################

# Data from games will be stored in a particular folder of html files. 
data_in_folder = 'Research\\NoQuarter\\NCAA_football_quarters\\Data\\WebData\\Games\\' 

# Output will be saved in a folder for regression analysis.
data_out_folder = 'Research\\NoQuarter\\NCAA_football_quarters\\Data\\RegData\\' 





# Making a GET request
ncaa_r = requests.get('https://www.sports-reference.com/cfb/boxscores/2021-08-28-fresno-state.html')


# print content of request
print(ncaa_r.content)

# Save it in an html file.
# Later.


html_file_name = 'view-source_https___www.sports-reference.com_cfb_boxscores_2021-08-28-fresno-state.html'

html_file_path = drive_path + data_in_folder + html_file_name 

file = open(html_file_path, 'r')
html_file_content = file.read()
file.close()
# print(html_file_content)



get_NCAA_scores_html(html_file_content)



#------------------------------------------------------------------------------
# Loop over a list of html files to compile a table.
#------------------------------------------------------------------------------


html_file_names = ['view-sourcehttpswww.sports-reference.comcfbboxscores2021-08-28-fresno-state.html', 
                   'view-sourcehttpswww.sports-reference.comcfbboxscores2021-08-28-illinois.html', 
                   'view-sourcehttpswww.sports-reference.comcfbboxscores2021-08-28-san-jose-state.html', 
                   'view-sourcehttpswww.sports-reference.comcfbboxscores2021-08-28-new-mexico-state.html', 
                   'view-source:https://www.sports-reference.com/cfb/boxscores/2021-08-28-ucla.html']

html_prefix = 'view-sourcehttpswww.sports-reference.comcfbboxscores'

game_dates_and_teams = [['2021-08-28', 'fresno-state'], 
                        ['2021-08-28', 'illinois'], 
                        ['2021-08-28', 'san-jose-state'], 
                        ['2021-08-28', 'new-mexico-state'], 
                        ['2021-08-28', 'ucla']]


# Initialize a data frame of scores from these games.
points_full = pd.DataFrame(columns = 
                      ['quarter', 'time', 
                       'team1', 'team2', 
                       'score1', 'score2', 
                       'date', 'home_team'])


for game_num in range(len(game_dates_and_teams)):
    
    game = game_dates_and_teams[game_num]
    game_date = game[0]
    game_home_team = game[1]
    
    # Get path to html file.
    # print(html_prefix + game[0] + '-' + game[1] + '.html')
    html_file_name = html_prefix + game_date + '-' + game_home_team + '.html'
    html_file_path = drive_path + data_in_folder + html_file_name 
    
    # Get contents of file.
    file = open(html_file_path, 'r')
    html_file_content = file.read()
    file.close()
    
    # Get table of results from this file.
    points_sub = get_NCAA_scores_html(html_file_content)
    
    # Append the date that the game was held.
    points_sub['date'] = game_date
    
    # Append the date that the home team field where the game took place.
    points_sub['home_team'] = game_home_team
    
    # Append into the full dataset. 
    points_full = points_full.append(points_sub)





points_full







###############################################################################
# End
###############################################################################
