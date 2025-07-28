def normalize_entity(entity):
    ontology_map = {
        "heart attack": "myocardial infarction",
        "diabetes": "diabetes mellitus"
    }
    return ontology_map.get(entity.lower(), entity)