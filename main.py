from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexerClient
from azure.search.documents.indexes.models import SearchIndexerDataSourceConnection, SearchIndexerDataContainer
from cfg.config import OpenAIServiceConfig, SqlDBconnection, BlobConnection
from azure.search.documents.indexes import SearchIndexClient
from cfg.config import OpenAIServiceConfig, SqlDBconnection, BlobConnection
from datasource import datasource
from search_index import search_index
from skillset import skillset

CONFIG = OpenAIServiceConfig()
def main():
    """_summary_
    """
    STORAGE = False
    try:
        storage = datasource()
        print(f'the data store {CONFIG.index_name}-datastore successfully created')
        STORAGE=True
        if STORAGE:
            print(f'Starting the creation of index {CONFIG.index_name} --------')
            indexes = search_index()
            print(f'The indexes {CONFIG.index_name} was successfully created. Yay!')
            print(f'Starting the creation of skillset {CONFIG.index_name}-skillset --------')
            skillsets = skillset()
            print(f'the skillsets {CONFIG.index_name}-skillset was successfully created')
    except Exception as e:
        print('the error is here: ', str(e))
        
if __name__ == "__main__":
    main()