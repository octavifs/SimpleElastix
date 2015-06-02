#!/usr/bin/env python

from __future__ import print_function
import xml.dom.minidom
from  xml.parsers.expat import ExpatError
import argparse
import sys
import re

description = """
This script converts the default Release Notes from JIRA to a ITK's wiki format.

Specifically input such as:

<h2>        Epic
</h2>
<ul>
<li>[<a href='https://issues.itk.org/jira/browse/SIMPLEITK-1'>SIMPLEITK-1</a>] -         Develop registration framework for ITKv4 Framework
</li>
<li>[<a href='https://issues.itk.org/jira/browse/SIMPLEITK-571'>SIMPLEITK-571</a>] -         Add More Registration Examples
</li>
</ul>

is converted to:

==Epic==

*[[[https://issues.itk.org/jira/browse/SIMPLEITK-1SIMPLEITK-1]]] - Develop registration framework for ITKv4 Framework
*[[[https://issues.itk.org/jira/browse/SIMPLEITK-571SIMPLEITK-571]]] - Add More Registration Examples

"""


def do_text(node,strip=False):
    """Render a text node, with some while space cleanup"""
    text = node.data.encode('ascii', 'replace');
    text = re.sub(' +', ' ', text)
    if strip:
        text = text.strip()
    return text;

def do_li(node):
    """Render a li element into a wiki bullet-ed list"""
    return ("*"+parse(node)).rstrip('\n')

def do_a(node):
    """Render a hyperlink node, into a wiki link"""
    if node.hasAttribute("href"):
        return "[["+node.attributes["href"].value+' '+parse(node)+"]]"

def do_h(node, level=1):
    """Render a header title"""
    s="="*level
    if len(node.childNodes)==1 and node.firstChild.nodeType == xml.dom.Node.TEXT_NODE:
        s+=do_text(node.firstChild, strip=True)
    else:
        s+=parse(node)
    s +="="*level
    return s

def parse_Element(node):
    """Dispatch to correct handling do method"""
    if node.tagName == "li":
        return do_li(node)
    elif node.tagName == "a":
        return do_a(node)
    elif node.tagName == "h1":
        return do_h(node,1)
    elif node.tagName == "h2":
        return do_h(node,2)
    else:
        return parse(node)


def parse_Document(node):
    """Dispatch for root document element"""
    return parse(node.documentElement)

def parse(node):
    """Core reclusive method for depth-first traversal without state"""
    s=""
    for child in node.childNodes:
        if child.nodeType == xml.dom.Node.TEXT_NODE:
            s+=do_text(child)
        elif child.nodeType == xml.dom.Node.DOCUMENT_TYPE_NODE:
            s+=parse_Document(child)
        elif child.nodeType == xml.dom.Node.ELEMENT_NODE:
            s+=parse_Element(child)
    return s



def html_fragment_to_wiki(html_fragment):
    dom = xml.dom.minidom.parseString("<html>"+html_fragment+"</html>")
    return parse(dom)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("inputHTMLNotes", help="Input file name containing the HTML fragment of release notes generated by JIRA.")


    args = parser.parse_args()

    with open(args.inputHTMLNotes, "r") as myfile:
        data=myfile.read()

    try:
        print(html_fragment_to_wiki(data))
    except ExpatError as e:
        print(e, file=sys.stderr)
        # 1 based line index in error
        print( "   \"{0}\"".format(data.splitlines()[e.lineno-1]), file=sys.stderr)
