def process_input(input_data: dict) -> str:
    """
    User-customizable: Transform input data into a prompt for the AI.
    
    This is a skeleton implementation. Customize this function based on your use case.
    For example, if analyzing food items for calories:
        food_items = ', '.join(input_data.get('food_items', []))
        prompt = f"Analyze these food items: {food_items}. Estimate total approximate calories for the day and return only the number (e.g., 1500)."
        return prompt
    """
    # Default: just pass through as a simple prompt
    user_prompt = input_data.get('prompt', '')
    if not user_prompt:
        # Fallback: try to convert input_data to a readable format
        user_prompt = str(input_data)
    return user_prompt

def process_output(raw_output: str) -> dict:
    """
    User-customizable: Parse and format the AI's raw output.
    
    This is a skeleton implementation. Customize this function based on your use case.
    For example, if extracting calories:
        try:
            calories = int(raw_output.strip())
            return {"total_calories": calories}
        except ValueError:
            return {"error": "Invalid output from AI"}
    """
    # Default: return raw output wrapped in a dict
    return {"output": raw_output.strip()}