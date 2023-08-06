'''_3539.py

OilSealParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _2005
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6150
from mastapy.system_model.analyses_and_results.system_deflections import _2288
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3494
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'OilSealParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealParametricStudyTool',)


class OilSealParametricStudyTool(_3494.ConnectorParametricStudyTool):
    '''OilSealParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2005.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2005.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6150.OilSealLoadCase':
        '''OilSealLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6150.OilSealLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2288.OilSealSystemDeflection]':
        '''List[OilSealSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2288.OilSealSystemDeflection))
        return value
