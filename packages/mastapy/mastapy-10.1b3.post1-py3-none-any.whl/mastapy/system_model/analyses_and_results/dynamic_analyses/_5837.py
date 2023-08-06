'''_5837.py

DatumDynamicAnalysis
'''


from mastapy.system_model.part_model import _1990
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6096
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5815
from mastapy._internal.python_net import python_net_import

_DATUM_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'DatumDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumDynamicAnalysis',)


class DatumDynamicAnalysis(_5815.ComponentDynamicAnalysis):
    '''DatumDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _DATUM_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1990.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1990.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6096.DatumLoadCase':
        '''DatumLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6096.DatumLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
