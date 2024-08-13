from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexerClient
from cfg.config import OpenAIServiceConfig, SqlDBconnection, BlobConnection

from azure.search.documents.indexes.models import (
    SplitSkill,
    InputFieldMappingEntry,
    OutputFieldMappingEntry,
    AzureOpenAIEmbeddingSkill,
    SearchIndexerIndexProjections,
    SearchIndexerIndexProjectionSelector,
    SearchIndexerIndexProjectionsParameters,
    IndexProjectionMode,
    SearchIndexerSkillset
)
import os

#load_dotenv(override=True)
def skillset():
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

    skillset_name = f'{index_name}-skillset'  

    split_skill = SplitSkill(  
        description='Split skill to chunk documents',  
        text_split_mode='pages',  
        context='/document',  
        maximum_page_length=1000,  
        page_overlap_length=200,  
        inputs=[  
            InputFieldMappingEntry(name='text',
                                source='/document/content'),  
        ],  
        outputs=[  
            OutputFieldMappingEntry(name='textItems',
                                    target_name='pages')  
        ],
        default_language_code='en'
    )  

    # TEXT MUST BE LESS THAN 8000 TOKENS
    embedding_skill = AzureOpenAIEmbeddingSkill(  
        description='Skill to generate embeddings via Azure OpenAI',  
        context='/document/pages/*',  
        resource_uri=azure_openai_endpoint,  
        deployment_id=azure_openai_embedding_deployment,  
        api_key=azure_openai_key,  
        inputs=[  
            InputFieldMappingEntry(name='text',
                                source='/document/pages/*'),  
        ],  
        outputs=[  
            OutputFieldMappingEntry(name='embedding',
                                    target_name='vector')  
        ],  
    )  

    index_projections = SearchIndexerIndexProjections(  
        selectors=[  
            SearchIndexerIndexProjectionSelector(  
                target_index_name=index_name,  
                parent_key_field_name='parent_id',  
                source_context='/document/pages/*',  
                mappings=[  
                    InputFieldMappingEntry(name='chunk', source='/document/pages/*'),  
                    InputFieldMappingEntry(name='vector', source='/document/pages/*/vector'),  
                    InputFieldMappingEntry(name='title', source='/document/title'),  
                ],  
            ),  
        ],  
        parameters=SearchIndexerIndexProjectionsParameters(  
            projection_mode=IndexProjectionMode.INCLUDE_INDEXING_PARENT_DOCUMENTS  
        ),  
    ) 

    skillset = SearchIndexerSkillset(  
        name=skillset_name,  
        description='Skillset to chunk documents and generating embeddings',  
        skills=[split_skill, embedding_skill],  
        index_projections=index_projections,  
    ) 

    client = SearchIndexerClient(endpoint, credential)
    client.create_or_update_skillset(skillset)