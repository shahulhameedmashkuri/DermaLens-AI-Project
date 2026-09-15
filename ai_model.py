from PIL import Image
import os
from transformers import pipeline

classifier = pipeline(
    "image-classification",
    model="microsoft/resnet-50",
    device=-1
)


def analyze_skin_image(image_path):

    try:
        if not os.path.isfile(image_path):
            return {
                "success": False,
                "error": "Image file not found."
            }

        image = Image.open(image_path).convert("RGB")

        results = classifier(image)
        best_result = results[0]

        prediction = best_result["label"]
        confidence = round(best_result["score"] * 100, 2)

        return {
            "success": True,
            "prediction": prediction,
            "confidence": confidence,
            "recommendation": (
                f"Model output: {prediction}. "
                "This is a general image-classification result, "
                "not a skin-disease diagnosis. "
                "Please consult a qualified dermatologist."
            )
        }

    except Exception as error:
        print("Analysis error:", error)

        return {
            "success": False,
            "error": "Unable to analyze image. Please try again."
        }