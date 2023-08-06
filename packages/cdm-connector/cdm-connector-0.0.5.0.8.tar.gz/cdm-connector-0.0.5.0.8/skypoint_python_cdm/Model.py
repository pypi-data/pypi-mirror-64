from .DataObject import DataObject
from .SchemaEntry import SchemaEntry
from .Entity import EntityCollection
from .Entity import Entity
from .LocalEntity import LocalEntity
from .Annotation import AnnotationCollection
from .Relationship import RelationshipCollection
from .SingleKeyRelationship import SingleKeyRelationship
from .Reference import ReferenceCollection
from .Attribute import Attribute
from .Annotation import Annotation
from .AttributeReference import AttributeReference
from .Partition import Partition
from .Partition import PartitionCollection
from .utils import String
from .utils import dtype_converter
from datetime import datetime
import pandas as pd
import numpy as np
import json
import pprint
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


class Model(DataObject):
    
    def __init__(self, from_json=False, json_data=None, 
                        application=config['DEFAULT']['application'], 
                        name=config['DEFAULT']['name'], 
                        description=config['DEFAULT']['description'], 
                        version=config['DEFAULT']['version'],
                        culture=None,
                        modified_time=None):

        self.schema = [
            SchemaEntry("application", String),
            SchemaEntry("name", String),
            SchemaEntry("description", String),
            SchemaEntry("version", String),
            SchemaEntry("culture", String),
            SchemaEntry("modifiedTime", String),
            SchemaEntry("isHidden", bool),
            SchemaEntry("entities", EntityCollection),
            SchemaEntry("annotations", AnnotationCollection),
            SchemaEntry("relationships", RelationshipCollection),
            SchemaEntry("referenceModels", ReferenceCollection)
        ]
        super().__init__(self.schema)
        
        if from_json:
            self.application = json_data.get("application", None)
            self.name = json_data["name"]
            self.description = json_data.get("description", None)
            self.version = json_data["application"]
            self.culture = json_data.get("culture", None)
            self.modifiedTime = json_data.get("modifiedTime", None)
            self.isHidden = json_data.get("isHidden", None)

            self.entities = EntityCollection.fromJson(json_data["entities"])

            annotations = json_data.get("annotations", None)
            if annotations is not None:
                self.annotations = AnnotationCollection.fromJson(annotations)

            relationships = json_data.get("relationships", None)
            if relationships is not None:
                self.relationships = RelationshipCollection.fromJson(relationships)

            referenceModels = json_data.get("referenceModels", None)
            if referenceModels is not None:
                self.referenceModels = ReferenceCollection.fromJson(referenceModels)

        else:
            self.application = application
            self.name = name
            self.description = description
            self.version = version
            self.culture = culture
            self.modifiedTime = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')


    def add_entity(self, entity):
        for entity_index in range(len(self.entities)):
            if self.entities[entity_index].name.lower() == entity.name.lower():
                self.entities[entity_index] = entity
                break
        else:
            self.entities.append(entity)

    def add_relationship(self, from_attribute_entity_name, from_attribute_attribute_name,
                               to_attribute_entity_name, to_attribute_attribute_name):
        from_attribute = AttributeReference()
        from_attribute.entityName = from_attribute_entity_name
        from_attribute.attributeName = from_attribute_attribute_name

        to_attribute = AttributeReference()
        to_attribute.entityName = to_attribute_entity_name
        to_attribute.attributeName = to_attribute_attribute_name

        relationship = SingleKeyRelationship()
        relationship.fromAttribute = from_attribute
        relationship.toAttribute = to_attribute
        
        self.relationships.append(relationship)

    @staticmethod
    def generate_entity(dataframe, name, description=None, _dtype_converter=None):
        entity = LocalEntity()
        entity.name = name
        entity.description = description

        if _dtype_converter is None:
            _dtype_converter = dtype_converter

        for column_name, column_datatype in (dataframe.dtypes).items():
            attribute = Attribute()
            attribute.name = column_name
            attribute.dataType = _dtype_converter.get(column_datatype, 'string')
            entity.attributes.append(attribute)
        return entity

    @staticmethod
    def add_annotation(name, value, obj):
        """
        Annotations can be added at root level (model.json),
        entity level or attribute level.
        obj is an object in which if "annotations" is present
        then new annotation will be added.
        """
        annotation = Annotation()
        annotation.name = name
        annotation.value = value
        obj.annotations.append(annotation)
        return True


    def toJson(self):
        result = dict()
        result["application"] = self.application
        result["name"] = self.name
        result["description"] = self.description
        result["version"] = self.version
        result["culture"] = self.culture
        result["modifiedTime"] = self.modifiedTime
        result["isHidden"] = self.isHidden
        result["entities"] = self.entities.toJson()
        result["annotations"] = self.annotations.toJson()
        result["relationships"] = self.relationships.toJson()
        result["referenceModels"] = self.referenceModels.toJson()
        return result

    def write_to_storage(self, entity_name, dataframe, writer, number_of_partition=None):
        entity = None
        entity_index = -1
        for _entity_index, _entity in enumerate(self.entities):
            if _entity.name.lower() == entity_name.lower():
                entity = _entity
                entity_index = _entity_index
                break
        else:
            return AssertionError("Passed entity is not a part of current model.json")

        if number_of_partition is None:
            number_of_partition = 5
        if isinstance(dataframe, pd.DataFrame):
            dfs = np.array_split(dataframe, number_of_partition)
        else:
            dfs = dataframe.randomSplit([1.0 for _ in range(number_of_partition)])
        
        partitions = PartitionCollection()

        for index in range(number_of_partition):
            location  = '{entity_name}/{entity_name}.csv.snapshots/{entity_name}{index}.csv'.format(entity_name=entity_name, index=index)
            url = writer.write_df(location, dfs[index])

            partition = Partition()
            partition.name = '{entity_name}{index}.csv'.format(entity_name=entity_name, index=index)
            partition.location = url
            partition.refreshTime = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')

            partitions.append(partition)

        self.entities[entity_index].partitions = partitions

        model_json = self.toJson()
        writer.write_json("model.json", model_json)
        return

    def read_from_storage(self, entity_name, reader):
        entity = None
        entity_index = -1
        for _entity_index, _entity in enumerate(self.entities):
            if _entity.name.lower() == entity_name.lower():
                entity = _entity
                entity_index = _entity_index
                break
        else:
            return AssertionError("Passed entity is not a part of current model.json")
        
        locations = []
        for partition in self.entities[entity_index].partitions:
            locations.append(partition.location)

        headers = []
        dtypes = []
        attributes = self.entities[entity_index].attributes
        for attribute in attributes:
            headers.append(attribute.name)
            dtypes.append({attribute.name: attribute.dataType})

        dataframe = reader.read_df(locations, headers, dtypes)
        return dataframe