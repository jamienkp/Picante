import os
from flask import Flask, render_template
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Initialize the Flask application
app = Flask(__name__)

# Azure Key Vault Configuration
KEY_VAULT_URL = "https://cdi-keyvault.vault.azure.net/"

def get_storage_connection_string_from_keyvault():
    """Retrieve Azure Storage connection string from Key Vault"""
    try:
        # Use DefaultAzureCredential to authenticate
        credential = DefaultAzureCredential()
        secret_client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

        # Retrieve the connection string secret
        secret = secret_client.get_secret("CDI-ConnectionStringBlob")  # Correct secret name
        print(f"🔑 Retrieved connection string from Key Vault.")  # Debugging log
        return secret.value

    except Exception as e:
        print(f"⚠️ Error retrieving secret from Key Vault: {str(e)}")  # Debug log
        return f"⚠️ Error retrieving secret from Key Vault: {str(e)}"

# Fetch the connection string from Key Vault
AZURE_CONNECTION_STRING = get_storage_connection_string_from_keyvault()

print(f"Connection String: {AZURE_CONNECTION_STRING}")  # Debug print for connection string

# Azure Storage Configuration
CONTAINER_NAME = "cdicontainer"
BLOB_NAME = "Secret Recipe 3 2.txt"

def get_recipe_from_blob():
    """Fetch recipe content from Azure Blob Storage"""
    try:
        print(f"🔍 Attempting to fetch blob: {BLOB_NAME} from container: {CONTAINER_NAME}") 
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        blob_client = container_client.get_blob_client(BLOB_NAME)

        blob_data = blob_client.download_blob()
        recipe_content = blob_data.readall().decode('utf-8')
        
        print(f"✅ Successfully retrieved recipe content.")
        return recipe_content

    except Exception as e:
        print(f"⚠️ Error retrieving recipe: {str(e)}")  
        return f"⚠️ Error retrieving recipe: {str(e)}"

@app.route('/')
def home():
    print("🔄 Serving home page.")  # Debug log
    return render_template('index.html')

@app.route('/about')
def about():
    print("🔄 Serving about page.")  # Debug log
    return render_template('about.html')

@app.route('/recipe')
def recipe():
    print("🔄 Serving recipe page.")  # Debug log
    recipe_text = get_recipe_from_blob()
    print(f"📜 Recipe content: {recipe_text[:100]}...")  # Debug log, printing the first 100 chars of the recipe
    return render_template('recipe.html', recipe=recipe_text)

# Run the Flask application
if __name__ == '__main__':
    print("🚀 Flask application is starting...")  # Debug log
    app.run(debug=True)
