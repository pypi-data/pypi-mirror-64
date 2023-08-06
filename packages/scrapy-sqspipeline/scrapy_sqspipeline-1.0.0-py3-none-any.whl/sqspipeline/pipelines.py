import json
import boto3
from scrapy.utils.serialize import ScrapyJSONEncoder


class SQSPipeline:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler.stats)

    def __init__(self, settings, stats):
        self.queue_url = settings['SQSPIPELINE_QUEUE_URL']
        self.queue_name = settings['SQSPIPELINE_QUEUE_NAME']

        if not self.queue_url and not self.queue_name:
            raise ValueError('Either SQSPIPELINE_QUEUE_URL or SQSPIPELINE_QUEUE_NAME is required.')

        sqs = boto3.resource(
            'sqs',
            aws_access_key_id=settings['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=settings['AWS_SECRET_ACCESS_KEY'],
            endpoint_url=settings['AWS_ENDPOINT_URL'],
            region_name=settings['AWS_REGION_NAME'],
            use_ssl=settings['AWS_USE_SSL'],
            verify=settings['AWS_VERIFY'],
        )

        if self.queue_url:
            self.queue = sqs.Queue(self.queue_url)
        else:
            self.queue = sqs.get_queue_by_name(QueueName=self.queue_name)

        self.stats = stats

    def process_item(self, item, spider):
        try:
            self.queue.send_message(
                MessageBody=json.dumps(item, ensure_ascii=False, cls=ScrapyJSONEncoder),
                MessageAttributes={
                    'spider_name': {
                        'DataType': 'String',
                        'StringValue': spider.name,
                    },
                    'item_name': {
                        'DataType': 'String',
                        'StringValue': item.__class__.__name__,
                    },
                }
            )
        except:
            self.stats.inc_value('pipeline/sqs/fail')
            raise
        else:
            self.stats.inc_value('pipeline/sqs/success')

        return item
