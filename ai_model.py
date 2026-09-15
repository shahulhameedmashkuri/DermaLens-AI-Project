from PIL import Image
import os


def analyze_skin_image(image_path):
    try:
        if not os.path.isfile(image_path):
            return {
                "success": False,
                "error": "Image file not found."
            }

        image = Image.open(image_path).convert("RGB")

        width, height = image.size

        if width < 100 or height < 100:
            return {
                "success": False,
                "error": "Please upload a clearer image."
            }

        # Lightweight image screening only
        pixels = list(image.resize((50, 50)).getdata())

        average_red = sum(pixel[0] for pixel in pixels) / len(pixels)
        average_green = sum(pixel[1] for pixel in pixels) / len(pixels)
        average_blue = sum(pixel[2] for pixel in pixels) / len(pixels)

        prediction = "Image received for preliminary screening"
        confidence = 0

        return {
            "success": True,
            "prediction": prediction,
            "confidence": confidence,
            "recommendation": (
                "This is a lightweight prototype screening result. "
                "It is not an AI-based skin-disease diagnosis. "
                "Please consult a qualified dermatologist for accurate diagnosis."
            )
        }

    except Exception as error:
        print("Analysis error:", error)

        return {
            "success": False,
            "error": "Unable to analyze image. Please try again."
        }