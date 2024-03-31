from typing import Any, Dict
from pydantic import BaseModel, create_model

def json_to_pydantic(name: str, json_object: Dict[str, Any], depth: int = 0) -> BaseModel:
    """
    Dynamically creates a Pydantic model from a JSON object, handling nested objects.

    Args:
    - name: The name of the Pydantic model.
    - json_object: The JSON object from which to create the model.
    - depth: Current depth of recursion; used for naming nested models.

    Returns:
    - A dynamically created Pydantic model class.
    """
    fields = {}
    for key, value in json_object.items():
        print(key, ": ", value)
        if isinstance(value, dict):
            # Recursive call for nested dictionaries
            nested_model_name = f"{name}_{key.capitalize()}Model"
            print("Nested model name: ", nested_model_name)
            nested_model = json_to_pydantic(nested_model_name, value, depth + 1)
            print("Nested model: ", nested_model)
            fields[key] = (nested_model, ...)
            print(fields)
        else:
            # Handle basic data types (int, float, str, bool, list)
            fields[key] = (type(value), ...)
            print(fields)
    
    # Create the Pydantic model
    return create_model(name, **fields)

# Example usage
if __name__ == "__main__":
    json_example = {
        "id": 123,
        "name": "John Doe",
        "email": "john@example.com",
        "is_active": True,
        "balance": 99.95,
        "tags": ["new", "user"],
        "profile": {
            "age": 30,
            "country": "US",
            "preferences": {
                "newsletter": True,
                "notifications": False
            }
        }
    }

    UserModel = json_to_pydantic("UserModel", json_example)
    user = UserModel(**json_example)
    print(user)
    print(user.profile)
    print(user.profile.preferences)
