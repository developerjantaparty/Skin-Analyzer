import sys
from model.detector import SkinIssueDetector
from ui.cli import get_image_path, display_results, display_disclaimer

def run_project() -> None:
    """
    Orchestrates the execution of the skin issue detection project.
    Connects user input, model inference, and results display with disclaimer.
    """
    display_disclaimer()
    
    image_path = get_image_path()
    if not image_path:
        print("Error: No image path provided.")
        return

    try:
        detector = SkinIssueDetector()
        print("\nAnalyzing image...")
        prediction_result = detector.predict(image_path)
        
        # Format result to match ui.cli expectations (dictionary of prediction: confidence)
        formatted_results = {
            prediction_result["prediction"]: prediction_result["confidence"]
        }
        
        display_results(formatted_results)
        
    except IOError as e:
        print(f"\nError: {e}")
    except RuntimeError as e:
        print(f"\nFatal Error: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    run_project()