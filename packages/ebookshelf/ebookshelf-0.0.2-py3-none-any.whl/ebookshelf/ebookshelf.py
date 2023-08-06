#! /usr/bin/python3
import xml.etree.ElementTree as ET
from .book import Book
from .library import Library

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
