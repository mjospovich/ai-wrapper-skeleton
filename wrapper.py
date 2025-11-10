"""
WRAPPER.PY - Main Customization File
=====================================

This is the PRIMARY file you should customize for your use case.
Edit the functions below to transform your input/output as needed.

The default implementation works with simple Q&A prompts like:
    {"prompt": "What is the capital of France?"}
"""

def process_input(input_data: dict) -> str:
    """
    User-customizable: Transform input data into a prompt for the AI.
    
    This is a skeleton implementation. Customize this function based on your use case.
    
    Default behavior: Extracts 'prompt' key from input and returns it as-is.
    This works well for simple Q&A use cases like "What is the capital of France?"
    
    Example customizations:
    - For calorie estimation:
        food_items = ', '.join(input_data.get('food_items', []))
        return f"Analyze these food items: {food_items}. Estimate total calories and return only the number."
    
    - For structured data extraction:
        return f"Extract the following information from: {input_data.get('text')}. Return as JSON."
    """
    # Extract prompt from input
    prompt = input_data.get('prompt', '')
    
    # Validate that we have a prompt
    if not prompt or not prompt.strip():
        raise ValueError("No 'prompt' provided in input data. Please provide a prompt to process.")
    
    # Return the prompt (customize this logic for your use case)
    return prompt.strip()

def process_output(raw_output: str) -> dict:
    """
    User-customizable: Parse and format the AI's raw output.
    
    This is a skeleton implementation. Customize this function based on your use case.
    
    Default behavior: Returns the raw AI response wrapped in a dict with 'output' key.
    This works well for simple Q&A responses.
    
    Example customizations:
    - For extracting numbers:
        try:
            number = int(raw_output.strip())
            return {"value": number}
        except ValueError:
            return {"error": "Could not extract number"}
    
    - For JSON parsing:
        import json
        return json.loads(raw_output)
    
    - For structured extraction:
        # Parse and validate the response
        return {"answer": raw_output.strip(), "confidence": "high"}
    """
    # Validate that we have output
    if not raw_output or not raw_output.strip():
        return {"error": "Empty response from AI", "output": None}
    
    # Return formatted output (customize this logic for your use case)
    return {"output": raw_output.strip()}