#from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexerClient
from azure.search.documents.indexes.models import SearchIndexerDataSourceConnection, SearchIndexerDataContainer
from cfg.config import OpenAIServiceConfig, SqlDBconnection, BlobConnection
import os

#load_dotenv(override=True) 

def datasource():
    """_summary_
    """

    CONFIG = OpenAIServiceConfig()
    CONFIG_SQL = SqlDBconnection()
    CONFIG_BLOB = BlobConnection()


    endpoint = CONFIG.endpoint
    credential = CONFIG.credential
    #endpoint = os.environ['AZURE_SEARCH_SERVICE_ENDPOINT']
    #credential = AzureKeyCredential(os.environ['AZURE_SEARCH_ADMIN_KEY']) if len(os.environ['AZURE_SEARCH_ADMIN_KEY']) > 0 else DefaultAzureCredential()

    #index_name = os.environ['AZURE_SEARCH_INDEX']
    index_name = CONFIG.index_name
    #data_source=os.environ['AZURE_SEARCH_DATA_SOURCE']
    #azure_openai_endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
    #azure_openai_key = os.environ['AZURE_OPENAI_KEY'] if len(os.environ['AZURE_OPENAI_KEY']) > 0 else None
    #azure_openai_embedding_deployment = os.environ['AZURE_OPENAI_EMBEDDING_DEPLOYMENT']

    data_source=f'{index_name}-datastore'
    #connecting to azure sql database
    #######################################################
    #server_name=os.environ['SQL_SERVER_NAME']
    #database_name=os.environ['SQL_DB_NAME']
    #user_id=os.environ['SQL_USER_ID']
    #password=os.environ['SQL_PASSWORD']


    sql_connection_string='Server=CONFIG_SQL.server_name;Database=CONFIG_SQL.database_name;User ID=CONFIG_SQL.user_id;Password=CONFIG_SQL.password;Trusted_Connection=False;Encrypt=True;Connection Timeout=30;'
    #sql_connection_string = 'Server=server_name;Database=database_name;Uid=user_id;Pwd:password;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    sql_table_name = 'articles'

    indexer_client =SearchIndexerClient(endpoint, credential)
    container =SearchIndexerDataContainer(name=sql_table_name)
    data_source_connection =SearchIndexerDataSourceConnection(
        name=f'{data_source}',
        type='azuresql',
        connection_string=sql_connection_string,
        container=container
    )
    data_sources = indexer_client.create_or_update_data_source_connection(data_source_connection)
    #########################################################
    #########################################################
    #connecting to azure blob storage
    #storage_name= os.environ['STORAGE_NAME']
    #storage_key=os.environ['STORAGE_KEY']
    #storage_connection_string=os.environ['STORAGE_CONNECTION_STRING']

    #blob_name =os.environ['BLOB_NAME']
    # 
    #indexer_client =SearchIndexerClient(endpoint, credential)
    #container =SearchIndexerDataContainer(name=blob_name)
    #data_source_connection =SearchIndexerDataSourceConnection(
    #    name='integrated-azure-blob-index',
    #    type='azureblob',
    #    connection_string=storage_connection_string,
    #    container=container
    #)
    #data_source = indexer_client.create_or_update_data_source_connection(data_source_connection)
    ###########################################################