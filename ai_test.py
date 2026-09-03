from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch

MODEL_NAME = "LaurianeMD/vit-skin-disease"

print("Loading DermaLens.AI model...")

processor = AutoImageProcessor.from_pretrained(MODEL_NAME)

model = AutoModelForImageClassification.from_pretrained(
    MODEL_NAME
)

model.eval()

print("Model loaded successfully!")


image_path = "static/uploads/skin.jpg"

image = Image.open(image_path).convert("RGB")

inputs = processor(
    images=image,
    return_tensors="pt"
)

with torch.no_grad():
    outputs = model(**inputs)

probabilities = torch.softmax(
    outputs.logits,
    dim=-1
)

confidence, predicted_class = torch.max(
    probabilities,
    dim=-1
)

label = model.config.id2label[
    predicted_class.item()
]

print("--------------------------------")
print("Prediction:", label)
print("Confidence:", round(confidence.item() * 100, 2), "%")
print("--------------------------------")