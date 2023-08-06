'''_3502.py

HypoidGearParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2050
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6110
from mastapy.system_model.analyses_and_results.system_deflections import _2250
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3443
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'HypoidGearParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearParametricStudyTool',)


class HypoidGearParametricStudyTool(_3443.AGMAGleasonConicalGearParametricStudyTool):
    '''HypoidGearParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2050.HypoidGear':
        '''HypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2050.HypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6110.HypoidGearLoadCase':
        '''HypoidGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6110.HypoidGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2250.HypoidGearSystemDeflection]':
        '''List[HypoidGearSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2250.HypoidGearSystemDeflection))
        return value
