# File: CheckTags.py

"""
This program checks that tags are properly matched in an HTML file.
This version of the program runs in Python; the checktags version runs
directly from the command line.
"""

import html.parser
import urllib.request
import urllib.error
import os.path

def CheckTags():
    """Reads a URL from the user and then checks it for tag matching."""
    # url = input("URL: ")
    url = 'http://people.reed.edu/~esroberts/index.html'
    base = os.path.dirname(url)
    checkURL(url,base)
def checkURL(url,base):
    """Checks whether the tags are balanced in the specified URL."""
    # response = urllib.request.Request(url)

    try: 
        response = urllib.request.urlopen(url)
        print("!",type(response))
        parser = HTMLTagParser()
        # parser.checkTags(response.read().decode("UTF-8"))
        parser.brokenLinks(response.read().decode("UTF-8"),base)
    except urllib.error.URLError as e: 
        print("Encountered a problem:", e.getcode(), e.reason)
# From https://python.readthedocs.io/en/stable/howto/urllib2.html




class HTMLTagParser(html.parser.HTMLParser):

    """
    This class extends the standard HTML parser and overrides the
    callback methods used for start and end tags.
    """

    def __init__(self):
        """Creates a new HTMLTagParser object."""
        html.parser.HTMLParser.__init__(self)
        self._stack = [ ]
        self.linkStack = []

    def checkTags(self, text):
        """Checks that the tags are balanced in the supplied text."""

        self.feed(text)
        while len(self._stack) > 0:
            startTag,startLine = self._stack.pop()
            print("Missing </" + startTag + "> for <" + startTag +
                  "> at line " + str(startLine))
    def brokenLinks(self,text,base):
        '''
        Checks for all links in webpages and reports all broken 
        links using error checking methods 
        '''


        self.feed(text)
        while len(self.linkStack) > 0:
            
            #attempt to parse, if error, print. otherwise, move on
            try:
                tag, line, link = self.linkStack.pop()
                response = urllib.request.urlopen(link)
            except urllib.error.URLError as e: 
                print("Encountered a problem on line "+str(line)+ " with tag <"+str(tag)+ "> for link "+str(link)+"\n"+ str(e.reason))
            except ValueError:
                response = urllib.request.urlopen(base+"/"+link)
    def handle_starttag(self, startTag, attributes):
        """Overrides the callback function for start tags."""
        startLine,_ = self.getpos()
        self._stack.append((startTag, startLine))
        if attributes:
            if attributes[0][0] == 'href':
                self.linkStack.append((startTag,startLine,attributes[0][1]))
            elif attributes[0][0] == 'src':
                self.linkStack.append((startTag,startLine,attributes[0][1]))

    def handle_endtag(self, endTag):
        """Overrides the callback function for end tags."""
        endLine,_ = self.getpos()
        if len(self._stack) == 0:
            print("No <" + endTag + "> for </" + endTag +
                  "> at line " + str(endLine))
        else:
            while len(self._stack) > 0:
                startTag,startLine = self._stack.pop()
                if startTag == endTag:
                    break;
                print("Missing </" + startTag + "> for <" + startTag +
                      "> at line " + str(startLine))

# Startup code

if __name__ == "__main__":
    CheckTags()
