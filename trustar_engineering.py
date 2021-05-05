import json
import re
import github

# Regular expression to validate that the property
# defines an item value to be searched inside of a
# list at certain index (i.e. 'entities[0]')
regex_item_in_list = re.compile(r'^(.+)\[(\d+)\]$')


# Function that takes a JSON string representing the object that contains
# all the info, and a list of properties (strings) that need to be searched
# inside the object structure. The function returns a dictionary where the
# key is the property searched and the value is the one gathered from the object.
def properties_search(json_s, properties):
    # Convert JSON string into a Python object
    json_object = json.loads(json_s)
    # Obtain all the properties values
    prop_values = {prop: get_property_value(prop, json_object) for prop in properties if prop}
    # Filter out the dictionary items that have None values
    return {key: value for key, value in prop_values.items() if value}


# Auxiliary function that take the property to be found along with the entire
# JSON object and return the corresponding value if the property exist.
def get_property_value(prop, json_object):
    item = None
    # Split the property defined with dot notation
    for i, prop in enumerate(prop.split(".")):
        # Check if the property is indicating to obtain an item
        # inside of a list (i.e. property name: 'entities[0]')
        is_item_in_list = regex_item_in_list.match(prop)

        if i == 0 and not is_item_in_list:
            item = json_object.get(prop, None)
        elif is_item_in_list:
            item = get_item_from_list(json_object if i == 0 else item, prop)
        elif isinstance(item, dict):
            item = item.get(prop, None)
        else:
            item = None

    return item


# Auxiliary function to obtain an item from a list. The
# first input param is the item in which the list will
# be first retrieved, and the second is the property
# that holds both, the list name and the item index.
def get_item_from_list(item, prop):
    list_name, item_index = get_list_name_and_item_index(prop)
    items = item.get(list_name, None)
    if items and item_index < len(items):
        item = items[item_index]
    else:
        item = None
    return item


# Auxiliary function to that takes a property as input
# parameter that holds a list name and an item index.
# It return the list name and index parsed from the
# input string.
def get_list_name_and_item_index(prop):
    list_name = regex_item_in_list.match(prop).group(1)
    item_index = regex_item_in_list.match(prop).group(2)
    return list_name, int(item_index)


if __name__ == "__main__":
    fields = ["id", "objects[0].name", "objects[0].kill_chain_phases"]
    g = github.Github("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")
    repo = g.get_user().get_repo("cti")
    for file in repo.get_contents("enterprise-attack/attack-pattern"):
        print(properties_search(file.decoded_content, fields))
