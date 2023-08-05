'''_164.py

GearSetDutyCycleRating
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs import _705
from mastapy.gears.gear_designs.zerol_bevel import _709
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.worm import _714
from mastapy.gears.gear_designs.straight_bevel_diff import _718
from mastapy.gears.gear_designs.straight_bevel import _722
from mastapy.gears.gear_designs.spiral_bevel import _726
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _730
from mastapy.gears.gear_designs.klingelnberg_hypoid import _734
from mastapy.gears.gear_designs.klingelnberg_conical import _738
from mastapy.gears.gear_designs.hypoid import _742
from mastapy.gears.gear_designs.face import _750
from mastapy.gears.gear_designs.cylindrical import _777, _786
from mastapy.gears.gear_designs.conical import _880
from mastapy.gears.gear_designs.concept import _902
from mastapy.gears.gear_designs.bevel import _906
from mastapy.gears.gear_designs.agma_gleason_conical import _919
from mastapy.gears.rating import _160, _167, _157
from mastapy._internal.python_net import python_net_import

_GEAR_SET_DUTY_CYCLE_RATING = python_net_import('SMT.MastaAPI.Gears.Rating', 'GearSetDutyCycleRating')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetDutyCycleRating',)


class GearSetDutyCycleRating(_157.AbstractGearSetRating):
    '''GearSetDutyCycleRating

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_DUTY_CYCLE_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetDutyCycleRating.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.'''

        return self.wrapped.Name

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else None

    @property
    def total_duty_cycle_gear_set_reliability(self) -> 'float':
        '''float: 'TotalDutyCycleGearSetReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalDutyCycleGearSetReliability

    @property
    def duty_cycle_name(self) -> 'str':
        '''str: 'DutyCycleName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DutyCycleName

    @property
    def set_face_widths_for_specified_safety_factors(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'SetFaceWidthsForSpecifiedSafetyFactors' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SetFaceWidthsForSpecifiedSafetyFactors

    @property
    def gear_set_design(self) -> '_705.GearSetDesign':
        '''GearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_705.GearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_set_design_of_type_zerol_bevel_gear_set_design(self) -> '_709.ZerolBevelGearSetDesign':
        '''ZerolBevelGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _709.ZerolBevelGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to ZerolBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new(_709.ZerolBevelGearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_set_design_of_type_worm_gear_set_design(self) -> '_714.WormGearSetDesign':
        '''WormGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _714.WormGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to WormGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new(_714.WormGearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_set_design_of_type_straight_bevel_diff_gear_set_design(self) -> '_718.StraightBevelDiffGearSetDesign':
        '''StraightBevelDiffGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _718.StraightBevelDiffGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to StraightBevelDiffGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new(_718.StraightBevelDiffGearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_set_design_of_type_straight_bevel_gear_set_design(self) -> '_722.StraightBevelGearSetDesign':
        '''StraightBevelGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _722.StraightBevelGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to StraightBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new(_722.StraightBevelGearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_set_design_of_type_spiral_bevel_gear_set_design(self) -> '_726.SpiralBevelGearSetDesign':
        '''SpiralBevelGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _726.SpiralBevelGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to SpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new(_726.SpiralBevelGearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_set_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(self) -> '_730.KlingelnbergCycloPalloidSpiralBevelGearSetDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _730.KlingelnbergCycloPalloidSpiralBevelGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to KlingelnbergCycloPalloidSpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new(_730.KlingelnbergCycloPalloidSpiralBevelGearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_set_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_design(self) -> '_734.KlingelnbergCycloPalloidHypoidGearSetDesign':
        '''KlingelnbergCycloPalloidHypoidGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _734.KlingelnbergCycloPalloidHypoidGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to KlingelnbergCycloPalloidHypoidGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new(_734.KlingelnbergCycloPalloidHypoidGearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_set_design_of_type_klingelnberg_conical_gear_set_design(self) -> '_738.KlingelnbergConicalGearSetDesign':
        '''KlingelnbergConicalGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _738.KlingelnbergConicalGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to KlingelnbergConicalGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new(_738.KlingelnbergConicalGearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_set_design_of_type_hypoid_gear_set_design(self) -> '_742.HypoidGearSetDesign':
        '''HypoidGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _742.HypoidGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to HypoidGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new(_742.HypoidGearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_set_design_of_type_face_gear_set_design(self) -> '_750.FaceGearSetDesign':
        '''FaceGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _750.FaceGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to FaceGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new(_750.FaceGearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_set_design_of_type_cylindrical_gear_set_design(self) -> '_777.CylindricalGearSetDesign':
        '''CylindricalGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _777.CylindricalGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to CylindricalGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new(_777.CylindricalGearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_set_design_of_type_cylindrical_planetary_gear_set_design(self) -> '_786.CylindricalPlanetaryGearSetDesign':
        '''CylindricalPlanetaryGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _786.CylindricalPlanetaryGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to CylindricalPlanetaryGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new(_786.CylindricalPlanetaryGearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_set_design_of_type_conical_gear_set_design(self) -> '_880.ConicalGearSetDesign':
        '''ConicalGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _880.ConicalGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to ConicalGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new(_880.ConicalGearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_set_design_of_type_concept_gear_set_design(self) -> '_902.ConceptGearSetDesign':
        '''ConceptGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _902.ConceptGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to ConceptGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new(_902.ConceptGearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_set_design_of_type_bevel_gear_set_design(self) -> '_906.BevelGearSetDesign':
        '''BevelGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _906.BevelGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to BevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new(_906.BevelGearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_set_design_of_type_agma_gleason_conical_gear_set_design(self) -> '_919.AGMAGleasonConicalGearSetDesign':
        '''AGMAGleasonConicalGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _919.AGMAGleasonConicalGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to AGMAGleasonConicalGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new(_919.AGMAGleasonConicalGearSetDesign)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign else None

    @property
    def gear_ratings(self) -> 'List[_160.GearDutyCycleRating]':
        '''List[GearDutyCycleRating]: 'GearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearRatings, constructor.new(_160.GearDutyCycleRating))
        return value

    @property
    def gear_duty_cycle_ratings(self) -> 'List[_160.GearDutyCycleRating]':
        '''List[GearDutyCycleRating]: 'GearDutyCycleRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearDutyCycleRatings, constructor.new(_160.GearDutyCycleRating))
        return value

    @property
    def gear_mesh_ratings(self) -> 'List[_167.MeshDutyCycleRating]':
        '''List[MeshDutyCycleRating]: 'GearMeshRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearMeshRatings, constructor.new(_167.MeshDutyCycleRating))
        return value

    @property
    def gear_mesh_duty_cycle_ratings(self) -> 'List[_167.MeshDutyCycleRating]':
        '''List[MeshDutyCycleRating]: 'GearMeshDutyCycleRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearMeshDutyCycleRatings, constructor.new(_167.MeshDutyCycleRating))
        return value
