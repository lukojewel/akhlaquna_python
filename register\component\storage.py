from azure.storage.blob import BlockBlobService
from config.config import AZURE_STORAGE_ACCOUNT_NAME,AZURE_STORAGE_KEY,AZURE_STORAGE_CONTAINER
from azure.storage.blob import ContentSettings

block_blob_service = BlockBlobService(account_name=AZURE_STORAGE_ACCOUNT_NAME, account_key=AZURE_STORAGE_KEY)

def upload_file(file_name, file_type, name_to_save):
	result = block_blob_service.create_blob_from_path(
	    AZURE_STORAGE_CONTAINER,
	    name_to_save,
	    file_name,
	    content_settings=ContentSettings(content_type=file_type)
	)