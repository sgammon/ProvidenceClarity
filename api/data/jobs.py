from . import DataController
from google.appengine.ext import db
from ProvidenceClarity.data.data import DataJobTemplate, DataJob, DataJobEntry
from ProvidenceClarity.data.core.model import Model


class JobController(DataController):

    
    def create(self):
        pass
        
        
    @classmethod
    def expandTemplate(cls, template, in_data):
        
        if isinstance(template, (str, basestring, unicode)):
            d = DataJobTemplate.get_by_key_name(template)
            
        elif isinstance(template, Model):
            d = template
            
        else:
            return False ## @TODO: Error Handling here plz
        
        job = DataJob.put()
        
        entries = []

        for item in d.entries:

            entries.append(DataJobEntry(job, job=job, in_data=in_data))
            