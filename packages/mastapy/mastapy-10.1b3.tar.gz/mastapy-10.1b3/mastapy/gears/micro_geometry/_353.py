'''_353.py

FlankMicroGeometry
'''


from mastapy.gears import _138
from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs import _702
from mastapy.gears.gear_designs.zerol_bevel import _707
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.worm import _711, _712, _715
from mastapy.gears.gear_designs.straight_bevel_diff import _716
from mastapy.gears.gear_designs.straight_bevel import _720
from mastapy.gears.gear_designs.spiral_bevel import _724
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _728
from mastapy.gears.gear_designs.klingelnberg_hypoid import _732
from mastapy.gears.gear_designs.klingelnberg_conical import _736
from mastapy.gears.gear_designs.hypoid import _740
from mastapy.gears.gear_designs.face import _744, _749, _752
from mastapy.gears.gear_designs.cylindrical import _766, _787
from mastapy.gears.gear_designs.conical import _878
from mastapy.gears.gear_designs.concept import _900
from mastapy.gears.gear_designs.bevel import _904
from mastapy.gears.gear_designs.agma_gleason_conical import _917
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_FLANK_MICRO_GEOMETRY = python_net_import('SMT.MastaAPI.Gears.MicroGeometry', 'FlankMicroGeometry')


__docformat__ = 'restructuredtext en'
__all__ = ('FlankMicroGeometry',)


class FlankMicroGeometry(_0.APIBase):
    '''FlankMicroGeometry

    This is a mastapy class.
    '''

    TYPE = _FLANK_MICRO_GEOMETRY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FlankMicroGeometry.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def micro_geometry_input_type(self) -> '_138.MicroGeometryInputTypes':
        '''MicroGeometryInputTypes: 'MicroGeometryInputType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.MicroGeometryInputType)
        return constructor.new(_138.MicroGeometryInputTypes)(value) if value else None

    @micro_geometry_input_type.setter
    def micro_geometry_input_type(self, value: '_138.MicroGeometryInputTypes'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MicroGeometryInputType = value

    @property
    def gear_design(self) -> '_702.GearDesign':
        '''GearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_702.GearDesign)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_zerol_bevel_gear_design(self) -> '_707.ZerolBevelGearDesign':
        '''ZerolBevelGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _707.ZerolBevelGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to ZerolBevelGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new(_707.ZerolBevelGearDesign)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_worm_design(self) -> '_711.WormDesign':
        '''WormDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _711.WormDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to WormDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new(_711.WormDesign)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_worm_gear_design(self) -> '_712.WormGearDesign':
        '''WormGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _712.WormGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to WormGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new(_712.WormGearDesign)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_worm_wheel_design(self) -> '_715.WormWheelDesign':
        '''WormWheelDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _715.WormWheelDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to WormWheelDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new(_715.WormWheelDesign)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_straight_bevel_diff_gear_design(self) -> '_716.StraightBevelDiffGearDesign':
        '''StraightBevelDiffGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _716.StraightBevelDiffGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to StraightBevelDiffGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new(_716.StraightBevelDiffGearDesign)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_straight_bevel_gear_design(self) -> '_720.StraightBevelGearDesign':
        '''StraightBevelGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _720.StraightBevelGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to StraightBevelGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new(_720.StraightBevelGearDesign)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_spiral_bevel_gear_design(self) -> '_724.SpiralBevelGearDesign':
        '''SpiralBevelGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _724.SpiralBevelGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to SpiralBevelGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new(_724.SpiralBevelGearDesign)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_design(self) -> '_728.KlingelnbergCycloPalloidSpiralBevelGearDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _728.KlingelnbergCycloPalloidSpiralBevelGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to KlingelnbergCycloPalloidSpiralBevelGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new(_728.KlingelnbergCycloPalloidSpiralBevelGearDesign)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_design(self) -> '_732.KlingelnbergCycloPalloidHypoidGearDesign':
        '''KlingelnbergCycloPalloidHypoidGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _732.KlingelnbergCycloPalloidHypoidGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to KlingelnbergCycloPalloidHypoidGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new(_732.KlingelnbergCycloPalloidHypoidGearDesign)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_klingelnberg_conical_gear_design(self) -> '_736.KlingelnbergConicalGearDesign':
        '''KlingelnbergConicalGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _736.KlingelnbergConicalGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to KlingelnbergConicalGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new(_736.KlingelnbergConicalGearDesign)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_hypoid_gear_design(self) -> '_740.HypoidGearDesign':
        '''HypoidGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _740.HypoidGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to HypoidGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new(_740.HypoidGearDesign)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_face_gear_design(self) -> '_744.FaceGearDesign':
        '''FaceGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _744.FaceGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to FaceGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new(_744.FaceGearDesign)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_face_gear_pinion_design(self) -> '_749.FaceGearPinionDesign':
        '''FaceGearPinionDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _749.FaceGearPinionDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to FaceGearPinionDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new(_749.FaceGearPinionDesign)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_face_gear_wheel_design(self) -> '_752.FaceGearWheelDesign':
        '''FaceGearWheelDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _752.FaceGearWheelDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to FaceGearWheelDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new(_752.FaceGearWheelDesign)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_cylindrical_gear_design(self) -> '_766.CylindricalGearDesign':
        '''CylindricalGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _766.CylindricalGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to CylindricalGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new(_766.CylindricalGearDesign)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_cylindrical_planet_gear_design(self) -> '_787.CylindricalPlanetGearDesign':
        '''CylindricalPlanetGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _787.CylindricalPlanetGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to CylindricalPlanetGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new(_787.CylindricalPlanetGearDesign)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_conical_gear_design(self) -> '_878.ConicalGearDesign':
        '''ConicalGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _878.ConicalGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to ConicalGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new(_878.ConicalGearDesign)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_concept_gear_design(self) -> '_900.ConceptGearDesign':
        '''ConceptGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _900.ConceptGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to ConceptGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new(_900.ConceptGearDesign)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_bevel_gear_design(self) -> '_904.BevelGearDesign':
        '''BevelGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _904.BevelGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to BevelGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new(_904.BevelGearDesign)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    @property
    def gear_design_of_type_agma_gleason_conical_gear_design(self) -> '_917.AGMAGleasonConicalGearDesign':
        '''AGMAGleasonConicalGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _917.AGMAGleasonConicalGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to AGMAGleasonConicalGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new(_917.AGMAGleasonConicalGearDesign)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None
