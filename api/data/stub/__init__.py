import exceptions
from .. import DataController
from ProvidenceClarity.data.data import DataStub, DataBackend, FORMAT_LIST, ORIGIN_LIST
from ProvidenceClarity.data.input import DataInput

class StubController(DataController):
    

    @classmethod
    def create(cls, backend, format, origin=None, source=None, **kwargs):
        
            d = DataStub()
        
            # Backend first
            if isinstance(backend, DataBackend):
                d.backend = backend
            elif isinstance(backend, (str, basestring, unicode)):
                d.backend = DataBackend.get_by_key_name(backend)
            else:
                raise exceptions.InvalidDataBackend()
               
            # Process format
            if format in FORMAT_LIST:
                f.format = format
            else:
                f.format = 'other'
                f.format_other = format
                
            # Process origin
            if origin in ORIGIN_LIST:
                f.origin = origin
            else:
                f.origin = 'other'
                f.origin_other = origin
                
            # Process source
            if source is not None:
                if isinstance(source, DataInput):
                    d.source = source
                else:
                    raise exceptions.InvalidDataSource()
                    
            # Process kwargs
            if 'key_name' in kwargs:
                del kwargs['key_name']
            
            
            