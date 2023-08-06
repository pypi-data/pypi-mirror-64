'''_6048.py

AGMAGleasonConicalGearSetLoadCase
'''


from mastapy._internal import constructor
from mastapy.system_model.part_model.gears import (
    _2050, _2052, _2056, _2071,
    _2080, _2082, _2084, _2090
)
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.bevel import _575, _573, _574
from mastapy.system_model.analyses_and_results.static_loads import _6079
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'AGMAGleasonConicalGearSetLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAGleasonConicalGearSetLoadCase',)


class AGMAGleasonConicalGearSetLoadCase(_6079.ConicalGearSetLoadCase):
    '''AGMAGleasonConicalGearSetLoadCase

    This is a mastapy class.
    '''

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_SET_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AGMAGleasonConicalGearSetLoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def override_manufacturing_config_micro_geometry(self) -> 'bool':
        '''bool: 'OverrideManufacturingConfigMicroGeometry' is the original name of this property.'''

        return self.wrapped.OverrideManufacturingConfigMicroGeometry

    @override_manufacturing_config_micro_geometry.setter
    def override_manufacturing_config_micro_geometry(self, value: 'bool'):
        self.wrapped.OverrideManufacturingConfigMicroGeometry = bool(value) if value else False

    @property
    def assembly_design(self) -> '_2050.AGMAGleasonConicalGearSet':
        '''AGMAGleasonConicalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2050.AGMAGleasonConicalGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_design_of_type_bevel_differential_gear_set(self) -> '_2052.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2052.BevelDifferentialGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to BevelDifferentialGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new(_2052.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_design_of_type_bevel_gear_set(self) -> '_2056.BevelGearSet':
        '''BevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2056.BevelGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to BevelGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new(_2056.BevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_design_of_type_hypoid_gear_set(self) -> '_2071.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2071.HypoidGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to HypoidGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new(_2071.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_design_of_type_spiral_bevel_gear_set(self) -> '_2080.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2080.SpiralBevelGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to SpiralBevelGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new(_2080.SpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_design_of_type_straight_bevel_diff_gear_set(self) -> '_2082.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2082.StraightBevelDiffGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to StraightBevelDiffGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new(_2082.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_design_of_type_straight_bevel_gear_set(self) -> '_2084.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2084.StraightBevelGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to StraightBevelGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new(_2084.StraightBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_design_of_type_zerol_bevel_gear_set(self) -> '_2090.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2090.ZerolBevelGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to ZerolBevelGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new(_2090.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def overridden_manufacturing_config_micro_geometry(self) -> '_575.ConicalSetMicroGeometryConfigBase':
        '''ConicalSetMicroGeometryConfigBase: 'OverriddenManufacturingConfigMicroGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_575.ConicalSetMicroGeometryConfigBase)(self.wrapped.OverriddenManufacturingConfigMicroGeometry) if self.wrapped.OverriddenManufacturingConfigMicroGeometry else None

    @property
    def overridden_manufacturing_config_micro_geometry_of_type_conical_set_manufacturing_config(self) -> '_573.ConicalSetManufacturingConfig':
        '''ConicalSetManufacturingConfig: 'OverriddenManufacturingConfigMicroGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _573.ConicalSetManufacturingConfig.TYPE not in self.wrapped.OverriddenManufacturingConfigMicroGeometry.__class__.__mro__:
            raise CastException('Failed to cast overridden_manufacturing_config_micro_geometry to ConicalSetManufacturingConfig. Expected: {}.'.format(self.wrapped.OverriddenManufacturingConfigMicroGeometry.__class__.__qualname__))

        return constructor.new(_573.ConicalSetManufacturingConfig)(self.wrapped.OverriddenManufacturingConfigMicroGeometry) if self.wrapped.OverriddenManufacturingConfigMicroGeometry else None

    @property
    def overridden_manufacturing_config_micro_geometry_of_type_conical_set_micro_geometry_config(self) -> '_574.ConicalSetMicroGeometryConfig':
        '''ConicalSetMicroGeometryConfig: 'OverriddenManufacturingConfigMicroGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _574.ConicalSetMicroGeometryConfig.TYPE not in self.wrapped.OverriddenManufacturingConfigMicroGeometry.__class__.__mro__:
            raise CastException('Failed to cast overridden_manufacturing_config_micro_geometry to ConicalSetMicroGeometryConfig. Expected: {}.'.format(self.wrapped.OverriddenManufacturingConfigMicroGeometry.__class__.__qualname__))

        return constructor.new(_574.ConicalSetMicroGeometryConfig)(self.wrapped.OverriddenManufacturingConfigMicroGeometry) if self.wrapped.OverriddenManufacturingConfigMicroGeometry else None
