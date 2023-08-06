'''_1832.py

ComponentConnection
'''


from typing import Callable

from PIL.Image import Image

from mastapy._internal import constructor, conversion
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
from mastapy.system_model.connections_and_sockets import _1833
from mastapy._internal.python_net import python_net_import

_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'ComponentConnection')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentConnection',)


class ComponentConnection(_1833.ComponentMeasurer):
    '''ComponentConnection

    This is a mastapy class.
    '''

    TYPE = _COMPONENT_CONNECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ComponentConnection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def socket(self) -> 'str':
        '''str: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Socket

    @property
    def connected_components_socket(self) -> 'str':
        '''str: 'ConnectedComponentsSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ConnectedComponentsSocket

    @property
    def delete(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'Delete' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Delete

    @property
    def assembly_view(self) -> 'Image':
        '''Image: 'AssemblyView' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_image(self.wrapped.AssemblyView)
        return value

    @property
    def detail_view(self) -> 'Image':
        '''Image: 'DetailView' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_image(self.wrapped.DetailView)
        return value

    @property
    def swap(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'Swap' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Swap

    @property
    def connected_component(self) -> '_1986.Component':
        '''Component: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1986.Component)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_abstract_shaft_or_housing(self) -> '_1979.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1979.AbstractShaftOrHousing.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to AbstractShaftOrHousing. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1979.AbstractShaftOrHousing)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_bearing(self) -> '_1982.Bearing':
        '''Bearing: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1982.Bearing.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Bearing. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1982.Bearing)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_bolt(self) -> '_1984.Bolt':
        '''Bolt: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1984.Bolt.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Bolt. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1984.Bolt)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_connector(self) -> '_1989.Connector':
        '''Connector: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1989.Connector.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Connector. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1989.Connector)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_datum(self) -> '_1990.Datum':
        '''Datum: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1990.Datum.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Datum. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1990.Datum)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_external_cad_model(self) -> '_1993.ExternalCADModel':
        '''ExternalCADModel: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1993.ExternalCADModel.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ExternalCADModel. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1993.ExternalCADModel)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_guide_dxf_model(self) -> '_1995.GuideDxfModel':
        '''GuideDxfModel: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1995.GuideDxfModel.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to GuideDxfModel. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1995.GuideDxfModel)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_imported_fe_component(self) -> '_1998.ImportedFEComponent':
        '''ImportedFEComponent: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1998.ImportedFEComponent.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ImportedFEComponent. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1998.ImportedFEComponent)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_mass_disc(self) -> '_2001.MassDisc':
        '''MassDisc: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2001.MassDisc.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to MassDisc. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2001.MassDisc)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_measurement_component(self) -> '_2002.MeasurementComponent':
        '''MeasurementComponent: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2002.MeasurementComponent.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to MeasurementComponent. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2002.MeasurementComponent)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_mountable_component(self) -> '_2003.MountableComponent':
        '''MountableComponent: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2003.MountableComponent.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to MountableComponent. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2003.MountableComponent)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_oil_seal(self) -> '_2005.OilSeal':
        '''OilSeal: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2005.OilSeal.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to OilSeal. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2005.OilSeal)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_planet_carrier(self) -> '_2007.PlanetCarrier':
        '''PlanetCarrier: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2007.PlanetCarrier.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to PlanetCarrier. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2007.PlanetCarrier)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_point_load(self) -> '_2009.PointLoad':
        '''PointLoad: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2009.PointLoad.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to PointLoad. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2009.PointLoad)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_power_load(self) -> '_2010.PowerLoad':
        '''PowerLoad: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2010.PowerLoad.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to PowerLoad. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2010.PowerLoad)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_unbalanced_mass(self) -> '_2015.UnbalancedMass':
        '''UnbalancedMass: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2015.UnbalancedMass.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to UnbalancedMass. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2015.UnbalancedMass)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_virtual_component(self) -> '_2016.VirtualComponent':
        '''VirtualComponent: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2016.VirtualComponent.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to VirtualComponent. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2016.VirtualComponent)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_shaft(self) -> '_2019.Shaft':
        '''Shaft: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2019.Shaft.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Shaft. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2019.Shaft)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_agma_gleason_conical_gear(self) -> '_2049.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2049.AGMAGleasonConicalGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to AGMAGleasonConicalGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2049.AGMAGleasonConicalGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_bevel_differential_gear(self) -> '_2051.BevelDifferentialGear':
        '''BevelDifferentialGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2051.BevelDifferentialGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2051.BevelDifferentialGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_bevel_differential_planet_gear(self) -> '_2053.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2053.BevelDifferentialPlanetGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2053.BevelDifferentialPlanetGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_bevel_differential_sun_gear(self) -> '_2054.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2054.BevelDifferentialSunGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2054.BevelDifferentialSunGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_bevel_gear(self) -> '_2055.BevelGear':
        '''BevelGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2055.BevelGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to BevelGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2055.BevelGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_concept_gear(self) -> '_2057.ConceptGear':
        '''ConceptGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2057.ConceptGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ConceptGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2057.ConceptGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_conical_gear(self) -> '_2059.ConicalGear':
        '''ConicalGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2059.ConicalGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ConicalGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2059.ConicalGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_cylindrical_gear(self) -> '_2061.CylindricalGear':
        '''CylindricalGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2061.CylindricalGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to CylindricalGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2061.CylindricalGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_cylindrical_planet_gear(self) -> '_2063.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2063.CylindricalPlanetGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2063.CylindricalPlanetGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_face_gear(self) -> '_2064.FaceGear':
        '''FaceGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2064.FaceGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to FaceGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2064.FaceGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_gear(self) -> '_2066.Gear':
        '''Gear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2066.Gear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Gear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2066.Gear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_hypoid_gear(self) -> '_2070.HypoidGear':
        '''HypoidGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2070.HypoidGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to HypoidGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2070.HypoidGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2072.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2072.KlingelnbergCycloPalloidConicalGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2072.KlingelnbergCycloPalloidConicalGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2074.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2074.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2074.KlingelnbergCycloPalloidHypoidGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2076.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2076.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2076.KlingelnbergCycloPalloidSpiralBevelGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_spiral_bevel_gear(self) -> '_2079.SpiralBevelGear':
        '''SpiralBevelGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2079.SpiralBevelGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to SpiralBevelGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2079.SpiralBevelGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_straight_bevel_diff_gear(self) -> '_2081.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2081.StraightBevelDiffGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2081.StraightBevelDiffGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_straight_bevel_gear(self) -> '_2083.StraightBevelGear':
        '''StraightBevelGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2083.StraightBevelGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to StraightBevelGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2083.StraightBevelGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_straight_bevel_planet_gear(self) -> '_2085.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2085.StraightBevelPlanetGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2085.StraightBevelPlanetGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_straight_bevel_sun_gear(self) -> '_2086.StraightBevelSunGear':
        '''StraightBevelSunGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2086.StraightBevelSunGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2086.StraightBevelSunGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_worm_gear(self) -> '_2087.WormGear':
        '''WormGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2087.WormGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to WormGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2087.WormGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_zerol_bevel_gear(self) -> '_2089.ZerolBevelGear':
        '''ZerolBevelGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2089.ZerolBevelGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ZerolBevelGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2089.ZerolBevelGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_clutch_half(self) -> '_2111.ClutchHalf':
        '''ClutchHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2111.ClutchHalf.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ClutchHalf. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2111.ClutchHalf)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_concept_coupling_half(self) -> '_2114.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2114.ConceptCouplingHalf.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2114.ConceptCouplingHalf)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_coupling_half(self) -> '_2116.CouplingHalf':
        '''CouplingHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2116.CouplingHalf.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to CouplingHalf. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2116.CouplingHalf)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_cvt_pulley(self) -> '_2118.CVTPulley':
        '''CVTPulley: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2118.CVTPulley.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to CVTPulley. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2118.CVTPulley)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_part_to_part_shear_coupling_half(self) -> '_2120.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2120.PartToPartShearCouplingHalf.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2120.PartToPartShearCouplingHalf)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_pulley(self) -> '_2121.Pulley':
        '''Pulley: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2121.Pulley.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Pulley. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2121.Pulley)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_rolling_ring(self) -> '_2127.RollingRing':
        '''RollingRing: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2127.RollingRing.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to RollingRing. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2127.RollingRing)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_shaft_hub_connection(self) -> '_2129.ShaftHubConnection':
        '''ShaftHubConnection: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2129.ShaftHubConnection.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ShaftHubConnection. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2129.ShaftHubConnection)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_spring_damper_half(self) -> '_2131.SpringDamperHalf':
        '''SpringDamperHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2131.SpringDamperHalf.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to SpringDamperHalf. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2131.SpringDamperHalf)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_synchroniser_half(self) -> '_2134.SynchroniserHalf':
        '''SynchroniserHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2134.SynchroniserHalf.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to SynchroniserHalf. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2134.SynchroniserHalf)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_synchroniser_part(self) -> '_2135.SynchroniserPart':
        '''SynchroniserPart: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2135.SynchroniserPart.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to SynchroniserPart. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2135.SynchroniserPart)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_synchroniser_sleeve(self) -> '_2136.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2136.SynchroniserSleeve.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2136.SynchroniserSleeve)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_torque_converter_pump(self) -> '_2138.TorqueConverterPump':
        '''TorqueConverterPump: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2138.TorqueConverterPump.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to TorqueConverterPump. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2138.TorqueConverterPump)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_torque_converter_turbine(self) -> '_2140.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2140.TorqueConverterTurbine.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2140.TorqueConverterTurbine)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None
