from transformers import ViTImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch
import os


MODEL_NAME = "PREMAADC/vit-base-ham10000"

print("Loading DermaLens.AI model...")

processor = ViTImageProcessor.from_pretrained(
    "google/vit-base-patch16-224"
)

model = AutoModelForImageClassification.from_pretrained(
    MODEL_NAME
)

model.eval()

print("REAL AI MODEL LOADED SUCCESSFULLY")

print("DermaLens.AI model loaded successfully.")


def analyze_skin_image(image_path):

    try:
        if not os.path.isfile(image_path):
            return {
                "success": False,
                "error": "Image file not found."
            }

        image = Image.open(image_path).convert("RGB")

        inputs = processor(
            images=image,
            return_tensors="pt"
        )

        with torch.no_grad():
            outputs = model(**inputs)

        probabilities = torch.nn.functional.softmax(
            outputs.logits,
            dim=-1
        )

        confidence, predicted_class = torch.max(
            probabilities,
            dim=-1
        )

        prediction = model.config.id2label[
            predicted_class.item()
        ]

        confidence_value = round(
            confidence.item() * 100,
            2
        )

        return {
            "success": True,
            "prediction": prediction,
            "confidence": confidence_value,
            "recommendation": (
                "This is an AI-assisted research result, "
                "not a medical diagnosis. "
                "Please consult a qualified dermatologist."
            )
        }

    except Exception as error:

        print("AI analysis error:", error)

        return {
            "success": False,
            "error": "Unable to analyze the image."
        }