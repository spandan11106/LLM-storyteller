# storyteller/utils.py

def sanitize_data_for_graph(data):
    """
    Recursively traverses a data structure and converts any dicts or lists
    found as values into their string representations. This is an aggressive
    safety net to prevent 'unhashable type' errors when processing LLM output.
    """
    if isinstance(data, list):
        return [sanitize_data_for_graph(item) for item in data]
    
    if isinstance(data, dict):
        clean_dict = {}
        for key, value in data.items():
            # The key must be a string.
            clean_key = str(key)
            
            # If the value is a list or dict, stringify it. Otherwise, recurse.
            if isinstance(value, (dict, list)):
                clean_dict[clean_key] = str(value)
            else:
                clean_dict[clean_key] = sanitize_data_for_graph(value)
        return clean_dict
        
    # For all other types (int, str, bool, etc.), return as is.
    return data