
import os
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexerClient
from cfg.config import OpenAIServiceConfig, SqlDBconnection, BlobConnection

from azure.search.documents.indexes.models import (
    SearchIndexer,
    FieldMapping
)
def indexer():
    """_summary_
    """
    CONFIG = OpenAIServiceConfig()
    CONFIG_SQL = SqlDBconnection()

    endpoint=CONFIG.endpoint
    credential=CONFIG.credential
    index_name=CONFIG.index_name


    #index_name=os.environ['AZURE_SEARCH_INDEX']
    indexer_name = f'{index_name}-indexer'
    skillset_name = f'{index_name}-skillset'  
    data_source_name =f'{index_name}-datastore'
    #endpoint = os.environ['AZURE_SEARCH_SERVICE_ENDPOINT']
    #credential = AzureKeyCredential(os.environ['AZURE_SEARCH_ADMIN_KEY']) if len(os.environ['AZURE_SEARCH_ADMIN_KEY']) > 0 else DefaultAzureCredential()

    indexer = SearchIndexer(  
        name=indexer_name,  
        description='Indexer to index documents and generate embeddings',  
        skillset_name=skillset_name,  
        target_index_name=index_name,  
        data_source_name=data_source_name,  
        field_mappings=[FieldMapping(source_field_name='id', target_field_name='chunk_id'),
                        FieldMapping(source_field_name='title', target_field_name='title'),
                        FieldMapping(source_field_name='content', target_field_name='chunk')]  
    )  

    indexer_client = SearchIndexerClient(endpoint, credential)  
    indexer_result = indexer_client.create_or_update_indexer(indexer)  

    indexer_client.run_indexer(indexer_name)