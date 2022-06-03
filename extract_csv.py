# import json
# import time
# import pandas as pd
# from requests import get, post

# def extract_value(value):
#     """
#     Helper Method to Extract Cell Value from Response
#     """
#     if value['type'] == 'number':
#         return value['text']
#     elif value['type'] == 'string':
#         return value['valueString']
#     elif value['type'] == 'date':
#         return value['valueDate']            
#     elif value['type'] == 'time':
#         return value['valueTime']
#     elif value['type'] == 'phoneNumber':
#         return value['valuePhoneNumber']
#     elif value['type'] == 'object':
#         objectKeys = value['valueObject'].keys();
#         item_info = "" 
#         for ok in objectKeys:
#             item_info += ok + ":" + extract_value(value['valueObject'][ok]) + " "
#         return item_info
#     elif value['type'] == 'array':
#         itemInfo = ""
#         for item in value["valueArray"]:
#             itemInfo += extract_value(item) + "; "
#         return itemInfo[:-3] # ; 
#     else:
#         print("Skipping Unsupported Type")

# def recognizer2DF(post_url, apim_key, headers, data_bytes, confidence_threshold = 0, query_interval=5):
#     """
#     Submits Table or Form to recognizer asyncronously and processes the response
#     queryInterval amount of time to wait between checking whether a job is done
#     Optional confidence_threshold to deterimine whether to process a extracted feild 
#     """
#     try:
#         # Submit Async Table Job to Form Recognizer Endpoint 
#         resp = post(url = post_url, data = data_bytes, headers = headers)
#         if resp.status_code == 202:
#             # Query Submit Table Job
            
#             get_url = resp.headers["operation-location"]
             
#             resp = get(url = resp.headers["operation-location"], headers = {"Ocp-Apim-Subscription-Key": apim_key})
            
#             resp_json = json.loads(resp.text)
#             print(resp_json)
#             while resp_json["status"] == "running":
#                 resp = get(url = get_url, headers = {"Ocp-Apim-Subscription-Key": apim_key})
#                 resp_json = json.loads(resp.text)
#                 time.sleep(query_interval)
#             if resp_json["status"] == "succeeded":
#                 # Process Documents 
#                 docResults = resp_json['analyzeResult']['documentResults']
                
#                 docs = []
#                 for doc in docResults:
#                     fields = doc['fields']
#                     docs.append({key:extract_value(fields[key]) for key in fields.keys() \
#                                  if 'confidence' in fields[key] and fields[key]['confidence'] > confidence_threshold}) 
#                 return pd.DataFrame(docs)
#             elif resp_json["status"] == "failed":
#                 print("Layout analyze failed:\n%s" % resp_json)
#         else:
#             print("POST analyze failed:\n%s" % resp.text)     
#     except Exception as e:
#         print("Code Failed analyze failed:\n%s" % str(e))

# # Endpoint URL
# apim_key = 
# endpoint =  
# source = r'C:\Users\Hieu Tran\Documents\Source\hampton_house_apartment(multi).pdf'

# headers = {
#     # Request headers
#     'Content-Type': r'application/octet-stream',
#     'Ocp-Apim-Subscription-Key': apim_key,
# }

# with open(source, "rb") as f:
#     data_bytes = f.read()

# df = recognizer2DF(endpoint, apim_key, headers, data_bytes)
# df.to_csv("form_data.csv") # can now be processed with excel