# Load back with memory-mapping = read-only, shared across processes.
from gensim.models import KeyedVectors

wv = KeyedVectors.load("pizza.embeddings", mmap='r')


vector = wv['pizza22']  # Get numpy vector of a word
print(vector)
