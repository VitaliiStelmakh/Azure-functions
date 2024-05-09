from os import getenv
from azure.storage.fileshare.aio import ShareClient


class FileShare:

    def __init__(self):
        connectio_string = getenv("FILE_SHARE_CONNECTION_STRING")
        file_share_name = getenv("FILE_SHARE_NAME")

        self.service = ShareClient.from_connection_string(
            conn_str=connectio_string,
            share_name=file_share_name,
        )

    async def __select_all_files(self, file_ext):
        """
        Get all unprocessed files names
        file_ext: should be passed without dot in the beginning
        """
        all_files_names = []

        # Get items that have specific ext
        async for file in self.service.list_directories_and_files():
            if file['name'].endswith('.' + file_ext):
                all_files_names.append(file['name'])
        
        return all_files_names

    async def read_file(self):
        """
        Request to get file from file share 
        """
        # TODO refactor this function to save file localy then send it to Azure AI Document Intelligence 
        # test = await self.__select_all_files("txt")
        # return test
        
        all_data = []
        all_unprocesed_files = await self.__select_all_files("pdf")
        for file in all_unprocesed_files:
            file_client = self.service.get_file_client(file)
            stream = await file_client.download_file()
            all_data.append(await stream.readall())
        return all_data #stream.readall()
        # stream = await self.service.download_file()
        # return stream.readall()
