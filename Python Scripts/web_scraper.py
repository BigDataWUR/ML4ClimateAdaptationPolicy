#!usr/bin/env/python
"""
Author: Shashi
Description: Scrapes https://www.gov.uk/government/policies for policy documents
which we will apply the classification model on.
"""
from lxml import html
from lxml import etree
import requests
from pdf_parser import create_folder
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import os
import re
import time
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
def get_page(url):
    """Returns html element of the url of interest

    url: string, URL of a website
    """
    webpage = requests.get(url)
    web_source = html.fromstring(webpage.content)
    return web_source

def get_topics(web_source):
    """Returns a list of topic links from the UK policies website

    web_source: html element, output of get_page(url)
    """
    #retrieve every link on the page
    links = map(lambda tup: tup[2],list(web_source.iterlinks()))
    #filter for pages regarding policy topics
    topic_links = filter(lambda string: string.\
                         __contains__('/government/publications/'),links)
    return list(topic_links)

def get_publish_date(web_source):
    """Returns publishing date of policy paper as string"""
    top_level = web_source.find_class('app-c-published-dates')
    published = list(map(lambda el: list(el.itertext())[0],top_level))
    published = ' '.join(published[0].split()[-3:])
    return published

def get_department(web_source):
    """Returns department name(s) as string"""
    top_level = web_source.find_class('app-c-publisher-metadata__definition')
    department = list(map(lambda el: list(el.itertext())[2],top_level))
    return department[0]
    
def get_document_link(web_source,topic_url):
    """Returns PDF document URL if there is any"""
    links = list(map(lambda tup:tup[2],filter(lambda tup: tup[2].\
                    endswith('.pdf'),list(web_source.iterlinks()))))
    try:
        links[0]
        return links
    except IndexError:
        print('"{}" has no PDF file'.format(topic_url))
        return []

def download_save_document(full_path,document_link):
    """Downloads and writes PDF document to a file"""
    file = requests.get(document_link,verify = False)
    pdf = open(full_path,'wb')
    pdf.write(file.content)
    pdf.close()
    
def read_metadata(filename):
    """Read existing metadata dictionary in memory"""
    if os.path.isfile(filename):
        metadata = eval(open(filename,'r').read())
    else:
        print('Creating new metadata')
        metadata = {}
    return metadata

def add_metadata(document_name,publish_date,department):
    """Adds metadata to dictionary if it does not already exist"""
    try:
        metadata[document_name]
    except KeyError:
        metadata[document_name] = (publish_date,department)
    return metadata

def write_metadata(complete_metadata):
    """Writes complete collection of scraped metadata for PDF files"""
    file = open('metadata.txt','w')
    file.write(str(complete_metadata))
    file.close()
    return complete_metadata

def run_parser(target_dir,base_url,doctype,metadata):
    """Mainloop. Downloads all documents in allowed_doctypes"""
    #start timer
    start_time = time.clock()
    #Counter for eligable documents
    doc_count = 0
    failed_count = 0
    #define holder for all the metadata
    complete_metadata = {}
    topic_links = [None]
    page = 0
    #loop through all pages for a doctype
    while len(topic_links) != 0:
        page += 1
        web_url = """https://www.gov.uk/government/publications?departments%5B%5D=all&from_date=&keywords=&official_document_status=all&page={}&publication_filter_option={}&subtaxons%5B%5D=all&taxons%5B%5D=all&to_date=&world_locations%5B%5D=all""".format(page,doctype)
        web_source = get_page(web_url)
        topic_links = get_topics(web_source)
        #loops through all topics on a page
        for link in topic_links:
            topic_url = base_url+link
            web_source = get_page(topic_url)
            #loop through all pdf links in one topic
            pdf_links = get_document_link(web_source,topic_url)
            #if there is a pdf document
            if pdf_links:
                publish_date = get_publish_date(web_source)
                department = get_department(web_source)
                for link in pdf_links:
                    document_name = link.split('/')[-1]
                    if len(document_name) > 150:
                        document_name = document_name[:146]+'.pdf'
                    full_path = os.path.join(target_dir,document_name) 
                    #if it does not already exist, download it
                    if os.path.exists(full_path) == False:
                        try:
                            download_save_document(full_path,link)
                        except requests.exceptions.MissingSchema:
                            link = base_url+link
                            download_save_document(full_path,link)
                        except requests.exceptions.ConnectionError:
                            print("encountered an error, continueing")
                            failed_count += 1
                            continue
                            
                        metadata = add_metadata(document_name,publish_date,department)
                        doc_count += 1
                    
    #write complete metadata to a text file
    complete_metadata = write_metadata(metadata)
    print('Scraping complete. Took {} seconds to retrieve {} documents. Failed {}'\
          .format(int(time.clock()-start_time),doc_count, failed_count))
    return complete_metadata
if __name__ == '__main__':
    #load metadata if available
    metadata = read_metadata('metadata.txt')
    #define folder to store the documents
    target_dir = '..\PDF_files\Scraped documents'
    create_folder(target_dir)
    #base url and url that lists all topics which have policy papers
    base_url = 'https://www.gov.uk'
    
    #document types we are interested in
    allowed_doctypes = ['policy-papers']
    #start scraping process
    for doctype in allowed_doctypes:
        metadata = run_parser(target_dir,base_url,doctype,metadata)
