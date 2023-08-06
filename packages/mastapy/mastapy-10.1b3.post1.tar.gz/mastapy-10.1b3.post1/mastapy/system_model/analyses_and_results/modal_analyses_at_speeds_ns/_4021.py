'''_4021.py

HypoidGearSetModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model.gears import _2071
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6132
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4020, _4019, _3967
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'HypoidGearSetModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetModalAnalysesAtSpeeds',)


class HypoidGearSetModalAnalysesAtSpeeds(_3967.AGMAGleasonConicalGearSetModalAnalysesAtSpeeds):
    '''HypoidGearSetModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2071.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2071.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6132.HypoidGearSetLoadCase':
        '''HypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6132.HypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def hypoid_gears_modal_analyses_at_speeds(self) -> 'List[_4020.HypoidGearModalAnalysesAtSpeeds]':
        '''List[HypoidGearModalAnalysesAtSpeeds]: 'HypoidGearsModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsModalAnalysesAtSpeeds, constructor.new(_4020.HypoidGearModalAnalysesAtSpeeds))
        return value

    @property
    def hypoid_meshes_modal_analyses_at_speeds(self) -> 'List[_4019.HypoidGearMeshModalAnalysesAtSpeeds]':
        '''List[HypoidGearMeshModalAnalysesAtSpeeds]: 'HypoidMeshesModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesModalAnalysesAtSpeeds, constructor.new(_4019.HypoidGearMeshModalAnalysesAtSpeeds))
        return value
