from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def create_faiss(concept_context):
    texts = [f"{k}: {v}" for k, v in concept_context.items()]
    return FAISS.from_texts(texts, embedding_model)

def retrieve_concepts(faiss_store, query="concept", k=5):
    return [doc.page_content for doc in faiss_store.similarity_search(query, k=k)]
