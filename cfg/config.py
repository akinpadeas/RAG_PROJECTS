import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential

load_dotenv(override=True)

class SqlDBconnection:
    """ SQL Configuration """
    
    server_name=os.environ['SQL_SERVER_NAME']
    database_name=os.environ['SQL_DB_NAME']
    user_id=os.environ['SQL_USER_ID']
    password=os.environ['SQL_PASSWORD']
    
class BlobConnection:
    """ Blob Configuration """
    
    blob_name =os.environ['BLOB_NAME']
    storage_name= os.environ['STORAGE_NAME']
    storage_key=os.environ['STORAGE_KEY']
    storage_connection_string=os.environ['STORAGE_CONNECTION_STRING']
    
class OpenAIServiceConfig:
    """ Open AI Service Configuration """
    
    endpoint = os.environ['AZURE_SEARCH_SERVICE_ENDPOINT']
    credential = AzureKeyCredential(os.environ['AZURE_SEARCH_ADMIN_KEY']) if len(os.environ['AZURE_SEARCH_ADMIN_KEY']) > 0 else DefaultAzureCredential()
    index_name = os.environ['AZURE_SEARCH_INDEX']
    azure_openai_endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
    azure_openai_key = os.environ['AZURE_OPENAI_KEY'] if len(os.environ['AZURE_OPENAI_KEY']) > 0 else None
    azure_openai_embedding_deployment = os.environ['AZURE_OPENAI_EMBEDDING_DEPLOYMENT']