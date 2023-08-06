'''_1833.py

ComponentMeasurer
'''


from typing import List

from mastapy._internal import constructor
from mastapy.system_model.part_model import (
    _1986, _1979, _1982, _1984,
    _1989, _1990, _1993, _1995,
    _1998, _2001, _2002, _2003,
    _2005, _2007, _2009, _2010,
    _2015, _2016
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.shaft_model import _2019
from mastapy.system_model.part_model.gears import (
    _2049, _2051, _2053, _2054,
    _2055, _2057, _2059, _2061,
    _2063, _2064, _2066, _2070,
    _2072, _2074, _2076, _2079,
    _2081, _2083, _2085, _2086,
    _2087, _2089
)
from mastapy.system_model.part_model.couplings import (
    _2111, _2114, _2116, _2118,
    _2120, _2121, _2127, _2129,
    _2131, _2134, _2135, _2136,
    _2138, _2140
)
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_COMPONENT_MEASURER = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'ComponentMeasurer')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentMeasurer',)


class ComponentMeasurer(_0.APIBase):
    '''ComponentMeasurer

    This is a mastapy class.
    '''

    TYPE = _COMPONENT_MEASURER

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ComponentMeasurer.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def offset_of_component(self) -> 'float':
        '''float: 'OffsetOfComponent' is the original name of this property.'''

        return self.wrapped.OffsetOfComponent

    @offset_of_component.setter
    def offset_of_component(self, value: 'float'):
        self.wrapped.OffsetOfComponent = float(value) if value else 0.0

    @property
    def component(self) -> '_1986.Component':
        '''Component: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1986.Component)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_abstract_shaft_or_housing(self) -> '_1979.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1979.AbstractShaftOrHousing.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to AbstractShaftOrHousing. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1979.AbstractShaftOrHousing)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_bearing(self) -> '_1982.Bearing':
        '''Bearing: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1982.Bearing.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to Bearing. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1982.Bearing)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_bolt(self) -> '_1984.Bolt':
        '''Bolt: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1984.Bolt.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to Bolt. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1984.Bolt)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_connector(self) -> '_1989.Connector':
        '''Connector: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1989.Connector.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to Connector. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1989.Connector)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_datum(self) -> '_1990.Datum':
        '''Datum: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1990.Datum.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to Datum. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1990.Datum)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_external_cad_model(self) -> '_1993.ExternalCADModel':
        '''ExternalCADModel: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1993.ExternalCADModel.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ExternalCADModel. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1993.ExternalCADModel)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_guide_dxf_model(self) -> '_1995.GuideDxfModel':
        '''GuideDxfModel: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1995.GuideDxfModel.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to GuideDxfModel. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1995.GuideDxfModel)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_imported_fe_component(self) -> '_1998.ImportedFEComponent':
        '''ImportedFEComponent: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1998.ImportedFEComponent.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ImportedFEComponent. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1998.ImportedFEComponent)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_mass_disc(self) -> '_2001.MassDisc':
        '''MassDisc: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2001.MassDisc.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to MassDisc. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2001.MassDisc)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_measurement_component(self) -> '_2002.MeasurementComponent':
        '''MeasurementComponent: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2002.MeasurementComponent.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to MeasurementComponent. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2002.MeasurementComponent)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_mountable_component(self) -> '_2003.MountableComponent':
        '''MountableComponent: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2003.MountableComponent.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to MountableComponent. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2003.MountableComponent)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_oil_seal(self) -> '_2005.OilSeal':
        '''OilSeal: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2005.OilSeal.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to OilSeal. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2005.OilSeal)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_planet_carrier(self) -> '_2007.PlanetCarrier':
        '''PlanetCarrier: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2007.PlanetCarrier.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to PlanetCarrier. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2007.PlanetCarrier)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_point_load(self) -> '_2009.PointLoad':
        '''PointLoad: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2009.PointLoad.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to PointLoad. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2009.PointLoad)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_power_load(self) -> '_2010.PowerLoad':
        '''PowerLoad: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2010.PowerLoad.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to PowerLoad. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2010.PowerLoad)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_unbalanced_mass(self) -> '_2015.UnbalancedMass':
        '''UnbalancedMass: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2015.UnbalancedMass.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to UnbalancedMass. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2015.UnbalancedMass)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_virtual_component(self) -> '_2016.VirtualComponent':
        '''VirtualComponent: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2016.VirtualComponent.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to VirtualComponent. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2016.VirtualComponent)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_shaft(self) -> '_2019.Shaft':
        '''Shaft: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2019.Shaft.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to Shaft. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2019.Shaft)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_agma_gleason_conical_gear(self) -> '_2049.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2049.AGMAGleasonConicalGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to AGMAGleasonConicalGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2049.AGMAGleasonConicalGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_bevel_differential_gear(self) -> '_2051.BevelDifferentialGear':
        '''BevelDifferentialGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2051.BevelDifferentialGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2051.BevelDifferentialGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_bevel_differential_planet_gear(self) -> '_2053.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2053.BevelDifferentialPlanetGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2053.BevelDifferentialPlanetGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_bevel_differential_sun_gear(self) -> '_2054.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2054.BevelDifferentialSunGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2054.BevelDifferentialSunGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_bevel_gear(self) -> '_2055.BevelGear':
        '''BevelGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2055.BevelGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to BevelGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2055.BevelGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_concept_gear(self) -> '_2057.ConceptGear':
        '''ConceptGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2057.ConceptGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ConceptGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2057.ConceptGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_conical_gear(self) -> '_2059.ConicalGear':
        '''ConicalGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2059.ConicalGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ConicalGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2059.ConicalGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_cylindrical_gear(self) -> '_2061.CylindricalGear':
        '''CylindricalGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2061.CylindricalGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to CylindricalGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2061.CylindricalGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_cylindrical_planet_gear(self) -> '_2063.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2063.CylindricalPlanetGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2063.CylindricalPlanetGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_face_gear(self) -> '_2064.FaceGear':
        '''FaceGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2064.FaceGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to FaceGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2064.FaceGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_gear(self) -> '_2066.Gear':
        '''Gear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2066.Gear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to Gear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2066.Gear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_hypoid_gear(self) -> '_2070.HypoidGear':
        '''HypoidGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2070.HypoidGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to HypoidGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2070.HypoidGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2072.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2072.KlingelnbergCycloPalloidConicalGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2072.KlingelnbergCycloPalloidConicalGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2074.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2074.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2074.KlingelnbergCycloPalloidHypoidGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2076.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2076.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2076.KlingelnbergCycloPalloidSpiralBevelGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_spiral_bevel_gear(self) -> '_2079.SpiralBevelGear':
        '''SpiralBevelGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2079.SpiralBevelGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to SpiralBevelGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2079.SpiralBevelGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_straight_bevel_diff_gear(self) -> '_2081.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2081.StraightBevelDiffGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2081.StraightBevelDiffGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_straight_bevel_gear(self) -> '_2083.StraightBevelGear':
        '''StraightBevelGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2083.StraightBevelGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to StraightBevelGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2083.StraightBevelGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_straight_bevel_planet_gear(self) -> '_2085.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2085.StraightBevelPlanetGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2085.StraightBevelPlanetGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_straight_bevel_sun_gear(self) -> '_2086.StraightBevelSunGear':
        '''StraightBevelSunGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2086.StraightBevelSunGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2086.StraightBevelSunGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_worm_gear(self) -> '_2087.WormGear':
        '''WormGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2087.WormGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to WormGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2087.WormGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_zerol_bevel_gear(self) -> '_2089.ZerolBevelGear':
        '''ZerolBevelGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2089.ZerolBevelGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ZerolBevelGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2089.ZerolBevelGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_clutch_half(self) -> '_2111.ClutchHalf':
        '''ClutchHalf: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2111.ClutchHalf.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ClutchHalf. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2111.ClutchHalf)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_concept_coupling_half(self) -> '_2114.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2114.ConceptCouplingHalf.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2114.ConceptCouplingHalf)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_coupling_half(self) -> '_2116.CouplingHalf':
        '''CouplingHalf: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2116.CouplingHalf.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to CouplingHalf. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2116.CouplingHalf)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_cvt_pulley(self) -> '_2118.CVTPulley':
        '''CVTPulley: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2118.CVTPulley.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to CVTPulley. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2118.CVTPulley)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_part_to_part_shear_coupling_half(self) -> '_2120.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2120.PartToPartShearCouplingHalf.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2120.PartToPartShearCouplingHalf)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_pulley(self) -> '_2121.Pulley':
        '''Pulley: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2121.Pulley.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to Pulley. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2121.Pulley)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_rolling_ring(self) -> '_2127.RollingRing':
        '''RollingRing: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2127.RollingRing.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to RollingRing. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2127.RollingRing)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_shaft_hub_connection(self) -> '_2129.ShaftHubConnection':
        '''ShaftHubConnection: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2129.ShaftHubConnection.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ShaftHubConnection. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2129.ShaftHubConnection)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_spring_damper_half(self) -> '_2131.SpringDamperHalf':
        '''SpringDamperHalf: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2131.SpringDamperHalf.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to SpringDamperHalf. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2131.SpringDamperHalf)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_synchroniser_half(self) -> '_2134.SynchroniserHalf':
        '''SynchroniserHalf: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2134.SynchroniserHalf.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to SynchroniserHalf. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2134.SynchroniserHalf)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_synchroniser_part(self) -> '_2135.SynchroniserPart':
        '''SynchroniserPart: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2135.SynchroniserPart.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to SynchroniserPart. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2135.SynchroniserPart)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_synchroniser_sleeve(self) -> '_2136.SynchroniserSleeve':
        '''SynchroniserSleeve: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2136.SynchroniserSleeve.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2136.SynchroniserSleeve)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_torque_converter_pump(self) -> '_2138.TorqueConverterPump':
        '''TorqueConverterPump: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2138.TorqueConverterPump.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to TorqueConverterPump. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2138.TorqueConverterPump)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_torque_converter_turbine(self) -> '_2140.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2140.TorqueConverterTurbine.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2140.TorqueConverterTurbine)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def report_names(self) -> 'List[str]':
        '''List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReportNames

    def output_default_report_to(self, file_path: 'str'):
        ''' 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else None)

    def get_default_report_with_encoded_images(self) -> 'str':
        ''' 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        ''' 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else None)

    def output_active_report_as_text_to(self, file_path: 'str'):
        ''' 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else None)

    def get_active_report_with_encoded_images(self) -> 'str':
        ''' 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else None, file_path if file_path else None)

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        ''' 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        '''

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else None)
        return method_result
