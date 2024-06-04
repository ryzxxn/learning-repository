import torch
import yaml

from box import Box
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from llm.prompts import qa_template
from llm.llm import setup_llm

# Import config vars
with open('config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = Box(yaml.safe_load(ymlfile))

def set_qa_prompt():
    """
    Prompt template for QA retrieval for each vectorstore
    """

    prompt = PromptTemplate(template=qa_template,
                            input_variables=['context', 'question'])

    return prompt

def build_retrieval_qa_chain(llm, prompt):
    # Use CUDA if available
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    embeddings = HuggingFaceEmbeddings(model_name=cfg.EMBEDDINGS,
                                       model_kwargs={'device': device})
    vectordb = FAISS.load_local(cfg.DB_FAISS_PATH, embeddings)
    retriever = vectordb.as_retriever(search_kwargs={'k': cfg.VECTOR_COUNT})

    qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                           chain_type='stuff',
                                           retriever=retriever,
                                           return_source_documents=cfg.RETURN_SOURCE_DOCUMENTS,
                                           chain_type_kwargs={'prompt': prompt})
    return qa_chain

def setup_qa_chain():
    llm = setup_llm()
    qa_prompt = set_qa_prompt()
    qa_chain = build_retrieval_qa_chain(llm, qa_prompt)

    return qa_chain

def query_embeddings(query):
    # Use CUDA if available
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    embeddings = HuggingFaceEmbeddings(model_name=cfg.EMBEDDINGS,
                                       model_kwargs={'device': device})
    vectordb = FAISS.load_local(cfg.DB_FAISS_PATH, embeddings)
    retriever = vectordb.as_retriever(search_kwargs={'k': cfg.VECTOR_COUNT})
    semantic_search = retriever.get_relevant_documents(query)

    return semantic_search

# Set up your QA chain
qa_chain = setup_qa_chain()

# Example usage:
query_result = query_embeddings("your_query_here")
print(query_result)
