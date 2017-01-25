from bs4 import BeautifulSoup
import logging
import re
import html2text

def clean_html(html):
    """
    Copied from NLTK package.
    Remove HTML markup from the given string.

    :param html: the HTML string to be cleaned
    :type html: str
    :rtype: str
    """

    # First we remove inline JavaScript/CSS:
    cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
    # Then we remove html comments. This has to be done before removing regular
    # tags since comments can contain '>' characters.
    cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
    # Next we can remove the remaining tags:
    cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
    # Finally, we deal with whitespace
    cleaned = re.sub(r"&nbsp;", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    return cleaned.strip()

def clean_word(word):
    # no whitespace
    word = word.strip()

    # only lowercase
    word = word.lower()

    return word

def clean_words(list_of_words):
    return [clean_word(word) for word in list_of_words]

def count(list_of_words):
    count = {}
    for word in list_of_words:
        if word not in count.keys():
            count[word] = 1
        else:
            count[word] += 1
    return count

def bag_of_words(document):
    print("Bag of words for",document['url'])
    logging.debug("Bag of words for %s",document['url'])

    text = document['content']
    
    # method 1 (lots of garbage from script and style
    #soup = BeautifulSoup(text,"html.parser")
    #text = soup.get_text()
    #text = clean_html(text)
    #text = html2text.html2text(text)

    # method 2 (html2text seems robuster)
    textmaker = html2text.HTML2Text()
    textmaker.ignore_images = True;
    textmaker.ignore_links = True;
    textmaker.ignore_emphasis = True;
    text = textmaker.handle(text)
    
    # from http://www.nltk.org/book/ch03.html 3.7 Regular Expressions for Tokenizing Text
    wordlist = re.findall(r"\w+(?:[-']\w+)*|'|[-.(]+|\S\w*", text) 

    #todo tokenize: add spaces for 
    words = clean_words(wordlist)
    return count(words)

def superbag(documents):
    superbag = {}
    for document in documents:
        for key in document['bow'].keys():
            if key not in superbag.keys():
                superbag[key] = document['bow'][key]
            else:
                superbag[key] += document['bow'][key]
    return sorted(superbag, key=superbag.get, reverse=True),superbag
