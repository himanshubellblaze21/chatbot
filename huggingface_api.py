from transformers import pipeline

# Load Hugging Face's Question Answering model (RoBERTa fine-tuned on SQuAD2)
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")


def query_huggingface(document_text, user_query):
    """Use Hugging Face AI to answer user queries based on document content."""
    result = qa_pipeline(question=user_query, context=document_text)
    return result["answer"]

