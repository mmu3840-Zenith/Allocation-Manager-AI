import json

class MetricsPipeline:
    def export(self, results):
        with open('analysis/results.json','w') as f:
            json.dump(results,f)
