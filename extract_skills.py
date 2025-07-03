import spacy
import pandas as pd
import os

def load_skills(file_path="skills.csv"):
    if not os.path.exists(file_path):
        print(f"[ERROR] skills.csv not found at {file_path}")
        return []
    df = pd.read_csv(file_path)
    return [{"label": "SKILL", "pattern": skill.strip()} for skill in df["skill"].dropna()]

def init_nlp_with_skills():
    nlp = spacy.load("en_core_web_lg")  # You can switch to "en_core_web_md" for better embeddings
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    patterns = load_skills()
    ruler.add_patterns(patterns)
    return nlp

nlp = init_nlp_with_skills()

def extract_skills(text):
    doc = nlp(text.lower())
    return list(set(ent.text.strip() for ent in doc.ents if ent.label_ == "SKILL"))
