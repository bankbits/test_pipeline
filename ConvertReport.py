import json
import pymongo
from pymongo import MongoClient
import bson
from bson import ObjectId
import sys

#########################################
# Connect to the mongodb server
#########################################

client_url = "mongodb://bfmongoadmin:safe4now@9.45.93.21/"


database = sys.argv[1]
table_url = sys.argv[2]
client_url += database + "." + table_url

client = MongoClient(client_url)

bfa_db = client[database]

# Locate the report you need:
# Input the ObjectId of the report you want to convert
object = sys.argv[3]

# ######################################
# Generate the record from the specified report
# ######################################

col = bfa_db[table_url]

cursor = col.find({ "_id":ObjectId(object)})
document = cursor[0]

#print("\nThe output of the original report: \n")
#print (document)

"""
Site type true: all sites
Site type false: per site
Have different columnschema formats
"""
site_type = True

'''
Returns the site id for the record name
'''
def site_id():
    if(site_type): return "All Sites "
    else: return "Per Site "

'''
Generates the record human readable description
'''
def gen_desc(report_inf):
    desc_types = report_inf[0]['columnSchemas']
    desc = "Connection counts for "

    for d in desc_types:
        desc += d['title'] + " "
    return desc

db_report = document
report_info = db_report['report']
report_params = db_report['parameters']

# the generated record object from the mongodb report
gen_record = {

        "bfa_reports":[{
        "ID": table_url + "_" + object,
        "Name": str(db_report["name"]) + "_" + object,
        "Description": str(gen_desc(report_info)),
        "SourceType": 'MONGO',
        "SourceParameter": {
            "host":"mongodb://9.45.93.21",
            "port":"27017",
            "database":"bfmongodb",
            "table": str(table_url)
        },
        "Parameters": {
            "report_id": str(report_params['report_id']),
            "start_date": str(report_params['start_date']),
            "end_date": str(report_params['end_date']),
            "classs": str(report_params['classs']),
            "sub_class": str(report_params['sub_class']),
            "types": str(report_params['types']),
            "sub_type": str(report_params['sub_type']),
            "org": str(report_params['org']),
            "account": str(report_params['account']),
            "message_id": str(report_params['message_id'])
        },
        "Metadata": {

        }
        }]
}   

#print("\nThe generated record:\n")

#final_cmd = "bluefringe CRUDReportRegistry createReportRegistry --data \'" + json.dumps(gen_record) + "\'"
#print(final_cmd)


print(gen_record)
# print(json.dumps(gen_record))
#print(json.loads(json.dumps(gen_record)))


with open(str(object) + '.json', 'w') as outfile:
    json.dump(gen_record, outfile)


