import requests
import json
import pprint
import time
from pymongo import MongoClient

# Streamsets credentials
auth = ('admin', 'admin')

# Streamsets url config
streamsets_root_url = 'http://bfstreamsets.innovate.ibm.com'
streamsets_port = '18630'
streamsets_url = streamsets_root_url + ':' + streamsets_port

originTargetList = [
    'conf.resourceUrl',
    'conf.remoteConfig.remoteAddress',
    'httpConfigs.port'
]
destinationTargetList = [
    'configBean.mongoConfig.connectionString',
    'solrURI',
    'zookeeperConnect'
]
def config_to_url(stage_configuration, URLList, targetList):
    for config_entry in stage_configuration:
        for supported_config_entry in targetList:
            if config_entry['name'] == supported_config_entry:
                URLList.append(config_entry['value'])
                return URLList
    return URLList

def add_origins_destinations(pipeline, pipeline_info):
    originStages = []
    destinationStages = []
    for stage in pipeline['stages']:
        if len(stage['inputLanes']) == 0:
            originStages.append(stage)
        if len(stage['outputLanes']) == 0:
            destinationStages.append(stage)
    pipeline_info['originStageNames'] = []
    pipeline_info['originURLs'] = []
    for stage in originStages:
        pipeline_info['originStageNames'].append(stage['instanceName'])
        pipeline_info['originURLs'] = config_to_url(stage['configuration'], pipeline_info['originURLs'], originTargetList)
    pipeline_info['destinationStageNames'] = []
    pipeline_info['destinationURLs'] = []
    for stage in destinationStages:
        pipeline_info['destinationStageNames'].append(stage['instanceName'])
        pipeline_info['destinationURLs'] = config_to_url(stage['configuration'], pipeline_info['destinationURLs'], destinationTargetList)
    return pipeline_info

def collect_pipeline_info(pipelineId):
    pipeline = requests.get(streamsets_url + "/rest/v1/pipeline/" + pipelineId, auth=auth).json() 
    pipeline_metadata = requests.get(streamsets_url + "/rest/v1/pipelines/status", auth=auth).json()[pipelineId]    
    pipeline_info = {}
    pipeline_info['pipelineId'] = pipeline['pipelineId']
    pipeline_info['title'] = pipeline['title']
    pipeline_info['description'] = pipeline['description']
    pipeline_info['status'] = pipeline_metadata['status']
    pipeline_info['pipeline_url'] = streamsets_url + "/collector/pipeline/" + pipelineId

    pipeline_info = add_origins_destinations(pipeline, pipeline_info)

    #pprint.pprint(pipeline)
    return pipeline_info

all_pipelines_brief_info = requests.get(streamsets_url + "/rest/v1/pipelines/", auth=auth).json()
current_pipelines = []
'''
for pipeline_brief in all_pipelines_brief_info:
    current_pipelines.append(collect_pipeline_info(pipeline_brief['pipelineId']))
    print(collect_pipeline_info(pipeline_brief['pipelineId']))
    print('\n')
'''
pipeline_brief = all_pipelines_brief_info[0]
print(collect_pipeline_info(pipeline_brief['pipelineId']))
