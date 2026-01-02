from enum import Enum
import torch
from transformers import AutoTokenizer, DistilBertForSequenceClassification

class ModelPrediction(Enum):
    FAKE = 0
    REAL = 1

tokenizer = AutoTokenizer.from_pretrained("model")
model = DistilBertForSequenceClassification.from_pretrained("model", use_safetensors=True)

def get_newsletter_text(url: str) -> str:
    raise NotImplementedError()

def predict(text: str) -> ModelPrediction:
    inputs = tokenizer(text[:512], return_tensors="pt")

    with torch.no_grad():
        logits = model(**inputs).logits

    predicted_class_id = logits.argmax().item()

    return ModelPrediction(predicted_class_id)