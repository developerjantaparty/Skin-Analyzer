def get_image_path() -> str:
    """
    Prompts the user to enter the path to an image file.

    Returns:
        str: The file path entered by the user.
    """
    return input("Enter the path to the skin image: ").strip()

def display_results(results: dict[str, float]) -> None:
    """
    Prints the analysis results in a readable format.

    Args:
        results (dict[str, float]): A dictionary mapping detected issues to confidence scores.
    """
    print("\n--- Analysis Results ---")
    if not results:
        print("No specific issues detected based on the analysis.")
    else:
        for issue, confidence in results.items():
            print(f"- {issue}: {confidence:.2f}")
    print("------------------------")

def display_disclaimer() -> None:
    """
    Prints a medical disclaimer.
    """
    print("\n**************************************************************")
    print("Disclaimer: This tool provides general information based on AI analysis.")
    print("It is NOT a substitute for professional medical advice, diagnosis, or treatment.")
    print("Always consult a dermatologist or healthcare professional.")
    print("**************************************************************\n")