import logging
import sys
import boto3
from datetime import datetime

def config_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    sh.setFormatter(
        logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    )
    logger.addHandler(sh)
    return logger

def get_table_details(glue_table_spec):
    return {
        "Name": glue_table_spec.get('Name'),
        "CreateTime": glue_table_spec.get('CreateTime').replace(tzinfo=None),
        "UpdateTime": glue_table_spec.get('UpdateTime').replace(tzinfo=None),
        "UpdatedLatency": datetime.now() - glue_table_spec.get('UpdateTime').replace(tzinfo=None),
        "recordCount": glue_table_spec.get('Parameters').get('recordCount'),
    }

def glue_fetch(db_name, next_token=None, max_results=10):
    glue = boto3.client('glue')
    return glue.get_tables(
        DatabaseName=db_name,
        MaxResults=max_results,
        NextToken=next_token
    )
    
def get_glue_tables(DB_NAME):

    next_token = ""
    full_tables_list = list()

    while next_token is not None:

        # Retrieve glue tables from catalog
        glue_tables = glue_fetch(DB_NAME, next_token)

        logging.debug("Looping glue results")
        for tb in glue_tables.get('TableList'):
            full_tables_list.append(get_table_details(tb))

        next_token=glue_tables.get('NextToken')
        logging.debug("Fetching glue tables for NextToken: {}".format(next_token))


    logging.debug("Glue database tables count: {}".format(len(full_tables_list)))

    return full_tables_list