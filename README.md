# NCAA_football_quarters
An analysis of scoring patterns in the fourth quarter of college football games.


## Data

The points totals within the games are available on the following pages, 
found within the webpage of the [College Football](https://www.sports-reference.com/cfb/) (CFB) section 
of 
[Sports Reference](https://www.sports-reference.com/cfb/).

The link to the data within a particular game is on the following page.
[Pinstripe Bowl - Maryland vs Virginia Tech Box Score, December 29, 2021](https://www.sports-reference.com/cfb/boxscores/2021-12-29-virginia-tech.html)


The links to all games in the 2021 season are available here:

[2021 College Football Schedule and Results](https://www.sports-reference.com/cfb/years/2021-schedule.html)


The links to each year of data are collected here:

[College Football National Champions and Seasons](https://www.sports-reference.com/cfb/years/)


The portal to abtain statistics from the database is through
[Stathead](https://stathead.com/) by Sports Reference.


## Data Collection 


The data were scraped from the html files from pages for each game. 
Some examples are available in the
[Games](https://github.com/LeeMorinUCF/NCAA_football_quarters/tree/main/Data/WebData/Games/2022) folder in the Data folder.


The Web-scraping procedure uses the 
[Beautiful Soup](https://www.tutorialspoint.com/beautiful_soup) module.

Some pages I found useful to get started are the 
[Kinds of Objects](https://www.tutorialspoint.com/beautiful_soup/beautiful_soup_kinds_of_objects.htm)
and, when getting down to business, the
[Souping the Page](https://www.tutorialspoint.com/beautiful_soup/beautiful_soup_souping_the_page.htm). 

After getting rolling and increasing the scale, however, 
one is usually met by roadblocks including the error message
```HTTPError: Too Many Requests```, 
in the ```urllib``` module, 
indicating that the server is blocking our access after
too many requests for webpages. 
The problem is described on the 
[Real Python](https://realpython.com) page
[Python's urllib.request for HTTP Requests](https://realpython.com/urllib-request/#common-urllibrequest-troubles)
and on [stackoverflow](https://stackoverflow.com) in
[this post](https://stackoverflow.com/questions/67418024/how-to-fix-urllib-error-httperror-http-error-429-too-many-requests)
and [this other post](https://stackoverflow.com/questions/50444977/urllib-error-too-many-requests). 

I had to switch to another research problem but I will pick this up 
where I left off later.
