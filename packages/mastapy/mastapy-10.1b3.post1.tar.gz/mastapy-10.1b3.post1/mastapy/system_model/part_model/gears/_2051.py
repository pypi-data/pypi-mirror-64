'''_2051.py

BevelDifferentialGear
'''


from mastapy.gears.gear_designs.bevel import _912
from mastapy._internal import constructor
from mastapy.gears.gear_designs.zerol_bevel import _715
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.straight_bevel_diff import _724
from mastapy.gears.gear_designs.straight_bevel import _728
from mastapy.gears.gear_designs.spiral_bevel import _732
from mastapy.system_model.part_model.gears import _2055
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialGear')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGear',)


class BevelDifferentialGear(_2055.BevelGear):
    '''BevelDifferentialGear

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGear.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def bevel_gear_design(self) -> '_912.BevelGearDesign':
        '''BevelGearDesign: 'BevelGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_912.BevelGearDesign)(self.wrapped.BevelGearDesign) if self.wrapped.BevelGearDesign else None

    @property
    def bevel_gear_design_of_type_zerol_bevel_gear_design(self) -> '_715.ZerolBevelGearDesign':
        '''ZerolBevelGearDesign: 'BevelGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _715.ZerolBevelGearDesign.TYPE not in self.wrapped.BevelGearDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_design to ZerolBevelGearDesign. Expected: {}.'.format(self.wrapped.BevelGearDesign.__class__.__qualname__))

        return constructor.new(_715.ZerolBevelGearDesign)(self.wrapped.BevelGearDesign) if self.wrapped.BevelGearDesign else None

    @property
    def bevel_gear_design_of_type_straight_bevel_diff_gear_design(self) -> '_724.StraightBevelDiffGearDesign':
        '''StraightBevelDiffGearDesign: 'BevelGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _724.StraightBevelDiffGearDesign.TYPE not in self.wrapped.BevelGearDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_design to StraightBevelDiffGearDesign. Expected: {}.'.format(self.wrapped.BevelGearDesign.__class__.__qualname__))

        return constructor.new(_724.StraightBevelDiffGearDesign)(self.wrapped.BevelGearDesign) if self.wrapped.BevelGearDesign else None

    @property
    def bevel_gear_design_of_type_straight_bevel_gear_design(self) -> '_728.StraightBevelGearDesign':
        '''StraightBevelGearDesign: 'BevelGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _728.StraightBevelGearDesign.TYPE not in self.wrapped.BevelGearDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_design to StraightBevelGearDesign. Expected: {}.'.format(self.wrapped.BevelGearDesign.__class__.__qualname__))

        return constructor.new(_728.StraightBevelGearDesign)(self.wrapped.BevelGearDesign) if self.wrapped.BevelGearDesign else None

    @property
    def bevel_gear_design_of_type_spiral_bevel_gear_design(self) -> '_732.SpiralBevelGearDesign':
        '''SpiralBevelGearDesign: 'BevelGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _732.SpiralBevelGearDesign.TYPE not in self.wrapped.BevelGearDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_design to SpiralBevelGearDesign. Expected: {}.'.format(self.wrapped.BevelGearDesign.__class__.__qualname__))

        return constructor.new(_732.SpiralBevelGearDesign)(self.wrapped.BevelGearDesign) if self.wrapped.BevelGearDesign else None
