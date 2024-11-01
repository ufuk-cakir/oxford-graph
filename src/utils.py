import json
from keybert import KeyBERT

def _predict_keywords(text, n_keywords=5):
    model = KeyBERT() # TODO - Load the model only once, move this outside of this function
    keywords = model.extract_keywords(text, keyphrase_ngram_range=(1, 2), use_maxsum=True, nr_candidates=20, top_n=10)
    sorted_keywords = sorted(keywords, key=lambda x: x[1], reverse=True)
    # return top n keywords
    keywords = [keyword for keyword, score in sorted_keywords[:n_keywords]]
    return keywords

def extract_research_areas(description):
    keywords = _predict_keywords(description)
    return keywords

def load_json(file):
    with open(file, 'r') as f:
        return json.load(f)
    
def save_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)