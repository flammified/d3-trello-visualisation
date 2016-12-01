# D3 project visualiser

This repository contains a bunch of scripts that build a D3 visualisation of a project that is managed using Trello. It is built for a specific project that I was a part of at the University of Applied Sciences Utrecht called R2D2 (Roving Robots and Distributed Devices).

Names and data have been removed from the scripts, just in case people don't want their name attached publicly.

## Usage

### Scraping
To run this visualisation, you need to fill in a few bits of information, so the database can be filled correctly.

First of all, you have to create a mysql database with the layout described in ```source/scraping/tables.txt```.

After this is done, you need to fill in information in the ```source/scraping/scrape_worked_on.py```. . We worked with a few special roles in the project: ```People Managers```, which were the equivalent of HR, ```Architects```, who designed the various parts of the project and ```Project Managers```, who (obviously) managed the projects. These roles can be attributed to people in this file and they get some special colors in the visualisation. We also had a CEO, CTO and CHO,  which can be attributed to people as well. Those roles get ignored in the visualisation, as they were not students, but lecturers.

After this is done, add the information in ```source/scraping/scrape_github_lines.py```. That same file contains a github to trello name conversion table which needs to be filled in.

After that is done, you need to edit ```github/repo.txt``` in the same way as it is in the repo. Then you can run gitAl.sh, which creates a sum.txt file with all lines added and removed. Keep in mind that, because of the way git tracks those metrics, people can get a -lot- of 'wrong' lines accredited to them.

At last you can run ```source/scraping/scrape_github_lines```. This will put the information in the database.

### D3

Now you can run the web visualiser. Fill in the database configuration in ```source/web/app.py``` and run it. You are done!
