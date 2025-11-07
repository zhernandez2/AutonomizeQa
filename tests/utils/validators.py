"""
Data validation utilities for test suite
"""
import jsonschema
from jsonschema import validate, ValidationError
from typing import Dict, Any, Tuple, List
import json
from pathlib import Path


class DataValidator:
    """Validates data against JSON schemas"""
    
    def __init__(self, schema_path: Path = None):
        """
        Initialize validator with schema path
        
        Args:
            schema_path: Path to directory containing JSON schemas
        """
        self.schema_path = schema_path or Path(__file__).parent.parent / "fixtures" / "schemas"
        self._schemas = {}
    
    def load_schema(self, schema_name: str) -> Dict[str, Any]:
        """
        Load JSON schema from file
        
        Args:
            schema_name: Name of schema file (e.g., 'patient_record.json')
            
        Returns:
            Schema dictionary
        """
        if schema_name not in self._schemas:
            schema_file = self.schema_path / schema_name
            with open(schema_file, 'r') as f:
                self._schemas[schema_name] = json.load(f)
        return self._schemas[schema_name]
    
    def validate_data(self, data: Dict[str, Any], schema_name: str) -> Tuple[bool, List[str]]:
        """
        Validate data against schema
        
        Args:
            data: Data to validate
            schema_name: Name of schema file
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        try:
            schema = self.load_schema(schema_name)
            validate(instance=data, schema=schema)
            return True, []
        except ValidationError as e:
            errors = [f"Validation error: {e.message} at path: {'.'.join(str(p) for p in e.path)}"]
            return False, errors
        except Exception as e:
            return False, [f"Unexpected error: {str(e)}"]
    
    def validate_required_fields(self, data: Dict[str, Any], schema_name: str) -> Tuple[bool, List[str]]:
        """
        Validate that all required fields are present
        
        Args:
            data: Data to validate
            schema_name: Name of schema file
            
        Returns:
            Tuple of (all_present, list_of_missing_fields)
        """
        schema = self.load_schema(schema_name)
        required_fields = schema.get("required", [])
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return False, missing_fields
        return True, []
    
    def validate_data_types(self, data: Dict[str, Any], schema_name: str) -> Tuple[bool, List[str]]:
        """
        Validate data types match schema
        
        Args:
            data: Data to validate
            schema_name: Name of schema file
            
        Returns:
            Tuple of (all_valid, list_of_type_errors)
        """
        schema = self.load_schema(schema_name)
        errors = []
        
        def check_type(value, schema_prop, path=""):
            if "type" in schema_prop:
                expected_type = schema_prop["type"]
                actual_type = type(value).__name__
                
                type_map = {
                    "string": "str",
                    "integer": "int",
                    "number": ("int", "float"),
                    "boolean": "bool",
                    "array": "list",
                    "object": "dict"
                }
                
                expected_python_type = type_map.get(expected_type)
                if expected_type == "number":
                    if actual_type not in expected_python_type:
                        errors.append(f"Type mismatch at {path}: expected number (int/float), got {actual_type}")
                elif actual_type != expected_python_type:
                    errors.append(f"Type mismatch at {path}: expected {expected_type}, got {actual_type}")
        
        def validate_recursive(data_obj, schema_obj, path=""):
            if "properties" in schema_obj:
                for key, value in data_obj.items():
                    current_path = f"{path}.{key}" if path else key
                    if key in schema_obj["properties"]:
                        prop_schema = schema_obj["properties"][key]
                        check_type(value, prop_schema, current_path)
                        
                        if prop_schema.get("type") == "object" and "properties" in prop_schema:
                            validate_recursive(value, prop_schema, current_path)
                        elif prop_schema.get("type") == "array" and "items" in prop_schema:
                            if isinstance(value, list):
                                for i, item in enumerate(value):
                                    item_path = f"{current_path}[{i}]"
                                    if prop_schema["items"].get("type") == "object":
                                        validate_recursive(item, prop_schema["items"], item_path)
                                    else:
                                        check_type(item, prop_schema["items"], item_path)
        
        validate_recursive(data, schema)
        return len(errors) == 0, errors
    
    def validate_format(self, data: Dict[str, Any], schema_name: str) -> Tuple[bool, List[str]]:
        """
        Validate data format (dates, patterns, etc.)
        
        Args:
            data: Data to validate
            schema_name: Name of schema file
            
        Returns:
            Tuple of (all_valid, list_of_format_errors)
        """
        schema = self.load_schema(schema_name)
        errors = []
        
        def validate_pattern(value, pattern, path):
            import re
            if not re.match(pattern, str(value)):
                errors.append(f"Format error at {path}: value '{value}' does not match pattern '{pattern}'")
        
        def validate_format_value(value, format_type, path):
            if format_type == "date":
                import re
                date_pattern = r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
                if not re.match(date_pattern, str(value)):
                    errors.append(f"Date format error at {path}: expected YYYY-MM-DD, got '{value}'")
            elif format_type == "email":
                import re
                email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
                if not re.match(email_pattern, str(value)):
                    errors.append(f"Email format error at {path}: invalid email format '{value}'")
        
        def validate_recursive(data_obj, schema_obj, path=""):
            if "properties" in schema_obj:
                for key, value in data_obj.items():
                    current_path = f"{path}.{key}" if path else key
                    if key in schema_obj["properties"]:
                        prop_schema = schema_obj["properties"][key]
                        
                        if "pattern" in prop_schema:
                            validate_pattern(value, prop_schema["pattern"], current_path)
                        
                        if "format" in prop_schema:
                            validate_format_value(value, prop_schema["format"], current_path)
                        
                        if prop_schema.get("type") == "object" and "properties" in prop_schema:
                            validate_recursive(value, prop_schema, current_path)
                        elif prop_schema.get("type") == "array" and "items" in prop_schema:
                            if isinstance(value, list):
                                for i, item in enumerate(value):
                                    item_path = f"{current_path}[{i}]"
                                    item_schema = prop_schema["items"]
                                    if "pattern" in item_schema:
                                        validate_pattern(item, item_schema["pattern"], item_path)
                                    if item_schema.get("type") == "object":
                                        validate_recursive(item, item_schema, item_path)
        
        validate_recursive(data, schema)
        return len(errors) == 0, errors

