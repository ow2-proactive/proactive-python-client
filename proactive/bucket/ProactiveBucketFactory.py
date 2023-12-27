from .ProactiveAiMachineLearningBucket import ProactiveAiMachineLearningBucket

class ProactiveBucketFactory:
    @staticmethod
    def getBucket(gateway, bucket_name):
        if bucket_name == 'ai-machine-learning':
            return ProactiveAiMachineLearningBucket(gateway)
        else:
            return ValueError("Unknown bucket name: " + bucket_name)

    def getBucketList(self):
        return ['ai-machine-learning']
