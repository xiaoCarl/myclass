import boto3
from moto import mock_s3
from s3demo import MyModel


@mock_s3
def test_my_model_1():
    # conn = boto3.resource('s3', region_name='us-east-1')
    # We need to create the bucket since this is all in Moto's 'virtual' AWS account
    # conn.create_bucket(Bucket='mybucket')

    model_instance = MyModel('mybucket')
   
    model_instance.save('steve','is awesome')
 
    body = model_instance.get('steve')
    # body = conn.Object('mybucket', 'steve').get()['Body'].read().decode("utf-8")

    assert body == 'is awesome'


def test_my_model_2():
    with mock_s3():
        model_instance = MyModel('mybucket')
        model_instance.save('steve','is awesome1')
        body = model_instance.get('steve')

        assert body == 'is awesome1'


def test_my_model_3():
    mock = mock_s3()
    mock.start()

    model_instance = MyModel('mybucket')
    model_instance.save('steve','is awesome2')
    body = model_instance.get('steve')

    assert body == 'is awesome2'
