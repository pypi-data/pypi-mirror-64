from .Writer import Writer
from azure.storage.blob import BlockBlobService
import json
import pandas as pd


class ADLSWriter(Writer):
    """
        Write dataframe/json to specified blob storage location
    """
    def __init__(self, account_name, account_key, container_name, storage_name, dataflow_name):
        self.account_name = account_name
        self.account_key = account_key
        self.container_name = container_name
        self.storage_name = storage_name
        self.dataflow_name = dataflow_name
    
    def write_df(self, blob_location, dataframe):
        """
            Write dataframe to specified blob storage location
        """
        dataframe = dataframe.to_csv(index=False, header=False)
        block_blob_service = BlockBlobService(account_name=self.account_name, account_key=self.account_key)
        block_blob_service.create_blob_from_text(self.container_name,self.dataflow_name+"/"+ blob_location, dataframe)
        blob_url = 'https://'+self.storage_name+'.dfs.core.windows.net/'+self.container_name+'/'+blob_location
        return blob_url

    def write_df(self, blob_location, dataframe, number_of_partition=1):
        """
            Write dataframe to specified blob storage location
        """
        #TODO partition the python df
        dataframe = dataframe.to_csv(index=False, header=False)
        block_blob_service = BlockBlobService(account_name=self.account_name, account_key=self.account_key)
        block_blob_service.create_blob_from_text(self.container_name + "/" + self.dataflow_name, blob_location, dataframe)
        blob_url = 'https://'+self.storage_name+'.dfs.core.windows.net/'+self.container_name+'/'+blob_location
        return blob_url