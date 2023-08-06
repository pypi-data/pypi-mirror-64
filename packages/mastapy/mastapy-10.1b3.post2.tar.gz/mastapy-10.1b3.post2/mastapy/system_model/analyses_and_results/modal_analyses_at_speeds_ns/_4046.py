'''_4046.py

StraightBevelDiffGearSetModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model.gears import _2062
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6164
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4045, _4044, _3959
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'StraightBevelDiffGearSetModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetModalAnalysesAtSpeeds',)


class StraightBevelDiffGearSetModalAnalysesAtSpeeds(_3959.BevelGearSetModalAnalysesAtSpeeds):
    '''StraightBevelDiffGearSetModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2062.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2062.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6164.StraightBevelDiffGearSetLoadCase':
        '''StraightBevelDiffGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6164.StraightBevelDiffGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def straight_bevel_diff_gears_modal_analyses_at_speeds(self) -> 'List[_4045.StraightBevelDiffGearModalAnalysesAtSpeeds]':
        '''List[StraightBevelDiffGearModalAnalysesAtSpeeds]: 'StraightBevelDiffGearsModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsModalAnalysesAtSpeeds, constructor.new(_4045.StraightBevelDiffGearModalAnalysesAtSpeeds))
        return value

    @property
    def straight_bevel_diff_meshes_modal_analyses_at_speeds(self) -> 'List[_4044.StraightBevelDiffGearMeshModalAnalysesAtSpeeds]':
        '''List[StraightBevelDiffGearMeshModalAnalysesAtSpeeds]: 'StraightBevelDiffMeshesModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesModalAnalysesAtSpeeds, constructor.new(_4044.StraightBevelDiffGearMeshModalAnalysesAtSpeeds))
        return value
