from azure.storage.blob import BlockBlobService
from Writer import Writer
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

    def write_json(self, blob_location, json_dict):
        """
        write json to specified blob storage location
        """
        json_dict = json.dumps(json_dict)
        block_blob_service = BlockBlobService(
            account_name=self.account_name, account_key=self.account_key)
        block_blob_service.create_blob_from_text(self.container_name,self.dataflow_name+"/"+ blob_location, json_dict)
        blob_url = 'https://'+self.storage_name+'.dfs.core.windows.net/'+self.container_name+'/'+blob_location
        return blob_url