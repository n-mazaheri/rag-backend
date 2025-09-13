from sentence_transformers import SentenceTransformer

# Choose the model
model_name = "sentence-transformers/all-MiniLM-L6-v2"

# Load the model (this will download it)
model = SentenceTransformer(model_name)

# Save it locally
model.save("./embedding_model")
print("Model saved to ./embedding_model")
