'''_5890.py

SpringDamperHalfDynamicAnalysis
'''


from mastapy.system_model.part_model.couplings import _2131
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6179
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5829
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_HALF_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'SpringDamperHalfDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperHalfDynamicAnalysis',)


class SpringDamperHalfDynamicAnalysis(_5829.CouplingHalfDynamicAnalysis):
    '''SpringDamperHalfDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_HALF_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperHalfDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2131.SpringDamperHalf':
        '''SpringDamperHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2131.SpringDamperHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6179.SpringDamperHalfLoadCase':
        '''SpringDamperHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6179.SpringDamperHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
