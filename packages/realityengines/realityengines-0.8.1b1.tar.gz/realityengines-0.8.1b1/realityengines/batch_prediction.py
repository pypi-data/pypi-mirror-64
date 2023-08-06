from .deployment import Deployment


class BatchPrediction():
    '''

    '''

    def __init__(self, client, batchPredictionId=None, status=None, deploymentId=None, dataSource=None, outputLocation=None, predictionsStartedAt=None, predictionsCompletedAt=None, deployment={}):
        self.client = client
        self.id = batchPredictionId
        self.batch_prediction_id = batchPredictionId
        self.status = status
        self.deployment_id = deploymentId
        self.data_source = dataSource
        self.output_location = outputLocation
        self.predictions_started_at = predictionsStartedAt
        self.predictions_completed_at = predictionsCompletedAt
        self.deployment = client._build_class(Deployment, deployment)

    def __repr__(self):
        return f"BatchPrediction(batch_prediction_id={repr(self.batch_prediction_id)}, status={repr(self.status)}, deployment_id={repr(self.deployment_id)}, data_source={repr(self.data_source)}, output_location={repr(self.output_location)}, predictions_started_at={repr(self.predictions_started_at)}, predictions_completed_at={repr(self.predictions_completed_at)}, deployment={repr(self.deployment)})"

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.id == other.id

    def to_dict(self):
        return {'batch_prediction_id': self.batch_prediction_id, 'status': self.status, 'deployment_id': self.deployment_id, 'data_source': self.data_source, 'output_location': self.output_location, 'predictions_started_at': self.predictions_started_at, 'predictions_completed_at': self.predictions_completed_at, 'deployment': self.deployment.to_dict() if self.deployment else None}
