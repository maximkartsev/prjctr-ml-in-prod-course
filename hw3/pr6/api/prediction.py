import torch
import joblib
from api.model import RegressionModel
from config.constants import TRAINED_MODEL_PATH, TFIDF_VECTOR_PATH

def predict_logic(text: str):
    # Load the TF-IDF vectorizer and trained model
    tfidf = joblib.load(TFIDF_VECTOR_PATH)
    input_dim = len(tfidf.get_feature_names_out())
    
    model = RegressionModel(input_dim)
    model.load_state_dict(torch.load(TRAINED_MODEL_PATH))
    model.eval()

    # Convert the input text to TF-IDF vector
    text_vector = tfidf.transform([text]).toarray()

    # Convert to torch tensor
    text_tensor = torch.tensor(text_vector, dtype=torch.float32)

    # Perform the prediction
    with torch.no_grad():
        prediction = model(text_tensor).item()

    return {"prediction": prediction}