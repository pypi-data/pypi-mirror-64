'''_2052.py

BevelDifferentialGearSet
'''


from typing import List

from mastapy.gears.gear_designs.bevel import _914
from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.zerol_bevel import _717
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.straight_bevel_diff import _726
from mastapy.gears.gear_designs.straight_bevel import _730
from mastapy.gears.gear_designs.spiral_bevel import _734
from mastapy.system_model.part_model.gears import _2055, _2056
from mastapy.system_model.connections_and_sockets.gears import _1862
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialGearSet')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSet',)


class BevelDifferentialGearSet(_2056.BevelGearSet):
    '''BevelDifferentialGearSet

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSet.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def conical_gear_set_design(self) -> '_914.BevelGearSetDesign':
        '''BevelGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_914.BevelGearSetDesign)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign else None

    @property
    def conical_gear_set_design_of_type_zerol_bevel_gear_set_design(self) -> '_717.ZerolBevelGearSetDesign':
        '''ZerolBevelGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _717.ZerolBevelGearSetDesign.TYPE not in self.wrapped.ConicalGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_set_design to ZerolBevelGearSetDesign. Expected: {}.'.format(self.wrapped.ConicalGearSetDesign.__class__.__qualname__))

        return constructor.new(_717.ZerolBevelGearSetDesign)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign else None

    @property
    def conical_gear_set_design_of_type_straight_bevel_diff_gear_set_design(self) -> '_726.StraightBevelDiffGearSetDesign':
        '''StraightBevelDiffGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _726.StraightBevelDiffGearSetDesign.TYPE not in self.wrapped.ConicalGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_set_design to StraightBevelDiffGearSetDesign. Expected: {}.'.format(self.wrapped.ConicalGearSetDesign.__class__.__qualname__))

        return constructor.new(_726.StraightBevelDiffGearSetDesign)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign else None

    @property
    def conical_gear_set_design_of_type_straight_bevel_gear_set_design(self) -> '_730.StraightBevelGearSetDesign':
        '''StraightBevelGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _730.StraightBevelGearSetDesign.TYPE not in self.wrapped.ConicalGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_set_design to StraightBevelGearSetDesign. Expected: {}.'.format(self.wrapped.ConicalGearSetDesign.__class__.__qualname__))

        return constructor.new(_730.StraightBevelGearSetDesign)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign else None

    @property
    def conical_gear_set_design_of_type_spiral_bevel_gear_set_design(self) -> '_734.SpiralBevelGearSetDesign':
        '''SpiralBevelGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _734.SpiralBevelGearSetDesign.TYPE not in self.wrapped.ConicalGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_set_design to SpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.ConicalGearSetDesign.__class__.__qualname__))

        return constructor.new(_734.SpiralBevelGearSetDesign)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign else None

    @property
    def bevel_gear_set_design(self) -> '_914.BevelGearSetDesign':
        '''BevelGearSetDesign: 'BevelGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_914.BevelGearSetDesign)(self.wrapped.BevelGearSetDesign) if self.wrapped.BevelGearSetDesign else None

    @property
    def bevel_gear_set_design_of_type_zerol_bevel_gear_set_design(self) -> '_717.ZerolBevelGearSetDesign':
        '''ZerolBevelGearSetDesign: 'BevelGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _717.ZerolBevelGearSetDesign.TYPE not in self.wrapped.BevelGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_set_design to ZerolBevelGearSetDesign. Expected: {}.'.format(self.wrapped.BevelGearSetDesign.__class__.__qualname__))

        return constructor.new(_717.ZerolBevelGearSetDesign)(self.wrapped.BevelGearSetDesign) if self.wrapped.BevelGearSetDesign else None

    @property
    def bevel_gear_set_design_of_type_straight_bevel_diff_gear_set_design(self) -> '_726.StraightBevelDiffGearSetDesign':
        '''StraightBevelDiffGearSetDesign: 'BevelGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _726.StraightBevelDiffGearSetDesign.TYPE not in self.wrapped.BevelGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_set_design to StraightBevelDiffGearSetDesign. Expected: {}.'.format(self.wrapped.BevelGearSetDesign.__class__.__qualname__))

        return constructor.new(_726.StraightBevelDiffGearSetDesign)(self.wrapped.BevelGearSetDesign) if self.wrapped.BevelGearSetDesign else None

    @property
    def bevel_gear_set_design_of_type_straight_bevel_gear_set_design(self) -> '_730.StraightBevelGearSetDesign':
        '''StraightBevelGearSetDesign: 'BevelGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _730.StraightBevelGearSetDesign.TYPE not in self.wrapped.BevelGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_set_design to StraightBevelGearSetDesign. Expected: {}.'.format(self.wrapped.BevelGearSetDesign.__class__.__qualname__))

        return constructor.new(_730.StraightBevelGearSetDesign)(self.wrapped.BevelGearSetDesign) if self.wrapped.BevelGearSetDesign else None

    @property
    def bevel_gear_set_design_of_type_spiral_bevel_gear_set_design(self) -> '_734.SpiralBevelGearSetDesign':
        '''SpiralBevelGearSetDesign: 'BevelGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _734.SpiralBevelGearSetDesign.TYPE not in self.wrapped.BevelGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_set_design to SpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.BevelGearSetDesign.__class__.__qualname__))

        return constructor.new(_734.SpiralBevelGearSetDesign)(self.wrapped.BevelGearSetDesign) if self.wrapped.BevelGearSetDesign else None

    @property
    def bevel_gears(self) -> 'List[_2055.BevelGear]':
        '''List[BevelGear]: 'BevelGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelGears, constructor.new(_2055.BevelGear))
        return value

    @property
    def bevel_meshes(self) -> 'List[_1862.BevelGearMesh]':
        '''List[BevelGearMesh]: 'BevelMeshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelMeshes, constructor.new(_1862.BevelGearMesh))
        return value
