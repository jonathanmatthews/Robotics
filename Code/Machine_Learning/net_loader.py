# import json

# def load_json(filename):
#     with open(filename, 'r') as filename:
#         print(filename.read())
#         return json.loads(filename.read())

# def json_to_dict(json):
#     """
#     Takes json file and converts it to python dictionary
#     Args:
#         json: raw data from json file
#     Returns:
#         json converted to dictionary
#     """
#     completed_dict = {}
#     for key, value in json.items():
#         completed_dict[key] = value
#     return completed_dict

# json = load_json('neural_net.json')
# data = json_to_dict(json)

from neural_net import neural_net

print neural_net