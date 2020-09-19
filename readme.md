# This is a Website Scrapper
This scrapper scrap information from [newskillsacademy](https://newskillsacademy.co.uk/) all course information with category. And create directory based on category and save course info in file where file name is course title.
For any python programmer this is nice scrapping tools for get some knowladege about scraping website.

# Installation process for windows
Use python version: Python 3.8.2
```
virtualenv scraper-env
source scraper-env/bin/activate
pip install requirements.txt
python scraper.py
```

# Usages
Enter url:https://newskillsacademy.co.uk/
after input url then this scraper automatically create directory and file one by one and save all course information in file.This scraper take some time for get all info and save.If you reduce execution time then you use threading.
# In future
I will add threading  and  infinit scrolling page scraping feature.
