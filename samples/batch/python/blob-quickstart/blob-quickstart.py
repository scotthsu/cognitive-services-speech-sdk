import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

try:
    print("Azure Blob Storage Python quickstart sample")
    os.environ['AZURE_STORAGE_CONNECTION_STRING']='DefaultEndpointsProtocol=https;AccountName=scotthsuspeech2text;AccountKey=fH463owsrgC/YZ9qyGkz91mPD/4WXPDoNhEHHh8BuzJ+74hOdz0JNx/FuHyn6SjDKyGgvUi5Pvej+AStlUXElw==;EndpointSuffix=core.windows.net'    
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(connect_str or "")

    # Create the container
    container_name = "audio-test-container"
#    container_client = blob_service_client.create_container(container_name)

    # Create a blob client using the local file name as the name for the blob
    local_file_name = "mayday_audio.wav"
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

    # Upload the created file
    upload_file_path = "e:\\temp\\mayday_audio.wav"  
#    with open(file=upload_file_path, mode="rb") as data:
#        blob_client.upload_blob(upload_file_path)

    print("\nListing blobs...")
    # List the blobs in the container
#    blob_list = container_client.list_blobs()
#    for blob in blob_list:
#        if blob.name:
#            print("\t" + blob.name)

    # Create a SAS token to use to authenticate a new client
    from datetime import datetime, timedelta
    from azure.storage.blob import ResourceTypes, AccountSasPermissions, generate_account_sas

    # https://learn.microsoft.com/en-us/azure/storage/common/storage-samples-python?toc=%2Fazure%2Fstorage%2Fblobs%2Ftoc.json&bc=%2Fazure%2Fstorage%2Fblobs%2Fbreadcrumb%2Ftoc.json#blob-samples
    # https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/storage/azure-storage-blob/samples/blob_samples_authentication.py#L110
    sas_token = generate_account_sas(
        blob_service_client.account_name or "",
        account_key=blob_service_client.credential.account_key,
        resource_types=ResourceTypes(object=True),
        permission=AccountSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )
    
    # https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/storage/azure-storage-blob/samples/blob_samples_containers.py#L146    
    # [START generate_sas_token]
    # Use access policy to generate a sas token
    from azure.storage.blob import generate_container_sas
    
#    sas_token = generate_container_sas(
#        container_client.account_name or "",
#        container_client.container_name,
#        account_key=container_client.credential.account_key,
#        policy_id='my-access-policy-id'
#    )
    # [END generate_sas_token]

    from azure.storage.blob import generate_blob_sas, BlobSasPermissions

    sas_token = generate_blob_sas(
        blob_client.account_name or "",
        blob_client.container_name,
        blob_client.blob_name,
        resource_types=ResourceTypes(object=True),
        permission=BlobSasPermissions(read=True),
        account_key=blob_service_client.credential.account_key,
        expiry=datetime.utcnow() + timedelta(hours=1)
    )
    print(f"\nListing blobs using SAS token...{sas_token}")

except Exception as ex:
    print('Exception:')
    print(ex)