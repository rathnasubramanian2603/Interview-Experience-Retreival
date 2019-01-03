import requests, io, os, json
from BeautifulSoup import BeautifulSoup

main_url = "https://www.geeksforgeeks.org/category/interview-experiences/"
page_urls = set()
count = 0

def mainPages(urls):
    filePath = "documents/"
    extension = ".json"
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    jsonData = dict()
    for url in urls:
        jsonData = {"title":"","company":"","content":"","url":url}
        response = requests.get(url)
        page = BeautifulSoup(response.content)
        text = ""
        fileName = ""
        for title in page.findAll("meta",{"property":"og:title"}):
            if not(jsonData['title']):
                jsonData['title'] = title['content'].split(" - GeeksforGeeks")[0].encode('utf-8')
        for company in page.findAll("meta",{"property":"article:tag"}):
            if not(jsonData['company']) and (company['content']!='On-Campus'):
                jsonData['company'] = company['content'].encode('utf-8')
        for content in page.findAll("div",{"class": "entry-content"}):
            text = " ".join(" ".join(terms.strip() for terms in content.findAll(text=True)).split())
            text = " ".join((text.split("Write your Interview Experience or mail it to contribute@geeksforgeeks.org")[0]).split("post_top_responsive (adsbygoogle = window.adsbygoogle || []).push({});"))
        jsonData['content'] = text.encode('utf-8')
        fileName = url.split("/")[3]
        with open(filePath+fileName+extension,'w+') as docFile:
            json.dump(jsonData,docFile)

def urlFileWrite(urls):
    urlFile = open("urlFile.txt",'a+')
    for url in urls:
        urlFile.write(url)
        urlFile.write("\n")
    urlFile.close()

def urlCheck():
    global page_urls
    try:
        urlFile = open("urlFile.txt",'r')
        page_url = set()
        for line in urlFile:
            page_url.add(line)
        urlFile.close()
        if page_url == page_urls:
            mainPages(page_urls)
        else:
            urlFileWrite(page_urls.difference(page_url))
            mainPages(page_urls.difference(page_url))
    except IOError:
        urlFileWrite(page_urls)
        mainPages(page_urls)

def urlPages(url):
    global page_urls, count
    response = requests.get(url)
    page = BeautifulSoup(response.content)
    for span in page.findAll("span",{"class": "read-more"}):
        for url in span.findAll("a"):
            page_urls.add(str(url['href']))
    nextUrl = ""
    for url in page.findAll("a",{"class": "nextpostslink"}):
        nextUrl = str(url['href'])
        count += 1
    if count<10:
        urlPages(nextUrl)

def main():
    global main_url
    urlPages(main_url)
    urlCheck()
    
if __name__ == "__main__":
    main()
