
class ProactiveBucket(object):
    """
    Represents a generic proactive bucket
    """

    def __init__(self, gateway, bucket_name=None):
        self._bucket_name = bucket_name
        self._gateway = gateway
        self._base_url = gateway.base_url
        self._runtime_gateway = gateway.getRuntimeGateway()

    def __str__(self):
        return self.getBucketName()

    def __repr__(self):
        return self.getBucketName()

    def getBucketName(self):
        return self._bucket_name
