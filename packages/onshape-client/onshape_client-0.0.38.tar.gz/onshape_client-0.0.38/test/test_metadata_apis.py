import pytest
from onshape_client.oas import BTPartMetadataInfo, BTPartAppearanceInfo, BTColorInfo
import webbrowser
import json


@pytest.mark.parametrize("element", ["ps_configurable_cube"], indirect=True)
def test_change_color(client, element, new_copied_document_factory):
    """Test to change part color."""
    new_cube = new_copied_document_factory(element).part_studios[0]
    meta_data = BTPartMetadataInfo(
        appearance=BTPartAppearanceInfo(color=BTColorInfo(blue=0, green=0, red=255))
    )
    parts = client.parts_api.get_parts_wmve(
        did=new_cube.did, wvm=new_cube.wvm, wvmid=new_cube.wvmid, eid=new_cube.eid
    )
    client.parts_api.update_part_metadata(
        did=new_cube.did,
        wvm=new_cube.wvm,
        wvmid=new_cube.wvmid,
        eid=new_cube.eid,
        partid=parts[0].part_id,
        body=json.dumps([meta_data.to_dict()]),
    )
    parts = client.parts_api.get_parts_wmve(
        did=new_cube.did, wvm=new_cube.wvm, wvmid=new_cube.wvmid, eid=new_cube.eid
    )
    assert parts[0].appearance.color.red == 255
