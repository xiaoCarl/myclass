import boto3

ACCESS_KEY = 'AKIAS4L3SZT6DWQAXDA6'
SECRET_KEY = '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'
mybucket = 'myaaasdasdsbucke111'


class MyModel(object):
    def __init__(self, bucket):
        self.bucket = bucket
        self.resource = boto3.resource(
                        's3',
                         aws_access_key_id=ACCESS_KEY,
                         aws_secret_access_key=SECRET_KEY)
        self.resource.create_bucket(Bucket=bucket)

    def save(self,key,value):
        s3 = boto3.client(
                's3',
                aws_access_key_id=ACCESS_KEY,
                aws_secret_access_key=SECRET_KEY)
        s3.put_object(Bucket=self.bucket, Key=key, Body=value)

    def get(self,key):
        body = self.resource.Object(self.bucket, key).get()['Body'].read().decode()
        return body

    def get_all_bucket(self):
        buckets=[]
        for bucket in self.resource.buckets.all():
            buckets.append(bucket.name)
        return buckets


def s3_demo():
    moduel = MyModel(mybucket)
    moduel.save('caih','hahahaha')
    print(moduel.get('caih'))
    print(moduel.get_all_bucket())


if __name__ == "__main__" :
    s3_demo()


