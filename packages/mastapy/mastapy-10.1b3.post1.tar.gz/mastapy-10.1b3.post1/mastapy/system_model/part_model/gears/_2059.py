'''_2059.py

ConicalGear
'''


from mastapy.system_model.part_model.gears import _2067, _2066
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears.gear_designs.conical import _886
from mastapy.gears.gear_designs.zerol_bevel import _715
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.straight_bevel_diff import _724
from mastapy.gears.gear_designs.straight_bevel import _728
from mastapy.gears.gear_designs.spiral_bevel import _732
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _736
from mastapy.gears.gear_designs.klingelnberg_hypoid import _740
from mastapy.gears.gear_designs.klingelnberg_conical import _744
from mastapy.gears.gear_designs.hypoid import _748
from mastapy.gears.gear_designs.bevel import _912
from mastapy.gears.gear_designs.agma_gleason_conical import _925
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConicalGear')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGear',)


class ConicalGear(_2066.Gear):
    '''ConicalGear

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGear.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def orientation(self) -> '_2067.GearOrientations':
        '''GearOrientations: 'Orientation' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.Orientation)
        return constructor.new(_2067.GearOrientations)(value) if value else None

    @orientation.setter
    def orientation(self, value: '_2067.GearOrientations'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Orientation = value

    @property
    def length(self) -> 'float':
        '''float: 'Length' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Length

    @property
    def active_gear_design(self) -> '_886.ConicalGearDesign':
        '''ConicalGearDesign: 'ActiveGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_886.ConicalGearDesign)(self.wrapped.ActiveGearDesign) if self.wrapped.ActiveGearDesign else None

    @property
    def active_gear_design_of_type_zerol_bevel_gear_design(self) -> '_715.ZerolBevelGearDesign':
        '''ZerolBevelGearDesign: 'ActiveGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _715.ZerolBevelGearDesign.TYPE not in self.wrapped.ActiveGearDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_design to ZerolBevelGearDesign. Expected: {}.'.format(self.wrapped.ActiveGearDesign.__class__.__qualname__))

        return constructor.new(_715.ZerolBevelGearDesign)(self.wrapped.ActiveGearDesign) if self.wrapped.ActiveGearDesign else None

    @property
    def active_gear_design_of_type_straight_bevel_diff_gear_design(self) -> '_724.StraightBevelDiffGearDesign':
        '''StraightBevelDiffGearDesign: 'ActiveGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _724.StraightBevelDiffGearDesign.TYPE not in self.wrapped.ActiveGearDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_design to StraightBevelDiffGearDesign. Expected: {}.'.format(self.wrapped.ActiveGearDesign.__class__.__qualname__))

        return constructor.new(_724.StraightBevelDiffGearDesign)(self.wrapped.ActiveGearDesign) if self.wrapped.ActiveGearDesign else None

    @property
    def active_gear_design_of_type_straight_bevel_gear_design(self) -> '_728.StraightBevelGearDesign':
        '''StraightBevelGearDesign: 'ActiveGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _728.StraightBevelGearDesign.TYPE not in self.wrapped.ActiveGearDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_design to StraightBevelGearDesign. Expected: {}.'.format(self.wrapped.ActiveGearDesign.__class__.__qualname__))

        return constructor.new(_728.StraightBevelGearDesign)(self.wrapped.ActiveGearDesign) if self.wrapped.ActiveGearDesign else None

    @property
    def active_gear_design_of_type_spiral_bevel_gear_design(self) -> '_732.SpiralBevelGearDesign':
        '''SpiralBevelGearDesign: 'ActiveGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _732.SpiralBevelGearDesign.TYPE not in self.wrapped.ActiveGearDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_design to SpiralBevelGearDesign. Expected: {}.'.format(self.wrapped.ActiveGearDesign.__class__.__qualname__))

        return constructor.new(_732.SpiralBevelGearDesign)(self.wrapped.ActiveGearDesign) if self.wrapped.ActiveGearDesign else None

    @property
    def active_gear_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_design(self) -> '_736.KlingelnbergCycloPalloidSpiralBevelGearDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearDesign: 'ActiveGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _736.KlingelnbergCycloPalloidSpiralBevelGearDesign.TYPE not in self.wrapped.ActiveGearDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_design to KlingelnbergCycloPalloidSpiralBevelGearDesign. Expected: {}.'.format(self.wrapped.ActiveGearDesign.__class__.__qualname__))

        return constructor.new(_736.KlingelnbergCycloPalloidSpiralBevelGearDesign)(self.wrapped.ActiveGearDesign) if self.wrapped.ActiveGearDesign else None

    @property
    def active_gear_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_design(self) -> '_740.KlingelnbergCycloPalloidHypoidGearDesign':
        '''KlingelnbergCycloPalloidHypoidGearDesign: 'ActiveGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _740.KlingelnbergCycloPalloidHypoidGearDesign.TYPE not in self.wrapped.ActiveGearDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_design to KlingelnbergCycloPalloidHypoidGearDesign. Expected: {}.'.format(self.wrapped.ActiveGearDesign.__class__.__qualname__))

        return constructor.new(_740.KlingelnbergCycloPalloidHypoidGearDesign)(self.wrapped.ActiveGearDesign) if self.wrapped.ActiveGearDesign else None

    @property
    def active_gear_design_of_type_klingelnberg_conical_gear_design(self) -> '_744.KlingelnbergConicalGearDesign':
        '''KlingelnbergConicalGearDesign: 'ActiveGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _744.KlingelnbergConicalGearDesign.TYPE not in self.wrapped.ActiveGearDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_design to KlingelnbergConicalGearDesign. Expected: {}.'.format(self.wrapped.ActiveGearDesign.__class__.__qualname__))

        return constructor.new(_744.KlingelnbergConicalGearDesign)(self.wrapped.ActiveGearDesign) if self.wrapped.ActiveGearDesign else None

    @property
    def active_gear_design_of_type_hypoid_gear_design(self) -> '_748.HypoidGearDesign':
        '''HypoidGearDesign: 'ActiveGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _748.HypoidGearDesign.TYPE not in self.wrapped.ActiveGearDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_design to HypoidGearDesign. Expected: {}.'.format(self.wrapped.ActiveGearDesign.__class__.__qualname__))

        return constructor.new(_748.HypoidGearDesign)(self.wrapped.ActiveGearDesign) if self.wrapped.ActiveGearDesign else None

    @property
    def active_gear_design_of_type_bevel_gear_design(self) -> '_912.BevelGearDesign':
        '''BevelGearDesign: 'ActiveGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _912.BevelGearDesign.TYPE not in self.wrapped.ActiveGearDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_design to BevelGearDesign. Expected: {}.'.format(self.wrapped.ActiveGearDesign.__class__.__qualname__))

        return constructor.new(_912.BevelGearDesign)(self.wrapped.ActiveGearDesign) if self.wrapped.ActiveGearDesign else None

    @property
    def active_gear_design_of_type_agma_gleason_conical_gear_design(self) -> '_925.AGMAGleasonConicalGearDesign':
        '''AGMAGleasonConicalGearDesign: 'ActiveGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _925.AGMAGleasonConicalGearDesign.TYPE not in self.wrapped.ActiveGearDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_design to AGMAGleasonConicalGearDesign. Expected: {}.'.format(self.wrapped.ActiveGearDesign.__class__.__qualname__))

        return constructor.new(_925.AGMAGleasonConicalGearDesign)(self.wrapped.ActiveGearDesign) if self.wrapped.ActiveGearDesign else None

    @property
    def conical_gear_design(self) -> '_886.ConicalGearDesign':
        '''ConicalGearDesign: 'ConicalGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_886.ConicalGearDesign)(self.wrapped.ConicalGearDesign) if self.wrapped.ConicalGearDesign else None

    @property
    def conical_gear_design_of_type_zerol_bevel_gear_design(self) -> '_715.ZerolBevelGearDesign':
        '''ZerolBevelGearDesign: 'ConicalGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _715.ZerolBevelGearDesign.TYPE not in self.wrapped.ConicalGearDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_design to ZerolBevelGearDesign. Expected: {}.'.format(self.wrapped.ConicalGearDesign.__class__.__qualname__))

        return constructor.new(_715.ZerolBevelGearDesign)(self.wrapped.ConicalGearDesign) if self.wrapped.ConicalGearDesign else None

    @property
    def conical_gear_design_of_type_straight_bevel_diff_gear_design(self) -> '_724.StraightBevelDiffGearDesign':
        '''StraightBevelDiffGearDesign: 'ConicalGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _724.StraightBevelDiffGearDesign.TYPE not in self.wrapped.ConicalGearDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_design to StraightBevelDiffGearDesign. Expected: {}.'.format(self.wrapped.ConicalGearDesign.__class__.__qualname__))

        return constructor.new(_724.StraightBevelDiffGearDesign)(self.wrapped.ConicalGearDesign) if self.wrapped.ConicalGearDesign else None

    @property
    def conical_gear_design_of_type_straight_bevel_gear_design(self) -> '_728.StraightBevelGearDesign':
        '''StraightBevelGearDesign: 'ConicalGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _728.StraightBevelGearDesign.TYPE not in self.wrapped.ConicalGearDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_design to StraightBevelGearDesign. Expected: {}.'.format(self.wrapped.ConicalGearDesign.__class__.__qualname__))

        return constructor.new(_728.StraightBevelGearDesign)(self.wrapped.ConicalGearDesign) if self.wrapped.ConicalGearDesign else None

    @property
    def conical_gear_design_of_type_spiral_bevel_gear_design(self) -> '_732.SpiralBevelGearDesign':
        '''SpiralBevelGearDesign: 'ConicalGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _732.SpiralBevelGearDesign.TYPE not in self.wrapped.ConicalGearDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_design to SpiralBevelGearDesign. Expected: {}.'.format(self.wrapped.ConicalGearDesign.__class__.__qualname__))

        return constructor.new(_732.SpiralBevelGearDesign)(self.wrapped.ConicalGearDesign) if self.wrapped.ConicalGearDesign else None

    @property
    def conical_gear_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_design(self) -> '_736.KlingelnbergCycloPalloidSpiralBevelGearDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearDesign: 'ConicalGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _736.KlingelnbergCycloPalloidSpiralBevelGearDesign.TYPE not in self.wrapped.ConicalGearDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_design to KlingelnbergCycloPalloidSpiralBevelGearDesign. Expected: {}.'.format(self.wrapped.ConicalGearDesign.__class__.__qualname__))

        return constructor.new(_736.KlingelnbergCycloPalloidSpiralBevelGearDesign)(self.wrapped.ConicalGearDesign) if self.wrapped.ConicalGearDesign else None

    @property
    def conical_gear_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_design(self) -> '_740.KlingelnbergCycloPalloidHypoidGearDesign':
        '''KlingelnbergCycloPalloidHypoidGearDesign: 'ConicalGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _740.KlingelnbergCycloPalloidHypoidGearDesign.TYPE not in self.wrapped.ConicalGearDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_design to KlingelnbergCycloPalloidHypoidGearDesign. Expected: {}.'.format(self.wrapped.ConicalGearDesign.__class__.__qualname__))

        return constructor.new(_740.KlingelnbergCycloPalloidHypoidGearDesign)(self.wrapped.ConicalGearDesign) if self.wrapped.ConicalGearDesign else None

    @property
    def conical_gear_design_of_type_klingelnberg_conical_gear_design(self) -> '_744.KlingelnbergConicalGearDesign':
        '''KlingelnbergConicalGearDesign: 'ConicalGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _744.KlingelnbergConicalGearDesign.TYPE not in self.wrapped.ConicalGearDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_design to KlingelnbergConicalGearDesign. Expected: {}.'.format(self.wrapped.ConicalGearDesign.__class__.__qualname__))

        return constructor.new(_744.KlingelnbergConicalGearDesign)(self.wrapped.ConicalGearDesign) if self.wrapped.ConicalGearDesign else None

    @property
    def conical_gear_design_of_type_hypoid_gear_design(self) -> '_748.HypoidGearDesign':
        '''HypoidGearDesign: 'ConicalGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _748.HypoidGearDesign.TYPE not in self.wrapped.ConicalGearDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_design to HypoidGearDesign. Expected: {}.'.format(self.wrapped.ConicalGearDesign.__class__.__qualname__))

        return constructor.new(_748.HypoidGearDesign)(self.wrapped.ConicalGearDesign) if self.wrapped.ConicalGearDesign else None

    @property
    def conical_gear_design_of_type_bevel_gear_design(self) -> '_912.BevelGearDesign':
        '''BevelGearDesign: 'ConicalGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _912.BevelGearDesign.TYPE not in self.wrapped.ConicalGearDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_design to BevelGearDesign. Expected: {}.'.format(self.wrapped.ConicalGearDesign.__class__.__qualname__))

        return constructor.new(_912.BevelGearDesign)(self.wrapped.ConicalGearDesign) if self.wrapped.ConicalGearDesign else None

    @property
    def conical_gear_design_of_type_agma_gleason_conical_gear_design(self) -> '_925.AGMAGleasonConicalGearDesign':
        '''AGMAGleasonConicalGearDesign: 'ConicalGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _925.AGMAGleasonConicalGearDesign.TYPE not in self.wrapped.ConicalGearDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_design to AGMAGleasonConicalGearDesign. Expected: {}.'.format(self.wrapped.ConicalGearDesign.__class__.__qualname__))

        return constructor.new(_925.AGMAGleasonConicalGearDesign)(self.wrapped.ConicalGearDesign) if self.wrapped.ConicalGearDesign else None
