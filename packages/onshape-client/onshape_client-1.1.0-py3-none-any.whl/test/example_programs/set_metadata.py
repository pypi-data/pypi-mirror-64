import json
from datetime import datetime

from onshape_client.client import Client
from onshape_client.utility import load_json


# For updating many properties of many elements
class BulkMetadataUpdate(object):
    def __init__(self, primary_metadata_body):
        # The primary metadata_body defines the wvm against which to update the metadata
        self.primary_metadata_body = primary_metadata_body
        self.additional_metadata_calls = []

    def add_metadata_body(self, metadata_body):
        self.additional_metadata_calls.append(metadata_body)

    def get_merged_bodies(self):
        body = self.primary_metadata_body.body
        # merge the bodies
        for metadata_body in self.additional_metadata_calls:
            body["items"].extend(metadata_body.body["items"])
        return body

    def send(self):
        body = self.get_merged_bodies()
        onshape_element = self.primary_metadata_body.onshape_element
        self.metadata = Client.get_client().metadata_api.update_wv_metadata(
            onshape_element.did,
            onshape_element.wvm,
            onshape_element.wvmid,
            body,
            _preload_content=False,
        )


# For updating multiple properties of a single Onshape element
class MetaDataBody(object):
    def __init__(self, onshape_element):
        self.body = {"items": []}
        self.onshape_element = onshape_element
        self.__element_property_map = None
        self.__part_property_map = None
        self.__part_index_to_part_id_map = None

    @property
    def element_property_map(self):
        if not self.__element_property_map:
            self.__element_property_map = (
                self.get_element_property_name_to_property_id_map()
            )
        return self.__element_property_map

    @property
    def part_index_to_pid_map(self):
        if not self.__part_index_to_part_id_map:
            (
                self.__part_property_map,
                self.__part_index_to_part_id_map,
            ) = self.get_part_property_name_to_property_id_map()
        return self.__part_index_to_part_id_map

    @property
    def part_property_map(self):
        if not self.__part_property_map:
            (
                self.__part_property_map,
                self.__part_index_to_part_id_map,
            ) = self.get_part_property_name_to_property_id_map()
        return self.__part_property_map

    def add_to_element_metadata(self, property_name, new_val, eid=None):
        """If needed, can specify other element metadata"""
        try:
            if not eid:
                eid = self.onshape_element.eid
            to_be_appended = {
                "properties": [
                    {
                        "value": new_val,
                        "propertyId": self.element_property_map[eid][property_name],
                    }
                ],
                "href": self.make_element_href(eid),
            }
            self.body["items"].append(to_be_appended)
        except:
            pass

    def add_to_part_metadata(self, property_name, new_val, pid=None, p_index=0):
        """Select part either by pid OR by the part index."""
        try:
            if not pid:
                pid = self.part_index_to_pid_map[p_index]
            to_be_appended = {
                "properties": [
                    {
                        "value": new_val,
                        "propertyId": self.part_property_map[pid][property_name],
                    }
                ],
                "href": self.make_part_href(pid),
            }
            self.body["items"].append(to_be_appended)
        except:
            pass

    def get_element_property_name_to_property_id_map(self):
        """Get the element metadata for the workspace/version and build the map"""
        client = Client.get_client()
        property_map = {}
        response = client.metadata_api.get_wv_es_metadata(
            self.onshape_element.did,
            self.onshape_element.wvm,
            self.onshape_element.wvmid,
            _preload_content=False,
        )
        data = json.loads(response.data)
        for element in data["items"]:
            eid = element["elementId"]
            property_map[eid] = {}
            props_to_be_added = property_map[eid]
            for property in element["properties"]:
                props_to_be_added[property["name"]] = property["propertyId"]
        return property_map

    def get_part_property_name_to_property_id_map(self):
        """Get the part property map for the element in the particular version and build out the property map"""
        client = Client.get_client()
        property_map = {}
        part_index_to_part_id = []
        el = self.onshape_element
        response = client.metadata_api.get_wmve_ps_metadata(
            el.did, el.wvm, el.wvmid, el.eid, _preload_content=False
        )
        data = load_json(response)
        for i, part in enumerate(data["items"]):
            partId = part["partId"]
            part_index_to_part_id.append(partId)
            property_map[partId] = {}
            props_to_be_added = property_map[partId]
            for property in part["properties"]:
                props_to_be_added[property["name"]] = property["propertyId"]
        return property_map, part_index_to_part_id

    def make_element_href(self, eid):
        return (
            Client.get_client().configuration.host
            + "/api/metadata/d/"
            + self.onshape_element.did
            + "/"
            + self.onshape_element.wvm
            + "/"
            + self.onshape_element.wvmid
            + "/e/"
            + eid
        )

    def make_part_href(self, pid):
        return self.make_element_href(self.onshape_element.eid) + "/p/{}".format(pid)

    def send(self):
        """Update the element metadata as seen fit."""
        self.metadata = Client.get_client().metadata_api.update_wv_metadata(
            self.onshape_element.did,
            self.onshape_element.wvm,
            self.onshape_element.wvmid,
            self.body,
        )


def update_one_element_metadata_example():
    from onshape_client.onshape_url import OnshapeElement

    print("Now updating a single property within a single element")
    element = OnshapeElement(
        "https://cad.onshape.com/documents/31e9fe5e53feb43633f360f4/w/052a282a976da47ba4c305dd/e/a270fe6f3d3ddc0dd6aee29c"
    )
    metadata_class = MetaDataBody(element)
    metadata_class.add_to_part_metadata(
        "Part number", "my glorious part number", pid="JHD"
    )
    metadata_class.send()


def update_many_element_metadata_example():
    from onshape_client.onshape_url import OnshapeElement

    print("Now updating multiple properties in many elements")

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    element1 = OnshapeElement(
        "https://cad.onshape.com/documents/31e9fe5e53feb43633f360f4/w/052a282a976da47ba4c305dd/e/a270fe6f3d3ddc0dd6aee29c"
    )
    metadata_class1 = MetaDataBody(element1)
    metadata_class1.add_to_part_metadata(
        "Part number", "my glorious part number! " + time, pid="JHD"
    )

    element2 = OnshapeElement(
        "https://cad.onshape.com/documents/31e9fe5e53feb43633f360f4/w/052a282a976da47ba4c305dd/e/d329ef11b727b097da599eb6"
    )
    metadata_class2 = MetaDataBody(element2)
    metadata_class2.add_to_part_metadata(
        "Description", "my wicked desciption! " + time, pid="JHD"
    )

    element3 = OnshapeElement(
        "https://cad.onshape.com/documents/31e9fe5e53feb43633f360f4/w/052a282a976da47ba4c305dd/e/e252cef9464938dc28356295"
    )
    metadata_class3 = MetaDataBody(element3)
    metadata_class3.add_to_part_metadata("Name", "my amazing name! " + time, pid="JHD")

    bulk_metadata = BulkMetadataUpdate(metadata_class1)
    bulk_metadata.add_metadata_body(metadata_class2)
    bulk_metadata.add_metadata_body(metadata_class3)

    bulk_metadata.send()


def test_set_metadata():
    update_one_element_metadata_example()
    update_many_element_metadata_example()
