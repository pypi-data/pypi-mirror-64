'''_3841.py

ZerolBevelGearSetModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model.gears import _2090
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6211
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3840, _3839, _3734
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'ZerolBevelGearSetModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetModalAnalysesAtStiffnesses',)


class ZerolBevelGearSetModalAnalysesAtStiffnesses(_3734.BevelGearSetModalAnalysesAtStiffnesses):
    '''ZerolBevelGearSetModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2090.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2090.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6211.ZerolBevelGearSetLoadCase':
        '''ZerolBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6211.ZerolBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def zerol_bevel_gears_modal_analyses_at_stiffnesses(self) -> 'List[_3840.ZerolBevelGearModalAnalysesAtStiffnesses]':
        '''List[ZerolBevelGearModalAnalysesAtStiffnesses]: 'ZerolBevelGearsModalAnalysesAtStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsModalAnalysesAtStiffnesses, constructor.new(_3840.ZerolBevelGearModalAnalysesAtStiffnesses))
        return value

    @property
    def zerol_bevel_meshes_modal_analyses_at_stiffnesses(self) -> 'List[_3839.ZerolBevelGearMeshModalAnalysesAtStiffnesses]':
        '''List[ZerolBevelGearMeshModalAnalysesAtStiffnesses]: 'ZerolBevelMeshesModalAnalysesAtStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesModalAnalysesAtStiffnesses, constructor.new(_3839.ZerolBevelGearMeshModalAnalysesAtStiffnesses))
        return value
