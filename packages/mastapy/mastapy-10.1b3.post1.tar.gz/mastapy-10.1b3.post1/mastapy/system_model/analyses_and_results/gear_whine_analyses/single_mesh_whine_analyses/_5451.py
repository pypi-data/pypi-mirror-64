'''_5451.py

ExternalCADModelSingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model import _1993
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6109
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5428
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'ExternalCADModelSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalCADModelSingleMeshWhineAnalysis',)


class ExternalCADModelSingleMeshWhineAnalysis(_5428.ComponentSingleMeshWhineAnalysis):
    '''ExternalCADModelSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _EXTERNAL_CAD_MODEL_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExternalCADModelSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1993.ExternalCADModel':
        '''ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1993.ExternalCADModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6109.ExternalCADModelLoadCase':
        '''ExternalCADModelLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6109.ExternalCADModelLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
