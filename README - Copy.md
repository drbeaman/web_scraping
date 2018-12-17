# README - Explained
To see the original assignment instructions, see the README file. Relevant files include:
1. mission_to_mars.ipynb file gives step-by-step instructions for how to scrape data.  This file served as my "scratch paper" to see immediate scraping results during development.  Results from this file are copy/pasted into the scrape_mars.py file.  
2. scrape_mars.py file runs the scrape, storing results into singular dictionary.
3. app.py file runs the Flask app which has two primary functions:
    a. Send the scraped data dictionary to MongoDB, where it is stored in a database/collection called 'mars_app_db' / 'collection'.
    b. Pass the scraped results into the index.html file home page.
4. templates\index.html file uses bootstrap to render the results.
5. styes.css file stores basic styles of the html file.
6. chromedriver.exe is necessary when using the Chrome browser for scraping.  Must be located in same folder as the scrape_mars.py, app.py files.