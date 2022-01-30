
from tkinter import W
import AdvancedHTMLParser

import urllib.request

import re


def getSurnames (headers):
    request = urllib.request.Request("https://www.italianames.com/italian-last-names.php", None, headers)
    contents = urllib.request.urlopen(request)
    data = contents.read()

    parser = AdvancedHTMLParser.AdvancedHTMLParser()
    parser.parseStr(data)
    table = parser.getElementsByClassName("pure-table pure-table-striped")

    nodes = table[0].children[1]

    surnames_list = []

    i = 0
    while(i<nodes.childElementCount):
        child = nodes.children[i]
        surname = " ".join(re.findall("[a-zA-Z]+", child.textContent))
        surnames_list.append(surname)
        i = i+1
    
    textfile = open("surnames_list.txt", "w")
    for element in surnames_list:
        textfile.write(element + ("\n"))
    textfile.close()

def getFirstNames(headers):
    links = open("link_list.txt", "r")
    list_of_links = []
    for line in links:
        stripped_line = line.strip()
        list_of_links.append(stripped_line)
    
    names_list = []

    for link in list_of_links:
        request = urllib.request.Request(link, None, headers)
        contents = urllib.request.urlopen(request)
        data = contents.read()

        parser = AdvancedHTMLParser.AdvancedHTMLParser()
        parser.parseStr(data)
        table = parser.getElementsByClassName("pure-table pure-table-striped")

        nodes = table[0].children + table[1].children


        i = 0
        while(i<len(nodes)):
            child = nodes[i]
            name1 = child.children[0].textContent
            name2 = child.children[1].textContent
            if name1 != "&nbsp;":
                names_list.append(name1)
            if name2 != "&nbsp;":
                names_list.append(name2)
            i = i+1

    textfile = open("names_list.txt", "w")
    for element in names_list:
        textfile.write(element + ("\n"))
    textfile.close()

def furniture_name(headers):
    request = urllib.request.Request("https://lar5.com/ikea", None, headers)
    contents = urllib.request.urlopen(request)
    data = contents.read()

    parser = AdvancedHTMLParser.AdvancedHTMLParser()
    parser.parseStr(data)
    table = parser.filter(tagname="div")
    
    furniture_list = []

    for i in range(0,len(table)):
        ch = table[i].childElementCount
        if (ch == 3):
            furniture_list.append(table[i].children[0].innerHTML)

    textfile = open("furniture_name.txt", "w", encoding='utf-8')
    for element in furniture_list:
        textfile.write(element + ("\n"))
    textfile.close()
        

def main():
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,}

    getFirstNames(headers)
    getSurnames(headers)
    furniture_name(headers)

if __name__ == "__main__":
    main()