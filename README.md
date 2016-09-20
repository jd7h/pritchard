# pritchard
Data mining on public security advisories.

### Etymology
This repository was named after [Francis Pritchard](http://deusex.wikia.com/wiki/Francis_Pritchard), the snarky head of Security from Deux Ex: Human Revolution.

### Goal
I want to find out whether we can successfully assign 
an impact score to a security advisory, 
based on the occurence of certain keywords in the document
and similarity to earlier advisories. 

### Implemented functionality
* Building the dataset
  * simple scraper for primary advisories (scraper_adv.py)
  * parser for primary advisories (parser_adv.py)
  * primary advisories are labeled, which enables supervised learning (parser_adv.py)
  * parsed advisories are saved as JSON-object (parser_adv.py)
  * scraper for all referenced webpages (scraper_ref.py)
  * url-extractor to find all urls present in the advisories (url_extractor.py)
  * error-logging
  * small module for loading and dumping datasets
* Exploring the dataset
  * Small report of url statuses (reference_report.py)

```
[jd7h@reinaert]$ cat urls.txt | cut -d'/' -f3 | sort | uniq -c | sort -nr | head 
     65 cve.mitre.org
     40 lists.fedoraproject.org
     34 lists.opensuse.org
     20 www-01.ibm.com
     19 www.vuxml.org
     19 www.ubuntu.com
     15 lists.centos.org
     14 www.debian.org
     14 rhn.redhat.com
     12 www.phpmyadmin.net
```

```
2016-09-20 17:35:32,711 INFO:------------ SCRAPER REFS -----------------
2016-09-20 17:35:32,712 INFO:Building data set.
2016-09-20 17:35:32,847 INFO:Loaded 9363 previously scraped advisories
2016-09-20 17:35:32,847 INFO:Opening ../data/references_*.json
2016-09-20 17:35:32,848 INFO:Loaded 0 previously scraped references
2016-09-20 17:35:35,484 INFO:0 old urls from datasets in ../data/references_*.json
2016-09-20 17:35:35,484 INFO:15207 new urls from advisories in primary_advisories.json
2016-09-20 17:35:35,495 INFO:Start scraping phase.
2016-09-20 17:35:35,495 INFO:Scraping references...
2016-09-20 17:35:35,495 INFO:Scraping http://lists.centos.org/pipermail/centos-announce/2013-February/019230.html ...
2016-09-20 17:35:45,952 INFO:Scraping https://blogs.oracle.com/sunsecurity/entry/cve_2012_2337_restriction_bypass ...
2016-09-20 17:35:49,899 INFO:Scraping http://www.ubuntu.com/usn/usn-3055-1/ ...
(...)
2016-09-20 17:36:17,398 INFO:Dumping 10 new results to backup.
(...)
2016-09-20 17:36:23,799 INFO:Dumped data to 15 files
```

### Planned functionality
* reference-page HTML parsing
* bag of words representation for references
* linking the advisories and the references
* keyword analysis
* frequency analysis

### Inspiration
Years ago, I had to do a machine learning project at university. I found [this comprehensive blogpost](http://www.drbunsen.org/beer-selection/) by Seth from drbunsen.org. The article contains an analysis of the RateBeer database from 2013. This article (and my data mining project, in which I used the same database) sparked my interest in natural language processing and text analysis with machine learning.

