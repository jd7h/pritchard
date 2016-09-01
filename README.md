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
* simple scraper for primary advisories (scraper_adv.py)
* parser for primary advisories (parser_adv.py)
* primary advisories are labeled, which enables supervised learning (parser_adv.py)
* parsed advisories are saved as JSON-object (parser_adv.py)
* scraper for all referenced webpages (scraper_ref.py)
* url-extractor to find all urls present in the advisories (url_extractor.py)
* running scripts in order builds dataset with primary and secondary advisories

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
[judith@loki]$ python3 scraper_refs.py 
Loaded 9363 previously scraped advisories.
Loaded 15207 previously scraped references.
old urls 15207
new urls 0
Scraping references...
Scraping http://technet.microsoft.com/en-us/security/bulletin/ms12-073.mspx ...
Scraping http://lists.opensuse.org/opensuse-security-announce/2015-01/msg00006.html ...
Done scraping.
Scraped: 2
Already visited: 50
```

### Planned functionality
* keyword analysis
* frequency analysis

### Inspiration
Years ago, I had to do a machine learning project at university. I found [this comprehensive blogpost](http://www.drbunsen.org/beer-selection/) by Seth from drbunsen.org. The article contains an analysis of the RateBeer database from 2013. This article (and my data mining project, in which I used the same database) sparked my interest in natural language processing and text analysis with machine learning.

