import os
from flask import Flask, render_template
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Initialize Flask application
app = Flask(__name__)

# Azure Key Vault Configuration
KEY_VAULT_URL = "https://cdi-vault.vault.azure.net/"  # ✅ Fixed double slash

def get_storage_connection_string_from_keyvault():
    """Retrieve Azure Storage connection string from Key Vault."""
    try:
        print("🔑 Attempting to authenticate with Azure Key Vault...")  # Debug log
        
        # Authenticate with DefaultAzureCredential
        credential = DefaultAzureCredential()
        secret_client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

        # Retrieve the secret
        secret = secret_client.get_secret("ConnectionStringBlob")
        print("✅ Successfully retrieved connection string from Key Vault.")  # Debug log
        return secret.value

    except Exception as e:
        print(f"❌ Error retrieving secret from Key Vault: {str(e)}")  # Debug log
        return None  # Return None instead of an error message

# Fetch the connection string from Key Vault
AZURE_CONNECTION_STRING = get_storage_connection_string_from_keyvault()

if AZURE_CONNECTION_STRING is None:
    print("❌ Exiting: Could not retrieve the connection string. Check Key Vault permissions.")
    exit(1)  # Stop execution if Key Vault authentication fails

# Azure Storage Configuration
CONTAINER_NAME = "jamiecontainer"
BLOB_NAME = "Secret Recipe 3 2.txt"

def get_recipe_from_blob():
    """Fetch recipe content from Azure Blob Storage."""
    try:
        print(f"🔍 Fetching blob '{BLOB_NAME}' from container '{CONTAINER_NAME}'")  # Debug log
        
        # Initialize Blob Service Client
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        blob_client = container_client.get_blob_client(BLOB_NAME)

        # Download the recipe
        blob_data = blob_client.download_blob()
        recipe_content = blob_data.readall().decode('utf-8')
        
        print("✅ Successfully retrieved recipe content.")  # Debug log
        return recipe_content

    except Exception as e:
        print(f"❌ Error retrieving recipe: {str(e)}")  # Debug log
        return f"❌ Error retrieving recipe: {str(e)}"

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
    print(f"📜 Recipe content preview: {recipe_text[:100]}...")  # Debug log, first 100 chars
    return render_template('recipe.html', recipe=recipe_text)

# Run the Flask application
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  # ✅ Use PORT from environment variable
    print(f"🚀 Flask application is starting on port {port}...")  # Debug log
    app.run(host='0.0.0.0', port=port, debug=True)  # ✅ Binds to all interfaces
