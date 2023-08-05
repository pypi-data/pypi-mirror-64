'''_5843.py

MassDiscDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _1981
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6125
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5888
from mastapy._internal.python_net import python_net_import

_MASS_DISC_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'MassDiscDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MassDiscDynamicAnalysis',)


class MassDiscDynamicAnalysis(_5888.VirtualComponentDynamicAnalysis):
    '''MassDiscDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _MASS_DISC_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MassDiscDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1981.MassDisc':
        '''MassDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1981.MassDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6125.MassDiscLoadCase':
        '''MassDiscLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6125.MassDiscLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[MassDiscDynamicAnalysis]':
        '''List[MassDiscDynamicAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(MassDiscDynamicAnalysis))
        return value
