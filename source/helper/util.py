import os
def filter_features_by_type(source_dict, schema_list):
    """
    Creates a filtered dictionary based on a schema list of (name, type).
    
    Args:
        source_dict (dict): The dictionary containing raw data (e.g., from a form).
        schema_list (list): List of tuples (feature_name, expected_type).
        
    Returns:
        dict: Filtered data containing only valid keys with correct types.
    """
    cleaned_data = {}
    
    hasher = {
        "integer" : int,
        "string" : str
    }

    for feature_name, expected_type in schema_list:
        # 1. Check if the key exists in the source dictionary
        if feature_name in source_dict:
            value = source_dict[feature_name]
            
            # 2. Check if the value matches the expected data type
            hash_type = hasher[expected_type.lower()]
            if isinstance(value, hash_type):
                cleaned_data[feature_name] = value

            if value == "" and hash_type is not str:
                continue
                
            try:
                # Attempt to cast the value (e.g., int("45") -> 45)
                converted_value = hash_type(value)
                cleaned_data[feature_name] = converted_value
            except (ValueError, TypeError):
                # If conversion fails (e.g., int("high")), skip this feature
                continue
                
    return cleaned_data

# 'postgresql://postgres:password@localhost:5432/my_auth_db'

class Congfi():
    def __init__(self):
        self.DBUSERNAME = os.getenv("POSTGRES_USER","postgres")
        self.DBPASSWORD = os.getenv("DB_PASSWORD_FILE","password")
        self.DBHOST = os.getenv("POSTGRES_HOST","localhost")
        self.DBPORT = os.getenv("POSTGRES_PORT","5432")
        self.DBDB = os.getenv("POSTGRES_DB","my_auth_db")
    def createDatabaseUrl(self):
        print("connecting to")
        databaseUrl = "postgresql://{}:{}@{}:{}/{}".format(self.DBUSERNAME,self.DBPASSWORD,self.DBHOST,self.DBPORT,self.DBDB)
        print(databaseUrl)
        return databaseUrl
CONF = Congfi()