import spacy
from ontology import normalize_entity

def extract_entities(text):
    try:
        nlp = spacy.load("en_core_sci_md")
        doc = nlp(text)
        entities = [
            {"text": ent.text, "label": ent.label_, "normalized": normalize_entity(ent.text)}
            for ent in doc.ents
        ]
        return entities
    except Exception as e:
        print(f"Error loading spaCy model or processing text: {e}")
        return []