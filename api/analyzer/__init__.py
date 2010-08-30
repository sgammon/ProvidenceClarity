from ProvidenceClarity import PCController
from .. import AdapterInterface
from . import mapper, object as obj, reducer, relation, stat


class AnalyzerController(PCController):

    _submodules = {mapper, obj, reducer, relation, stat}
    
    
class AnalyzerAdapter(AdapterInterface):
    pass
    
    
_controller = AnalyzerController