import pytest
import json
from trustar_engineering import properties_search, get_property_value

json_string = '{\
                "guid": "1234", \
                "content": { \
                            "type": "text/html",\
                            "title": "Challenge 1",\
                            "entities": ["1.2.3.4", "wannacry", "malware.com", {"owner": "Jeff Bezos"}]\
                           },\
                "score": 74,\
                "time": 1574879179,\
                "backdoors": ["injection"]\
            }'


def test_properties_search():
    expected = {
        'guid': '1234',
        'content.entities[3].owner': 'Jeff Bezos',
        'score': 74,
        'backdoors[0]': 'injection'
    }
    properties = ["guid", "content.entities[3].owner", "score",
                  "score.sign", "backdoors[0]", "", None, "backdoors[1]"]

    result = properties_search(json_string, properties)
    assert result == expected


def test_get_property_value():

    res_empty_index = get_property_value("backdoors[]", json.loads(json_string))
    assert res_empty_index is None
    res_invalid_index = get_property_value("backdoors[34]", json.loads(json_string))
    assert res_invalid_index is None
    res_invalid_list_name = get_property_value("[0]", json.loads(json_string))
    assert res_invalid_list_name is None


if __name__ == "__main__":
    pytest.main()
