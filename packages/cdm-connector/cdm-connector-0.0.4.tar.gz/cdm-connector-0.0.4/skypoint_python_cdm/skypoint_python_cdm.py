from Model import Model
import pandas as pd
from datetime import datetime
from Partition import Partition
from Partition import PartitionCollection
from ADLSWriter import ADLSWriter
from ADLSReader import ADLSReader
import json


if __name__ == "__main__":
    m = Model()

    df = {"country": ["Brazil", "Russia", "India", "China", "South Africa", "ParaSF"],
       "currentTime": [datetime.now(), datetime.now(), datetime.now(), datetime.now(), datetime.now(), datetime.now()],
       "area": [8.516, 17.10, 3.286, 9.597, 1.221, 2.222],
       "capital": ["Brasilia", "Moscow", "New Dehli", "Beijing", "Pretoria", "ParaSF"],
       "population": [200.4, 143.5, 1252, 1357, 52.98, 12.34] }
    df = pd.DataFrame(df)


    df2 = {"countryAA": ["AAA", "NNN", "UUU", "BBB", "HHH AAA"],
       "populationBB": [200.4, 143.5, 1252, 1357, 52.98],
       "currentTimeCC": [datetime.now(), datetime.now(), datetime.now(), datetime.now(), datetime.now()] }
    df2 = pd.DataFrame(df2)    

    entity = Model.generate_entity(df, "customEntity")
    m.add_entity(entity)
    entity3 = Model.generate_entity(df2, "customEntity3")
    entity3.partitions = PartitionCollection()
    p = Partition()
    p.name = "first"
    p.location = "foo/bar/first.csv"
    p.refreshTime = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
    entity3.partitions.append(p)
    m.add_entity(entity3)

    Model.add_annotation("modelJsonAnnotation", "modelJsonAnnotationValue", m)
    Model.add_annotation("annotationName", "annotationValue", entity3)
    Model.add_annotation("annotationName2", "annotationValue2", entity3.attributes[1])

    m.add_relationship("PeopleFromCalifornia", "skypointId", "Profile", "skypointId")

    writer = ADLSWriter("ACCOUNTNAME", "ACCOUNTKEY",
                        "CONTAINERNAME", "STORAGENAME", "DATAFLOWNAME")    
    
    reader = ADLSReader("ACCOUNTNAME", "ACCOUNTKEY",
                        "CONTAINERNAME", "STORAGENAME", "DATAFLOWNAME")    

    m.write_to_storage("customEntity", df, writer)

    read_df = m.read_from_storage("customEntity", reader)
    print(read_df)

    x = m.toJson()
    with open("foo.json", "w") as f:
        f.write(json.dumps(x))

    with open("foo.json") as f:
        x = json.load(f)

    m2 = Model(True, x)

    y = m2.toJson()
    with open("foo2.json", "w") as f:
        f.write(json.dumps(y))

    print(entity.name)
