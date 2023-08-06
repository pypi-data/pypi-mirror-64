# Scrapy SQS Pipeline

[![PyPI version](https://badge.fury.io/py/scrapy-sqspipeline.svg)](https://badge.fury.io/py/scrapy-sqspipeline)

Each time this pipeline receives an item, it sends it to SQS.

## Requirements

* Python 3+
* Scrapy 1.1+
* boto3

## Installation

```shell script
pip3 install scrapy-sqspipeline
```
 
## Configuration

1. Add the following lines to your Scrapy project settings.
    ```python
    ITEM_PIPELINES = {
       'sqspipeline.SQSPipeline': 100,
    }
   
    # Either `SQSPIPELINE_QUEUE_URL` or `SQSPIPELINE_QUEUE_NAME` is required.
    SQSPIPELINE_QUEUE_URL='https://sqs.ap-northeast-1.amazonaws.com/xxxxxxxxxx/scrapy-sqspipeline'
    # SQSPIPELINE_QUEUE_NAME=''
    ```

1. Use AWS CLI's `aws configure` command to set up credentials. Alternatively, you can use Scrapy's settings `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.
