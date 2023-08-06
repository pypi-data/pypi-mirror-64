'''_3714.py

WormGearSetCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2088
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3712, _3713, _3650
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3593
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'WormGearSetCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetCompoundParametricStudyTool',)


class WormGearSetCompoundParametricStudyTool(_3650.GearSetCompoundParametricStudyTool):
    '''WormGearSetCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2088.WormGearSet':
        '''WormGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2088.WormGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2088.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2088.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def worm_gears_compound_parametric_study_tool(self) -> 'List[_3712.WormGearCompoundParametricStudyTool]':
        '''List[WormGearCompoundParametricStudyTool]: 'WormGearsCompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsCompoundParametricStudyTool, constructor.new(_3712.WormGearCompoundParametricStudyTool))
        return value

    @property
    def worm_meshes_compound_parametric_study_tool(self) -> 'List[_3713.WormGearMeshCompoundParametricStudyTool]':
        '''List[WormGearMeshCompoundParametricStudyTool]: 'WormMeshesCompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesCompoundParametricStudyTool, constructor.new(_3713.WormGearMeshCompoundParametricStudyTool))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3593.WormGearSetParametricStudyTool]':
        '''List[WormGearSetParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3593.WormGearSetParametricStudyTool))
        return value

    @property
    def assembly_parametric_study_tool_load_cases(self) -> 'List[_3593.WormGearSetParametricStudyTool]':
        '''List[WormGearSetParametricStudyTool]: 'AssemblyParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyParametricStudyToolLoadCases, constructor.new(_3593.WormGearSetParametricStudyTool))
        return value
