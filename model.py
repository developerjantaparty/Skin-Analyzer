from transformers import pipeline, Pipeline
from PIL import Image
from typing import List, Dict, Union

class SkinFeatureAnalyzer:
    """
    Handles image classification using a Hugging Face pipeline for skin feature detection.
    """

    def __init__(self, model_name: str = "wetom/skin-disease-pre-trained-model"):
        """
        Initializes the classifier pipeline.

        Args:
            model_name: The Hugging Face model moniker.
        """
        try:
            self.classifier: Pipeline = pipeline("image-classification", model=model_name)
        except Exception as e:
            print(f"Error loading model {model_name}: {e}")
            raise

    def analyze_image(self, image: Image.Image) -> List[Dict[str, Union[str, float]]]:
        """
        Runs inference on the provided image and returns classification results.

        Args:
            image: A PIL Image object of the face.

        Returns:
            A list of dictionaries containing 'label' and 'score'.
        """
        try:
            results = self.classifier(image)
            return results
        except Exception as e:
            print(f"Error during image analysis: {e}")
            return []

if __name__ == "__main__":
    # Bare minimum test to initialize and verify object creation
    try:
        analyzer = SkinFeatureAnalyzer()
        print("Model initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize model: {e}")