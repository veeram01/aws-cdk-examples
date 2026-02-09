# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import boto3
import os
import json
import logging
import uuid

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb_client = boto3.client("dynamodb")


def log_structured(level, message, **kwargs):
    """Helper function for structured JSON logging"""
    log_entry = {
        "level": level,
        "message": message,
        **kwargs
    }
    logger.info(json.dumps(log_entry))


def handler(event, context):
    table = os.environ.get("TABLE_NAME")
    request_id = context.request_id
    
    log_structured(
        "INFO",
        "Processing request",
        table_name=table,
        request_id=request_id
    )
    
    if event["body"]:
        item = json.loads(event["body"])
        log_structured(
            "INFO",
            "Received payload",
            item=item,
            request_id=request_id
        )
        year = str(item["year"])
        title = str(item["title"])
        id = str(item["id"])
        
        dynamodb_client.put_item(
            TableName=table,
            Item={"year": {"N": year}, "title": {"S": title}, "id": {"S": id}},
        )
        
        log_structured(
            "INFO",
            "Successfully inserted data",
            item_id=id,
            request_id=request_id
        )
        
        message = "Successfully inserted data!"
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": message}),
        }
    else:
        log_structured(
            "INFO",
            "Received request without payload, using default data",
            request_id=request_id
        )
        
        default_id = str(uuid.uuid4())
        dynamodb_client.put_item(
            TableName=table,
            Item={
                "year": {"N": "2012"},
                "title": {"S": "The Amazing Spider-Man 2"},
                "id": {"S": default_id},
            },
        )
        
        log_structured(
            "INFO",
            "Successfully inserted default data",
            item_id=default_id,
            request_id=request_id
        )
        
        message = "Successfully inserted data!"
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": message}),
        }
