# backend/tools.py
import requests
from xml.etree import ElementTree as ET
import time

def pubmed_search(query, max_results=5, retries=3):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "xml"
    }
    headers = {"User-Agent": "MedicalResearchChatbot/1.0 (Contact: no-email-provided)"}
    
    for attempt in range(retries):
        try:
            response = requests.get(base_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            ids = [elem.text for elem in root.findall(".//Id") if elem.text]
            time.sleep(0.5)  # Add a 0.5-second delay to avoid rate-limiting
            return ids
        except (requests.exceptions.RequestException, ET.ParseError) as e:
            if attempt == retries - 1:
                print(f"Failed to search PubMed after {retries} attempts: {e}")
                return []
            time.sleep(2 ** attempt)  # Exponential backoff
    return []

def pubmed_fetch_details(id_list, retries=3):
    if not id_list:
        return []

    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    ids = ",".join(id_list)
    params = {
        "db": "pubmed",
        "id": ids,
        "retmode": "xml"
    }
    headers = {"User-Agent": "MedicalResearchChatbot/1.0 (Contact: no-email-provided)"}

    for attempt in range(retries):
        try:
            response = requests.get(base_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            papers = []
            for article in root.findall(".//PubmedArticle"):
                paper = {}
                article_meta = article.find("MedlineCitation/Article")
                if article_meta is not None:
                    title = article_meta.find("ArticleTitle")
                    paper['title'] = title.text if title is not None and title.text else "No Title"
                    abstract = article_meta.find("Abstract/AbstractText")
                    paper['abstract'] = abstract.text if abstract is not None and abstract.text else "No Abstract"
                    authors = []
                    for author in article_meta.findall("AuthorList/Author"):
                        first = author.find("ForeName")
                        last = author.find("LastName")
                        if first is not None and last is not None and first.text and last.text:
                            authors.append(f"{first.text} {last.text}")
                    paper['authors'] = authors if authors else ["Unknown Author"]
                else:
                    paper = {"title": "No Title", "abstract": "No Abstract", "authors": ["Unknown Author"]}
                huntington = article.find("MedlineCitation")
                if huntington is not None:
                    journal = huntington.find("Journal")
                    if journal is not None:
                        journal_title = journal.find("Title")
                        paper['journal'] = journal_title.text if journal_title is not None and journal_title.text else "Unknown Journal"
                        year = journal.find("JournalIssue/PubDate/Year")
                        paper['year'] = year.text if year is not None and year.text else "Unknown Year"
                    else:
                        paper['journal'] = "Unknown Journal"
                        paper['year'] = "Unknown Year"
                papers.append(paper)
            time.sleep(0.5)  # Add a 0.5-second delay to avoid rate-limiting
            return papers
        except (requests.exceptions.RequestException, ET.ParseError) as e:
            if attempt == retries - 1:
                print(f"Failed to fetch paper details after {retries} attempts: {e}")
                return []
            time.sleep(2 ** attempt)  # Exponential backoff
    return []