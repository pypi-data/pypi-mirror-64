﻿'''_587.py

PinionRoughMachineSetting
'''


from mastapy._internal import constructor
from mastapy.gears.manufacturing.bevel import _565
from mastapy.gears.gear_designs.conical import _880
from mastapy.gears.gear_designs.zerol_bevel import _709
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.straight_bevel_diff import _718
from mastapy.gears.gear_designs.straight_bevel import _722
from mastapy.gears.gear_designs.spiral_bevel import _726
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _730
from mastapy.gears.gear_designs.klingelnberg_hypoid import _734
from mastapy.gears.gear_designs.klingelnberg_conical import _738
from mastapy.gears.gear_designs.hypoid import _742
from mastapy.gears.gear_designs.bevel import _906
from mastapy.gears.gear_designs.agma_gleason_conical import _919
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_PINION_ROUGH_MACHINE_SETTING = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'PinionRoughMachineSetting')


__docformat__ = 'restructuredtext en'
__all__ = ('PinionRoughMachineSetting',)


class PinionRoughMachineSetting(_0.APIBase):
    '''PinionRoughMachineSetting

    This is a mastapy class.
    '''

    TYPE = _PINION_ROUGH_MACHINE_SETTING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PinionRoughMachineSetting.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def blank_offset(self) -> 'float':
        '''float: 'BlankOffset' is the original name of this property.'''

        return self.wrapped.BlankOffset

    @blank_offset.setter
    def blank_offset(self, value: 'float'):
        self.wrapped.BlankOffset = float(value) if value else 0.0

    @property
    def increment_of_pinion_workpiece_mounting_distance(self) -> 'float':
        '''float: 'IncrementOfPinionWorkpieceMountingDistance' is the original name of this property.'''

        return self.wrapped.IncrementOfPinionWorkpieceMountingDistance

    @increment_of_pinion_workpiece_mounting_distance.setter
    def increment_of_pinion_workpiece_mounting_distance(self, value: 'float'):
        self.wrapped.IncrementOfPinionWorkpieceMountingDistance = float(value) if value else 0.0

    @property
    def cone_distance_of_reference_point(self) -> 'float':
        '''float: 'ConeDistanceOfReferencePoint' is the original name of this property.'''

        return self.wrapped.ConeDistanceOfReferencePoint

    @cone_distance_of_reference_point.setter
    def cone_distance_of_reference_point(self, value: 'float'):
        self.wrapped.ConeDistanceOfReferencePoint = float(value) if value else 0.0

    @property
    def height_of_reference_point(self) -> 'float':
        '''float: 'HeightOfReferencePoint' is the original name of this property.'''

        return self.wrapped.HeightOfReferencePoint

    @height_of_reference_point.setter
    def height_of_reference_point(self, value: 'float'):
        self.wrapped.HeightOfReferencePoint = float(value) if value else 0.0

    @property
    def spiral_angle_at_reference_point(self) -> 'float':
        '''float: 'SpiralAngleAtReferencePoint' is the original name of this property.'''

        return self.wrapped.SpiralAngleAtReferencePoint

    @spiral_angle_at_reference_point.setter
    def spiral_angle_at_reference_point(self, value: 'float'):
        self.wrapped.SpiralAngleAtReferencePoint = float(value) if value else 0.0

    @property
    def minimum_allowed_finish_stock(self) -> 'float':
        '''float: 'MinimumAllowedFinishStock' is the original name of this property.'''

        return self.wrapped.MinimumAllowedFinishStock

    @minimum_allowed_finish_stock.setter
    def minimum_allowed_finish_stock(self, value: 'float'):
        self.wrapped.MinimumAllowedFinishStock = float(value) if value else 0.0

    @property
    def absolute_increment_in_machine_centre_to_back(self) -> 'float':
        '''float: 'AbsoluteIncrementInMachineCentreToBack' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AbsoluteIncrementInMachineCentreToBack

    @property
    def pinion_config(self) -> '_565.ConicalPinionManufacturingConfig':
        '''ConicalPinionManufacturingConfig: 'PinionConfig' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_565.ConicalPinionManufacturingConfig)(self.wrapped.PinionConfig) if self.wrapped.PinionConfig else None

    @property
    def gear_set(self) -> '_880.ConicalGearSetDesign':
        '''ConicalGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_880.ConicalGearSetDesign)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_zerol_bevel_gear_set_design(self) -> '_709.ZerolBevelGearSetDesign':
        '''ZerolBevelGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _709.ZerolBevelGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to ZerolBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new(_709.ZerolBevelGearSetDesign)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_straight_bevel_diff_gear_set_design(self) -> '_718.StraightBevelDiffGearSetDesign':
        '''StraightBevelDiffGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _718.StraightBevelDiffGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to StraightBevelDiffGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new(_718.StraightBevelDiffGearSetDesign)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_straight_bevel_gear_set_design(self) -> '_722.StraightBevelGearSetDesign':
        '''StraightBevelGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _722.StraightBevelGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to StraightBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new(_722.StraightBevelGearSetDesign)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_spiral_bevel_gear_set_design(self) -> '_726.SpiralBevelGearSetDesign':
        '''SpiralBevelGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _726.SpiralBevelGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to SpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new(_726.SpiralBevelGearSetDesign)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(self) -> '_730.KlingelnbergCycloPalloidSpiralBevelGearSetDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _730.KlingelnbergCycloPalloidSpiralBevelGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to KlingelnbergCycloPalloidSpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new(_730.KlingelnbergCycloPalloidSpiralBevelGearSetDesign)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_design(self) -> '_734.KlingelnbergCycloPalloidHypoidGearSetDesign':
        '''KlingelnbergCycloPalloidHypoidGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _734.KlingelnbergCycloPalloidHypoidGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to KlingelnbergCycloPalloidHypoidGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new(_734.KlingelnbergCycloPalloidHypoidGearSetDesign)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_klingelnberg_conical_gear_set_design(self) -> '_738.KlingelnbergConicalGearSetDesign':
        '''KlingelnbergConicalGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _738.KlingelnbergConicalGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to KlingelnbergConicalGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new(_738.KlingelnbergConicalGearSetDesign)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_hypoid_gear_set_design(self) -> '_742.HypoidGearSetDesign':
        '''HypoidGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _742.HypoidGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to HypoidGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new(_742.HypoidGearSetDesign)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_bevel_gear_set_design(self) -> '_906.BevelGearSetDesign':
        '''BevelGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _906.BevelGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to BevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new(_906.BevelGearSetDesign)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gear_set_of_type_agma_gleason_conical_gear_set_design(self) -> '_919.AGMAGleasonConicalGearSetDesign':
        '''AGMAGleasonConicalGearSetDesign: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _919.AGMAGleasonConicalGearSetDesign.TYPE not in self.wrapped.GearSet.__class__.__mro__:
            raise CastException('Failed to cast gear_set to AGMAGleasonConicalGearSetDesign. Expected: {}.'.format(self.wrapped.GearSet.__class__.__qualname__))

        return constructor.new(_919.AGMAGleasonConicalGearSetDesign)(self.wrapped.GearSet) if self.wrapped.GearSet else None
