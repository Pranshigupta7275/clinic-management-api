def custom_response(success, data=None, message=""):
    """
    Helper function to format API responses consistently.
    
    Args:
        success (bool): Whether the operation was successful
        data (any): The response data (serializer data, list, etc.)
        message (str): Optional message describing the result
    
    Returns:
        dict: Formatted response dictionary
    """
    return {
        "success": success,
        "data": data,
        "message": message
    }
