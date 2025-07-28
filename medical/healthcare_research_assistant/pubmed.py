# import requests
# from xml.etree import ElementTree as ET

# def search_pubmed(query, max_results=5):
#     base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
#     params = {
#         "db": "pubmed",
#         "term": query,
#         "retmax": max_results,
#         "retmode": "xml",
#     }
#     res = requests.get(base_url, params=params)
#     if res.status_code != 200:
#         return []

#     root = ET.fromstring(res.text)
#     id_list = [id_elem.text for id_elem in root.findall(".//Id")]

#     articles = []
#     for pmid in id_list:
#         article = fetch_pubmed_abstract(pmid)
#         if article:
#             articles.append(article)
#     return articles

# def fetch_pubmed_abstract(pmid):
#     base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
#     params = {
#         "db": "pubmed",
#         "id": pmid,
#         "retmode": "xml",
#     }
#     res = requests.get(base_url, params=params)
#     if res.status_code != 200:
#         return None

#     root = ET.fromstring(res.text)
#     article_title = root.findtext(".//ArticleTitle")
#     abstract_text = ""
#     abstract_elems = root.findall(".//AbstractText")
#     if abstract_elems:
#         abstract_text = " ".join(elem.text for elem in abstract_elems if elem.text)
#     if not article_title or not abstract_text:
#         return None
#     return {"title": article_title, "abstract": abstract_text}


import requests
import xml.etree.ElementTree as ElementTree
import time

def fetch_pubmed_papers(query, max_results=5, retries=3):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    headers = {"User-Agent": "MedicalResearchAssistant/1.0"}
    
    # Search for PubMed IDs
    search_url = f"{base_url}esearch.fcgi?db=pubmed&term={query}&retmax={max_results}&retmode=xml"
    for attempt in range(retries):
        try:
            response = requests.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()
            root = ElementTree.fromstring(response.content)
            pmids = [elem.text for elem in root.findall(".//Id") if elem.text]
            time.sleep(0.5)
            if not pmids:
                return []
            
            # Fetch paper details
            fetch_url = f"{base_url}efetch.fcgi?db=pubmed&id={','.join(pmids)}&retmode=xml"
            response = requests.get(fetch_url, headers=headers, timeout=10)
            response.raise_for_status()
            root = ElementTree.fromstring(response.content)
            papers = []
            for article in root.findall(".//PubmedArticle"):
                paper = {}
                article_meta = article.find("MedlineCitation/Article")
                if article_meta:
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
                    doi_elem = article.find(".//ArticleId[@IdType='doi']")
                    paper['doi'] = doi_elem.text if doi_elem is not None else "No DOI"
                else:
                    paper = {"title": "No Title", "abstract": "No Abstract", "authors": ["Unknown Author"], "doi": "No DOI"}
                journal = article.find("MedlineCitation/Journal")
                paper['journal'] = journal.find("Title").text if journal and journal.find("Title") else "Unknown Journal"
                paper['year'] = journal.find("JournalIssue/PubDate/Year").text if journal and journal.find("JournalIssue/PubDate/Year") else "Unknown Year"
                papers.append(paper)
            return papers
        except Exception as e:
            if attempt == retries - 1:
                print(f"Error fetching PubMed papers after {retries} attempts: {e}")
                return []
            time.sleep(2 ** attempt)
    return []