from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import numpy as np
import re
import gc

def getLinks(url):
    driver.get(url)
    print("fetched URL")
    content = driver.find_elements(By.ID, "mw-content-text")[0]
    body = content.find_elements(By.CLASS_NAME, "mw-parser-output")[0]
    allLinks = body.find_elements(By.TAG_NAME,"a")
    links = []
    print("iterating through",len(allLinks),"links")
    np.random.shuffle(allLinks)
    try:
        i = 0
        for link in allLinks:
            i+=1
            if "/wiki/" in link.get_attribute("href") and not url in link.get_attribute("href") and not ":" in link.get_attribute("href")[6:]and not "#" in link.get_attribute("href") and "ja.wikipedia.org" in link.get_attribute("href") and not link.get_attribute("href") in links:
                links.append(link.get_attribute("href"))
            if i%50 == 0:
                print(i)
            if(i>1000):
                break
    except:
        pass
    return links

def getLines(url):
    driver.get(url)
    print("fetched URL")
    try:
        content = driver.find_elements(By.ID, "mw-content-text")[0]
        body = content.find_elements(By.CLASS_NAME, "mw-parser-output")[0]
    except:
        return []
    children = body.find_elements(By.XPATH,"child::*")
    paragraphs = []
    for child in children:
        if child.tag_name == "p":
            paragraphs.append(child)
    print("collected p elements")
    article = ""
    print("parsing",len(paragraphs),"paragraphs")
    i = 0
    for p in paragraphs:
        i+=1
        if i%10 == 0:
            print(i)
        text = p.get_attribute("innerHTML")
        initialLength = len(text)

        while "<sup" in text:
            length = len(text)
            text = text[0:text.index("<sup")] +text[text.index("</sup>")+6:len(text)]
            if len(text)>length:
                break
            intialLength = len(text)
        if(initialLength < len(text)):
            continue
        
        while "<ruby" in text:
            length = len(text)
            text = text[0:text.index("<ruby")] +text[text.index("</ruby>")+7:len(text)]
            if len(text)>length:
                break
            intialLength = len(text)
        if(initialLength < len(text)):
            continue
        
        while "<a" in text:
            length = len(text)
            after = text[text.index("<a"):len(text)]
            text = text[0:text.index("<a")] + after[after.index(">")+1:len(after)]
            if len(text)>length:
                break
            intialLength = len(text)
        if(initialLength < len(text)):
            continue
        
        while "</a>" in text:
            length = len(text)
            first = text.index("</a>")
            text = text[0:first]+text[first+4:len(text)]
            if len(text)>length:
                break
            intialLength = len(text)
        if(initialLength < len(text)):
            continue
        
        while "<" in text:
            length = len(text)
            first = text.index("<")
            last = text[first:len(text)].index(">") + len(text[0:first])
            if(last <= first):
                break
            text = text[0:first]+text[last+1:len(text)]
            if len(text)>length:
                break
            intialLength = len(text)
        if(initialLength < len(text)):
            continue


        article += text + "。"

    article = article.replace("\n","")
    parse = article.split("。")
    lines = []
    for x in parse:
        if(len(x)>2):
            lines.append(x+"。")
    print("parsed text")
    return lines




randomArticle = "https://ja.wikipedia.org/wiki/%E7%89%B9%E5%88%A5:%E3%81%8A%E3%81%BE%E3%81%8B%E3%81%9B%E8%A1%A8%E7%A4%BA"

op = webdriver.ChromeOptions()
op.add_argument('headless')
driver = webdriver.Chrome(options=op, service=Service(ChromeDriverManager().install()))


maxLinkChecks = 10
used = []
nextArticle = randomArticle
while True:
    gc.collect()
    print("Opening",nextArticle)
    potential = getLinks(nextArticle)
    np.random.shuffle(potential)
    print("Links found:",len(potential))
    print()
    lineMat = []
    largest = 0
    if len(potential) >= maxLinkChecks:
        toCheck = maxLinkChecks
    elif len(potential)>0:
        toCheck = len(potential)
    else:
        print("Found no links. Restarting with random article")
        nextArticle = randomArticle
        continue
    for i in range(toCheck):
        print("Opening",potential[i])
        lineMat.append(getLines(potential[i]))
        if len(lineMat[i]) > len(lineMat[largest]) and not lineMat[i] in used:
            largest = i
        print("Found",len(lineMat[i]),"lines from link",i+1)
    if not lineMat[largest] in used:
        used.append(potential[largest])
        for i in range(len(lineMat[largest])):
            lineMat[largest][i] += "\n"
        file = open("lines.txt", 'a', encoding= "utf-8")
        file.writelines(lineMat[largest])
        file.close()
            
        nextArticle = potential[largest]
    else:
        print("Found no unused links. Restarting with random article")
        nextArticle = randomArticle
        continue
    print()
    print("Most lines from link",largest+1)
    print()
    


