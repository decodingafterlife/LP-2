import json
import numpy as np
from sentence_transformers import SentenceTransformer, util

class Chatbot:
    def __init__(self, kb_path="knowledge_base.json"):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        with open(kb_path, 'r') as f:
            self.kb = json.load(f)
        self.questions = [item['question'] for item in self.kb]
        self.answers = [item['answer'] for item in self.kb]
        self.embeddings = self.model.encode(self.questions, convert_to_tensor=True)

    def get_response(self, query):
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        scores = util.pytorch_cos_sim(query_embedding, self.embeddings)[0]
        best_match_idx = int(np.argmax(scores))
        confidence = float(scores[best_match_idx])
        if confidence < 0.5:
            return "I'm sorry, I couldn't find a suitable answer. Please contact support."
        return self.answers[best_match_idx]
