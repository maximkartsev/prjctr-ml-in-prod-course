import torch
from transformers import BertTokenizer, BertModel

# Function to get embeddings using BERT
def get_bert_embeddings(texts):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')

    inputs = tokenizer(texts, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    
    # We take the mean of the last hidden state to create the vector
    embeddings = torch.mean(outputs.last_hidden_state, dim=1)
    return embeddings.numpy()
