﻿'''_4310.py

StraightBevelDiffGearSetModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model.gears import _2082
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6184
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4309, _4308, _4225
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'StraightBevelDiffGearSetModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetModalAnalysisAtAStiffness',)


class StraightBevelDiffGearSetModalAnalysisAtAStiffness(_4225.BevelGearSetModalAnalysisAtAStiffness):
    '''StraightBevelDiffGearSetModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2082.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2082.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6184.StraightBevelDiffGearSetLoadCase':
        '''StraightBevelDiffGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6184.StraightBevelDiffGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def straight_bevel_diff_gears_modal_analysis_at_a_stiffness(self) -> 'List[_4309.StraightBevelDiffGearModalAnalysisAtAStiffness]':
        '''List[StraightBevelDiffGearModalAnalysisAtAStiffness]: 'StraightBevelDiffGearsModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsModalAnalysisAtAStiffness, constructor.new(_4309.StraightBevelDiffGearModalAnalysisAtAStiffness))
        return value

    @property
    def straight_bevel_diff_meshes_modal_analysis_at_a_stiffness(self) -> 'List[_4308.StraightBevelDiffGearMeshModalAnalysisAtAStiffness]':
        '''List[StraightBevelDiffGearMeshModalAnalysisAtAStiffness]: 'StraightBevelDiffMeshesModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesModalAnalysisAtAStiffness, constructor.new(_4308.StraightBevelDiffGearMeshModalAnalysisAtAStiffness))
        return value
