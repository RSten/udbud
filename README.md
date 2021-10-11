# Udbudsspider
This is a scrapy spider built for scraping www.udbud.dk - the website for public tenders in Denmark. 


## Requirements
Udbudsspider is built with Python 3.9 only dependent on the scrapy library. Hence the setup is as easy as it gets from a Python point of view.
You need to install scrapy via pip:

```
pip install scrapy
```

Afterwards you run the udbudsspider using scrapy command:

```
scrapy crawl udbud -O output_file.jl
```

Here we use the "-O" tag to define the output file. In this case a jsonlines file. 