from azure.search.documents.indexes import SearchIndexClient
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from cfg.config import OpenAIServiceConfig, SqlDBconnection, BlobConnection

from dotenv import load_dotenv
from azure.search.documents.indexes.models import (
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    HnswAlgorithmConfiguration,
    HnswParameters,
    VectorSearchAlgorithmMetric,
    ExhaustiveKnnAlgorithmConfiguration,
    ExhaustiveKnnParameters,
    VectorSearchProfile,
    AzureOpenAIVectorizer,
    AzureOpenAIParameters,
    SemanticConfiguration,
    SemanticSearch,
    SemanticPrioritizedFields,
    SemanticField,
    SearchIndex
)
import os
#load_dotenv(override=True)

def search_index():
    """_summary_
    """
    
    CONFIG = OpenAIServiceConfig()
    CONFIG_SQL = SqlDBconnection()

    endpoint=CONFIG.endpoint
    credential=CONFIG.credential
    index_name=CONFIG.index_name
    azure_openai_endpoint=CONFIG.azure_openai_endpoint
    azure_openai_embedding_deployment=CONFIG.azure_openai_embedding_deployment
    azure_openai_key=CONFIG.azure_openai_key

    #endpoint = os.environ['AZURE_SEARCH_SERVICE_ENDPOINT']
    #credential = AzureKeyCredential(os.environ['AZURE_SEARCH_ADMIN_KEY']) if len(os.environ['AZURE_SEARCH_ADMIN_KEY']) > 0 else DefaultAzureCredential()
    #index_name = os.environ['AZURE_SEARCH_INDEX']
    #azure_openai_endpoint=os.environ['AZURE_OPENAI_ENDPOINT']
    #azure_openai_embedding_deployment=os.environ['AZURE_OPENAI_EMBEDDING_DEPLOYMENT']
    #azure_openai_key=os.environ['AZURE_OPENAI_KEY']


    index_client = SearchIndexClient(endpoint=endpoint, credential=credential)  

    fields = [  
        SearchField(name='parent_id', # key column for azure ai search
                    type=SearchFieldDataType.String,
                    sortable=True,
                    filterable=True,
                    facetable=True),  
        SearchField(name='title',
                    type=SearchFieldDataType.String),  
        SearchField(name='chunk_id',
                    type=SearchFieldDataType.String,
                    key=True,
                    sortable=True,
                    filterable=True,
                    facetable=True,
                    analyzer_name='keyword'),  
        SearchField(name='chunk',
                    type=SearchFieldDataType.String,
                    sortable=False,
                    filterable=False,
                    facetable=False),  
        SearchField(name='vector',
                    type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                    vector_search_dimensions=1536,
                    vector_search_profile_name='myHnswProfile'),  
    ]  
    
    vector_search = VectorSearch(  
        algorithms=[  
            HnswAlgorithmConfiguration(  
                name='myHnsw',  
                parameters=HnswParameters(  
                    m=4,  
                    ef_construction=400,  
                    ef_search=500,  
                    metric=VectorSearchAlgorithmMetric.COSINE,  
                ),  
            ),  
            ExhaustiveKnnAlgorithmConfiguration(  
                name='myExhaustiveKnn',  
                parameters=ExhaustiveKnnParameters(  
                    metric=VectorSearchAlgorithmMetric.COSINE,  
                ),  
            ),  
        ],  
        profiles=[  
            VectorSearchProfile(  
                name='myHnswProfile',  
                algorithm_configuration_name='myHnsw',  
                vectorizer='myOpenAI',  
            ),  
            VectorSearchProfile(  
                name='myExhaustiveKnnProfile',  
                algorithm_configuration_name='myExhaustiveKnn',  
                vectorizer='myOpenAI',  
            ),  
        ],  
        vectorizers=[  
            AzureOpenAIVectorizer(  
                name='myOpenAI',  
                kind='azureOpenAI',  
                azure_open_ai_parameters=AzureOpenAIParameters(  
                    resource_uri=azure_openai_endpoint,  
                    deployment_id=azure_openai_embedding_deployment,  
                    api_key=azure_openai_key,  
                ),  
            ),  
        ],  
    )  

    semantic_config = SemanticConfiguration(  
        name='my-semantic-config',  
        prioritized_fields=SemanticPrioritizedFields(  
            content_fields=[SemanticField(field_name='chunk')]  
        ),  
    )  
    
    semantic_search = SemanticSearch(configurations=[semantic_config])  
    
    index = SearchIndex(name=index_name,
                        fields=fields,
                        vector_search=vector_search,
                        semantic_search=semantic_search)  

    result = index_client.create_or_update_index(index)