from azure.storage.blob.aio import ContainerClient
from json import dumps
from os import getenv
import logging
import uuid


class PushToBlob:

    def __init__(self):
        connection_string = getenv("STORAGE_CONNECTION_STRING")
        blob_container_name = getenv("BLOB_CONTAINER_NAME")

        self.blob_client = ContainerClient.from_connection_string(
            conn_str=connection_string,
            container_name=blob_container_name,
        )

    async def push_to_blob(self, data: dict):
        """
        Get's data processed by 
        data: dictionary with {name_of_file: {dict of returned pages}}
        """
        try:
            for key in data.keys():
                formated_name = f"{str(uuid.uuid4())[:8]}-{key.replace('.pdf', '.json')}"
                await self.blob_client.upload_blob(
                    formated_name, 
                    dumps(data[key])
                    )
            await self.blob_client.close()
            return True
        except Exception as e:
            logging.error(e)
            await self.blob_client.close()
            return e