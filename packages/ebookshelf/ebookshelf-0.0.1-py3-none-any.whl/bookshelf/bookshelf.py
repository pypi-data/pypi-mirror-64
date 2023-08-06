#! /usr/bin/python3
import xml.etree.ElementTree as ET
import xml.etree.cElementTree as SVG
import random
import hashlib
from math import sqrt
   
class Book:

    maxPages=0
    
    def __init__(self, booknode):
        self.publisher="None"
        self.series="None"
        self.authors=[]
        for el in booknode:
            if el.tag == "_genre":
                self.genre = el.text
            elif el.tag =="_seiten":
                self.pages = int(el.text)
                if self.pages > Book.maxPages:
                    Book.maxPages= self.pages
            elif el.tag =="_worte":
                if el.text=="None":
                    self.words=0
                else:    
                    self.words = int(el.text)
            elif el.tag =="id":
                self.bookId = el.text
            elif el.tag =="uuid":
                self.uuid = el.text
            elif el.tag =="size":
                self.size = int(el.text)
            elif el.tag =="title":
                self.title = el.text
            elif el.tag =="library_name":
                self.library = el.text
            elif el.tag =="timestamp":
                self.timestamp = el.text
            elif el.tag =="pubdate":
                self.pubdate = el.text
            elif el.tag =="publisher":
                self.publisher = el.text
            elif el.tag =="isbn":
                self.isbn = el.text
            elif el.tag =="rating":
                self.rating = el.text
            elif el.tag =="series":
                self.series = el.text
            elif el.tag =="comments":
                self.comments = el.text
            elif el.tag =="cover":
                self.cover = el.text
            elif el.tag =="identifiers":
                self.identifiers = el.text
            elif el.tag =="tags":
                self.tags=[]
            elif el.tag =="formats":
                self.formats=[]
                for format in el:
                    self.formats.append(format.text)
                    print(format.text)
            elif el.tag =="authors":
                for author in el:
                    self.authors.append(author.text)
            else:
                print(el.tag)

    def shelfspace(self):
        return sqrt(1-(1-(self.pages/Book.maxPages) ** 2)) * 90 + 10

    def draw(self,svg, bottom, position):
        hex = hashlib.md5(self.publisher.encode()).hexdigest() 
        h=int(int("0x"+str(hex)[-2:],16)/2)
        col = "#" + str(hex)[-6:]
        pubcol = "#" + str(hex)[-8:-2]
        hex = hashlib.md5(self.series.encode()).hexdigest() 
        sercol = "#" + str(hex)[-8:-2]
        link= SVG.SubElement(svg,"a")
        link.set("href", self.formats[0])
        link.set("type","application/epub+zip")
        linktitle = SVG.SubElement(link, "title")
        linktitle.text= self.title
        book = SVG.SubElement(link, "rect", fill=col, stroke="black",  x=str(position), y=str(bottom-192-h), width=str(self.shelfspace()), height=str(192+h))
        book.set("stroke-width", "0.5")
        publisher = SVG.SubElement(link, "rect", fill=pubcol, stroke="black",  x=str(position), y=str(bottom-16), width=str(self.shelfspace()), height=str(16))
        publisher.set("stroke-width", "0.5")
        series = SVG.SubElement(link, "rect", fill=sercol, stroke="black",  x=str(position), y=str(bottom-192-h), width=str(self.shelfspace()), height=str(16))
        series.set("stroke-width", "0.5")
        title = SVG.SubElement(link, "text",  x=str(position+self.shelfspace()/2+4), y=str(bottom-170-h))
        title.set("stroke-width", "0.5")
        title.set("transform", "rotate(-90 "+str(position+self.shelfspace()/2+4) +" "+str(bottom-170-h)+")")
        title.set("stroke", "white")
        title.set("text-anchor","end")
        title.set("font-family","Arial")
        title.set("font-size","10")
        title.set("fill", "white")
        title.text= self.title[:30]
        author = SVG.SubElement(link, "text",  x=str(position+self.shelfspace()/2+4), y=str(bottom-16))
        author.set("stroke-width", "0.5")
        author.set("transform", "rotate(-90 "+str(position+self.shelfspace()/2+4) +" "+str(bottom-16)+")")
        author.set("stroke", "white")
        author.set("text-anchor","start")
        author.set("font-family","Arial")
        author.set("font-size","5")
        author.set("fill", "white")
        author.text= self.authors[0][:30]
        
    
class Shelf:
    maxSpace=1000

    def __init__(self):
        self.space=0
        self.books = []
        print("New Shelf")

    def add(self,book):
        if book.shelfspace() + self.space > self.maxSpace:
            return False
        else:
            self.books.append(book)
            self.space = self.space + book.shelfspace()
            return True

    def draw(self,svg, left, position):
        top = 500+330*position
        self.bookIndex=0
        SVG.SubElement(svg, "rect", fill="brown", stroke="#000", x=str(left), y=str(top), width="1000", height="10")
        self.bookIndex=0
        for book in self.books:
            book.draw(svg,top, left + self.bookIndex)
            self.bookIndex += book.shelfspace()

class Case:
    maxSpace=6
    def __init__(self):
        self.space=0
        self.shelfs = []
        self.space = 0
        print("New Case")

    def add(self,shelf):
        if self.space + 1 > self.maxSpace:
            return False
        else:
            self.shelfs.append(shelf)
            self.space = self.space +1
            print("Shelf added", len(self.shelfs))
            return True

    def draw(self,svg, position):
        left = position *1050
        SVG.SubElement(svg, "rect", fill="brown", stroke="#000", x=str(left), y="500", width="50", height="2000")
        SVG.SubElement(svg, "rect", fill="brown", stroke="#000", x=str(left + 1050), y="500", width="50", height="2000")
        SVG.SubElement(svg, "rect", fill="brown", stroke="#000", x=str(left + 50), y="500", width="1000", height="10")
        self.shelfIndex=0
        left+=50
        self.shelfIndex = 0
        for shelf in self.shelfs:
            self.shelfIndex += 1
            shelf.draw(svg,left,self.shelfIndex)
    
class Library:
    cases=[]
    case = None
    shelf = None
    
    def add(self,book):
        if self.shelf == None:
            self.shelf=Shelf()
        if self.case == None:
            self.case =Case()
        if not self.shelf.add(book):
            if not self.case.add(self.shelf):
                self.cases.append(self.case)
                self.case=Case()
                self.case.add(self.shelf)
            self.shelf=Shelf()
            self.shelf.add(book)

    def caseCount(self):
        return len(self.cases)

    def finalize(self):
        if not self.case.add(self.shelf):
            self.cases.append(self.case)
            self.case=Case()
            self.case.add(self.shelf)
        self.cases.append(self.case)
        print(len(self.cases))

    def draw(self):
        svg=SVG.Element("svg",xmlns="http://www.w3.org/2000/svg" ,id="Calibre Bookshelf",version="2.0" ,width=str(1050*(len(self.cases)+1)+50) ,height="3000")
#        svg.set("xmlns:xlink","http://www.w3.org/1999/xlink")
        caseIndex=0
        for case in self.cases:
            print(len(case.shelfs),"draw")
            case.draw(svg,caseIndex)
            caseIndex += 1
        






        tree=SVG.ElementTree(svg)
        tree.write("test.svg")
    
        

def main():
    books=[]
    tree = ET.parse('MyBooks.xml')
    for record in tree.getroot():
       books.append(Book(record))

    library=Library()
    for book in books:
        library.add(book)
    library.finalize()
    
    library.draw()
    
if __name__ == '__main__':
    main()
