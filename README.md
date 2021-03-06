# pritchard
Data mining on public security advisories.

### Etymology
This repository was named after [Francis Pritchard](http://deusex.wikia.com/wiki/Francis_Pritchard), the snarky head of Security from Deux Ex: Human Revolution.

### Goal
I want to find out whether we can successfully assign 
an impact score to a security advisory, 
based on the occurence of certain keywords in the document
and similarity to earlier advisories. 

### Todo
* All code through pylint
* Remove all references to json
* Remove deprecated functions
* Re-run bag-of-words on references with new nltk tokenizer

### Implemented functionality
* Building the dataset
  * simple scraper for primary advisories with logging (scraper_adv.py)
  * parser for primary advisories with logging (parser_adv.py)
  * primary advisories are labeled, which enables supervised learning (parser_adv.py)
  * parsed advisories are saved as JSON-object (parser_adv.py)
  * scraper for all referenced webpages (scraper_ref.py)
  * url-extractor to find all urls present in the advisories (url_extractor.py)
  * error-logging
  * small module for loading and dumping datasets
* Exploring the dataset
  * Small report of url statuses (reference_report.py)
  * bag of words representation for references
* Preprocessing
  * Unscraped references are removed
  * Calculating the most significant keywords for each rating (bin)

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

### Planned functionality
* Keyword selection
* Classifier based on the n most significant keywords

### Inspiration
Years ago, I had to do a machine learning project at university. I found [this comprehensive blogpost](http://www.drbunsen.org/beer-selection/) by Seth from drbunsen.org. The article contains an analysis of the RateBeer database from 2013. This article (and my data mining project, in which I used the same database) sparked my interest in natural language processing and text analysis with machine learning.

