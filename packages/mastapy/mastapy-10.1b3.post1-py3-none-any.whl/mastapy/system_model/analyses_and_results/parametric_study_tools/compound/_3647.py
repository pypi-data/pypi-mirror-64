'''_3647.py

FlexiblePinAssemblyCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _1994
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3516
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3687
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ASSEMBLY_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'FlexiblePinAssemblyCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAssemblyCompoundParametricStudyTool',)


class FlexiblePinAssemblyCompoundParametricStudyTool(_3687.SpecialisedAssemblyCompoundParametricStudyTool):
    '''FlexiblePinAssemblyCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _FLEXIBLE_PIN_ASSEMBLY_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FlexiblePinAssemblyCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1994.FlexiblePinAssembly':
        '''FlexiblePinAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1994.FlexiblePinAssembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1994.FlexiblePinAssembly':
        '''FlexiblePinAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1994.FlexiblePinAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3516.FlexiblePinAssemblyParametricStudyTool]':
        '''List[FlexiblePinAssemblyParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3516.FlexiblePinAssemblyParametricStudyTool))
        return value

    @property
    def assembly_parametric_study_tool_load_cases(self) -> 'List[_3516.FlexiblePinAssemblyParametricStudyTool]':
        '''List[FlexiblePinAssemblyParametricStudyTool]: 'AssemblyParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyParametricStudyToolLoadCases, constructor.new(_3516.FlexiblePinAssemblyParametricStudyTool))
        return value
