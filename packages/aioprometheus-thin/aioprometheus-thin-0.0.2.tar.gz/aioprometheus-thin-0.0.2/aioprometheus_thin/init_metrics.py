from aioprometheus_thin.configs import MetricsTypes


class Metric:
    def __init__(self, name: str, description: str, metric_type: MetricsTypes, const_labels: dict):
        """
        Inits Metric object
        :param name:
        :param description:
        :param metric_type:
        :param const_labels:
        """
        self.name = name
        self.description = description
        self.metric_type = metric_type.name
        self.const_labels = const_labels
        self.metric = metric_type.value(name, description, const_labels=const_labels)
