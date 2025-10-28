from pdfminer.high_level import extract_text
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re
 
def extract_pdf_text(file_like):
    try:
        file_like.seek(0)
        text = extract_text(file_like)
        return text or ""
    except Exception:
        try:
            file_like.seek(0)
            return extract_text(file_like)
        except Exception:
            return ""
 
def calculate_similarity_bert(text1, text2):
    try:
        model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
        emb1 = model.encode([text1])
        emb2 = model.encode([text2])
        sim = cosine_similarity(emb1, emb2)[0][0]
        return float(sim)
    except Exception:
        return None
 
def extract_scores(text):
    pattern = r'(\d+(?:\.\d+)?)/5'
    matches = re.findall(pattern, text)
    scores = [float(m) for m in matches]
    return scores
