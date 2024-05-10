from os import getenv
from azure.storage.fileshare.aio import ShareClient


class FileShare:

    def __init__(self):
        connectio_string = getenv("STORAGE_CONNECTION_STRING")
        file_share_name = getenv("FILE_SHARE_NAME")

        self.service = ShareClient.from_connection_string(
            conn_str=connectio_string,
            share_name=file_share_name,
        )

    async def __select_all_files(self, file_ext):
        """
        Get all unprocessed files names
        file_ext: should be passed without dot in the beginning
        return: names of files only!
        """

        all_files_names = []
        # Get items that have specific ext
        async for file in self.service.list_directories_and_files():
            if file['name'].endswith('.' + file_ext):
                all_files_names.append(file['name'])
        self.service.close()
        return all_files_names
    
    async def __clear_up_file(self, file_name, binar_file):
        """
        Deletes files for root dir that was processed by AI Document Intelligence
        But beforehand renames them and moves to processed forlder
        file_name: string 
        binar_fiele: binary
        returt: true or false with error
        """

        file_client = self.service.get_file_client(
            f"processed/processed_{file_name.replace(' ', '_')}"
            )
        try:
            await file_client.upload_file(binar_file)
            # Creates directory_client to delete file
            directory_client = self.service.get_directory_client()
            await directory_client.delete_file(file_name)
            self.service.close()
            return 1
        except Exception as e:
            print(e)
            self.service.close()
            return 0, e

    async def read_file(self):
        """
        Request to get files from file share
        then add's them to dictionary for further manipulations 
        """ 

        all_data = {}
        all_unprocesed_files = await self.__select_all_files("pdf")
        for file in all_unprocesed_files:
            file_client = self.service.get_file_client(file)
            stream = await file_client.download_file()
            await self.__clear_up_file(file, await stream.content_as_bytes())
            all_data[file] = await stream.readall()
        await self.service.close()
        return all_data