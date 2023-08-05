'''_5459.py

PartSingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model import (
    _1986, _1957, _1958, _1959,
    _1962, _1964, _1965, _1966,
    _1969, _1970, _1973, _1974,
    _1975, _1978, _1981, _1982,
    _1983, _1985, _1987, _1989,
    _1990, _1992, _1994, _1995,
    _1996
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.shaft_model import _1999
from mastapy.system_model.part_model.gears import (
    _2029, _2030, _2031, _2032,
    _2033, _2034, _2035, _2036,
    _2037, _2038, _2039, _2040,
    _2041, _2042, _2043, _2044,
    _2045, _2046, _2048, _2050,
    _2051, _2052, _2053, _2054,
    _2055, _2056, _2057, _2058,
    _2059, _2060, _2061, _2062,
    _2063, _2064, _2065, _2066,
    _2067, _2068, _2069, _2070
)
from mastapy.system_model.part_model.couplings import (
    _2088, _2090, _2091, _2093,
    _2094, _2095, _2096, _2097,
    _2098, _2099, _2100, _2101,
    _2107, _2108, _2109, _2110,
    _2111, _2112, _2114, _2115,
    _2116, _2117, _2118, _2120
)
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5476
from mastapy.system_model.analyses_and_results.modal_analyses import (
    _4756, _4676, _4677, _4679,
    _4680, _4681, _4682, _4684,
    _4686, _4687, _4688, _4689,
    _4691, _4692, _4693, _4694,
    _4696, _4697, _4699, _4701,
    _4702, _4704, _4705, _4707,
    _4708, _4710, _4713, _4714,
    _4716, _4717, _4719, _4720,
    _4721, _4722, _4723, _4725,
    _4726, _4727, _4730, _4731,
    _4732, _4734, _4735, _4736,
    _4739, _4740, _4742, _4743,
    _4745, _4746, _4747, _4748,
    _4753, _4754, _4758, _4759,
    _4761, _4762, _4763, _4764,
    _4765, _4766, _4768, _4769,
    _4770, _4771, _4774, _4776,
    _4777, _4779, _4780, _4782,
    _4783, _4785, _4786, _4787,
    _4788, _4789, _4790, _4791,
    _4792, _4794, _4795, _4796,
    _4797, _4798, _4805, _4806,
    _4808, _4809
)
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5301
from mastapy.system_model.analyses_and_results.analysis_cases import _6471
from mastapy._internal.python_net import python_net_import

_PART_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'PartSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PartSingleMeshWhineAnalysis',)


class PartSingleMeshWhineAnalysis(_6471.PartStaticLoadAnalysisCase):
    '''PartSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _PART_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1986.Part':
        '''Part: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1986.Part)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_assembly(self) -> '_1957.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1957.Assembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Assembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1957.Assembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_abstract_assembly(self) -> '_1958.AbstractAssembly':
        '''AbstractAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1958.AbstractAssembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to AbstractAssembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1958.AbstractAssembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_abstract_shaft_or_housing(self) -> '_1959.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1959.AbstractShaftOrHousing.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to AbstractShaftOrHousing. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1959.AbstractShaftOrHousing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bearing(self) -> '_1962.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1962.Bearing.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Bearing. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1962.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bolt(self) -> '_1964.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1964.Bolt.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Bolt. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1964.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bolted_joint(self) -> '_1965.BoltedJoint':
        '''BoltedJoint: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1965.BoltedJoint.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BoltedJoint. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1965.BoltedJoint)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_component(self) -> '_1966.Component':
        '''Component: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1966.Component.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Component. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1966.Component)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_connector(self) -> '_1969.Connector':
        '''Connector: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1969.Connector.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Connector. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1969.Connector)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_datum(self) -> '_1970.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1970.Datum.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Datum. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1970.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_external_cad_model(self) -> '_1973.ExternalCADModel':
        '''ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1973.ExternalCADModel.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ExternalCADModel. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1973.ExternalCADModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_flexible_pin_assembly(self) -> '_1974.FlexiblePinAssembly':
        '''FlexiblePinAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1974.FlexiblePinAssembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to FlexiblePinAssembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1974.FlexiblePinAssembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_guide_dxf_model(self) -> '_1975.GuideDxfModel':
        '''GuideDxfModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1975.GuideDxfModel.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to GuideDxfModel. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1975.GuideDxfModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_imported_fe_component(self) -> '_1978.ImportedFEComponent':
        '''ImportedFEComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1978.ImportedFEComponent.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ImportedFEComponent. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1978.ImportedFEComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_mass_disc(self) -> '_1981.MassDisc':
        '''MassDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1981.MassDisc.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to MassDisc. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1981.MassDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_measurement_component(self) -> '_1982.MeasurementComponent':
        '''MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1982.MeasurementComponent.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to MeasurementComponent. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1982.MeasurementComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_mountable_component(self) -> '_1983.MountableComponent':
        '''MountableComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1983.MountableComponent.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to MountableComponent. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1983.MountableComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_oil_seal(self) -> '_1985.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1985.OilSeal.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to OilSeal. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1985.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_planet_carrier(self) -> '_1987.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1987.PlanetCarrier.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to PlanetCarrier. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1987.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_point_load(self) -> '_1989.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1989.PointLoad.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to PointLoad. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1989.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_power_load(self) -> '_1990.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1990.PowerLoad.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to PowerLoad. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1990.PowerLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_root_assembly(self) -> '_1992.RootAssembly':
        '''RootAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1992.RootAssembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to RootAssembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1992.RootAssembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_specialised_assembly(self) -> '_1994.SpecialisedAssembly':
        '''SpecialisedAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1994.SpecialisedAssembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SpecialisedAssembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1994.SpecialisedAssembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_unbalanced_mass(self) -> '_1995.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1995.UnbalancedMass.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to UnbalancedMass. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1995.UnbalancedMass)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_virtual_component(self) -> '_1996.VirtualComponent':
        '''VirtualComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1996.VirtualComponent.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to VirtualComponent. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1996.VirtualComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_shaft(self) -> '_1999.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1999.Shaft.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Shaft. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1999.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_agma_gleason_conical_gear(self) -> '_2029.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2029.AGMAGleasonConicalGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to AGMAGleasonConicalGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2029.AGMAGleasonConicalGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_agma_gleason_conical_gear_set(self) -> '_2030.AGMAGleasonConicalGearSet':
        '''AGMAGleasonConicalGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2030.AGMAGleasonConicalGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to AGMAGleasonConicalGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2030.AGMAGleasonConicalGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bevel_differential_gear(self) -> '_2031.BevelDifferentialGear':
        '''BevelDifferentialGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2031.BevelDifferentialGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2031.BevelDifferentialGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bevel_differential_gear_set(self) -> '_2032.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2032.BevelDifferentialGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BevelDifferentialGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2032.BevelDifferentialGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bevel_differential_planet_gear(self) -> '_2033.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2033.BevelDifferentialPlanetGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2033.BevelDifferentialPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bevel_differential_sun_gear(self) -> '_2034.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2034.BevelDifferentialSunGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2034.BevelDifferentialSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bevel_gear(self) -> '_2035.BevelGear':
        '''BevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2035.BevelGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BevelGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2035.BevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bevel_gear_set(self) -> '_2036.BevelGearSet':
        '''BevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2036.BevelGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BevelGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2036.BevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_concept_gear(self) -> '_2037.ConceptGear':
        '''ConceptGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2037.ConceptGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ConceptGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2037.ConceptGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_concept_gear_set(self) -> '_2038.ConceptGearSet':
        '''ConceptGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2038.ConceptGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ConceptGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2038.ConceptGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_conical_gear(self) -> '_2039.ConicalGear':
        '''ConicalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2039.ConicalGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ConicalGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2039.ConicalGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_conical_gear_set(self) -> '_2040.ConicalGearSet':
        '''ConicalGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2040.ConicalGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ConicalGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2040.ConicalGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cylindrical_gear(self) -> '_2041.CylindricalGear':
        '''CylindricalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2041.CylindricalGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CylindricalGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2041.CylindricalGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cylindrical_gear_set(self) -> '_2042.CylindricalGearSet':
        '''CylindricalGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2042.CylindricalGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CylindricalGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2042.CylindricalGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cylindrical_planet_gear(self) -> '_2043.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2043.CylindricalPlanetGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2043.CylindricalPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_face_gear(self) -> '_2044.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2044.FaceGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to FaceGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2044.FaceGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_face_gear_set(self) -> '_2045.FaceGearSet':
        '''FaceGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2045.FaceGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to FaceGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2045.FaceGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_gear(self) -> '_2046.Gear':
        '''Gear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2046.Gear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Gear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2046.Gear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_gear_set(self) -> '_2048.GearSet':
        '''GearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2048.GearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to GearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2048.GearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_hypoid_gear(self) -> '_2050.HypoidGear':
        '''HypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2050.HypoidGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to HypoidGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2050.HypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_hypoid_gear_set(self) -> '_2051.HypoidGearSet':
        '''HypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2051.HypoidGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to HypoidGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2051.HypoidGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2052.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2052.KlingelnbergCycloPalloidConicalGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2052.KlingelnbergCycloPalloidConicalGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_conical_gear_set(self) -> '_2053.KlingelnbergCycloPalloidConicalGearSet':
        '''KlingelnbergCycloPalloidConicalGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2053.KlingelnbergCycloPalloidConicalGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidConicalGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2053.KlingelnbergCycloPalloidConicalGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2054.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2054.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2054.KlingelnbergCycloPalloidHypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self) -> '_2055.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2055.KlingelnbergCycloPalloidHypoidGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidHypoidGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2055.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2056.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2056.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2056.KlingelnbergCycloPalloidSpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self) -> '_2057.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2057.KlingelnbergCycloPalloidSpiralBevelGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidSpiralBevelGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2057.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_planetary_gear_set(self) -> '_2058.PlanetaryGearSet':
        '''PlanetaryGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2058.PlanetaryGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to PlanetaryGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2058.PlanetaryGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_spiral_bevel_gear(self) -> '_2059.SpiralBevelGear':
        '''SpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2059.SpiralBevelGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SpiralBevelGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2059.SpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_spiral_bevel_gear_set(self) -> '_2060.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2060.SpiralBevelGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SpiralBevelGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2060.SpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_diff_gear(self) -> '_2061.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2061.StraightBevelDiffGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2061.StraightBevelDiffGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_diff_gear_set(self) -> '_2062.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2062.StraightBevelDiffGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to StraightBevelDiffGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2062.StraightBevelDiffGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_gear(self) -> '_2063.StraightBevelGear':
        '''StraightBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2063.StraightBevelGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to StraightBevelGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2063.StraightBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_gear_set(self) -> '_2064.StraightBevelGearSet':
        '''StraightBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2064.StraightBevelGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to StraightBevelGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2064.StraightBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_planet_gear(self) -> '_2065.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2065.StraightBevelPlanetGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2065.StraightBevelPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_sun_gear(self) -> '_2066.StraightBevelSunGear':
        '''StraightBevelSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2066.StraightBevelSunGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2066.StraightBevelSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_worm_gear(self) -> '_2067.WormGear':
        '''WormGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2067.WormGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to WormGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2067.WormGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_worm_gear_set(self) -> '_2068.WormGearSet':
        '''WormGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2068.WormGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to WormGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2068.WormGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_zerol_bevel_gear(self) -> '_2069.ZerolBevelGear':
        '''ZerolBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2069.ZerolBevelGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ZerolBevelGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2069.ZerolBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_zerol_bevel_gear_set(self) -> '_2070.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2070.ZerolBevelGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ZerolBevelGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2070.ZerolBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_belt_drive(self) -> '_2088.BeltDrive':
        '''BeltDrive: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2088.BeltDrive.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BeltDrive. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2088.BeltDrive)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_clutch(self) -> '_2090.Clutch':
        '''Clutch: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2090.Clutch.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Clutch. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2090.Clutch)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_clutch_half(self) -> '_2091.ClutchHalf':
        '''ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2091.ClutchHalf.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ClutchHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2091.ClutchHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_concept_coupling(self) -> '_2093.ConceptCoupling':
        '''ConceptCoupling: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2093.ConceptCoupling.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ConceptCoupling. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2093.ConceptCoupling)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_concept_coupling_half(self) -> '_2094.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2094.ConceptCouplingHalf.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2094.ConceptCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_coupling(self) -> '_2095.Coupling':
        '''Coupling: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2095.Coupling.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Coupling. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2095.Coupling)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_coupling_half(self) -> '_2096.CouplingHalf':
        '''CouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2096.CouplingHalf.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CouplingHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2096.CouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cvt(self) -> '_2097.CVT':
        '''CVT: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2097.CVT.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CVT. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2097.CVT)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cvt_pulley(self) -> '_2098.CVTPulley':
        '''CVTPulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2098.CVTPulley.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CVTPulley. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2098.CVTPulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_part_to_part_shear_coupling(self) -> '_2099.PartToPartShearCoupling':
        '''PartToPartShearCoupling: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2099.PartToPartShearCoupling.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to PartToPartShearCoupling. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2099.PartToPartShearCoupling)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_part_to_part_shear_coupling_half(self) -> '_2100.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2100.PartToPartShearCouplingHalf.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2100.PartToPartShearCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_pulley(self) -> '_2101.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2101.Pulley.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Pulley. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2101.Pulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_rolling_ring(self) -> '_2107.RollingRing':
        '''RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2107.RollingRing.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to RollingRing. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2107.RollingRing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_rolling_ring_assembly(self) -> '_2108.RollingRingAssembly':
        '''RollingRingAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2108.RollingRingAssembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to RollingRingAssembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2108.RollingRingAssembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_shaft_hub_connection(self) -> '_2109.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2109.ShaftHubConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ShaftHubConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2109.ShaftHubConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_spring_damper(self) -> '_2110.SpringDamper':
        '''SpringDamper: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2110.SpringDamper.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SpringDamper. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2110.SpringDamper)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_spring_damper_half(self) -> '_2111.SpringDamperHalf':
        '''SpringDamperHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2111.SpringDamperHalf.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SpringDamperHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2111.SpringDamperHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_synchroniser(self) -> '_2112.Synchroniser':
        '''Synchroniser: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2112.Synchroniser.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Synchroniser. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2112.Synchroniser)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_synchroniser_half(self) -> '_2114.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2114.SynchroniserHalf.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SynchroniserHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2114.SynchroniserHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_synchroniser_part(self) -> '_2115.SynchroniserPart':
        '''SynchroniserPart: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2115.SynchroniserPart.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SynchroniserPart. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2115.SynchroniserPart)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_synchroniser_sleeve(self) -> '_2116.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2116.SynchroniserSleeve.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2116.SynchroniserSleeve)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_torque_converter(self) -> '_2117.TorqueConverter':
        '''TorqueConverter: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2117.TorqueConverter.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to TorqueConverter. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2117.TorqueConverter)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_torque_converter_pump(self) -> '_2118.TorqueConverterPump':
        '''TorqueConverterPump: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2118.TorqueConverterPump.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to TorqueConverterPump. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2118.TorqueConverterPump)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_torque_converter_turbine(self) -> '_2120.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2120.TorqueConverterTurbine.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2120.TorqueConverterTurbine)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def single_mesh_whine_analysis(self) -> '_5476.SingleMeshWhineAnalysis':
        '''SingleMeshWhineAnalysis: 'SingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5476.SingleMeshWhineAnalysis)(self.wrapped.SingleMeshWhineAnalysis) if self.wrapped.SingleMeshWhineAnalysis else None

    @property
    def uncoupled_modal_analysis(self) -> '_4756.PartModalAnalysis':
        '''PartModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4756.PartModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_abstract_assembly_modal_analysis(self) -> '_4676.AbstractAssemblyModalAnalysis':
        '''AbstractAssemblyModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4676.AbstractAssemblyModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to AbstractAssemblyModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4676.AbstractAssemblyModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_abstract_shaft_or_housing_modal_analysis(self) -> '_4677.AbstractShaftOrHousingModalAnalysis':
        '''AbstractShaftOrHousingModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4677.AbstractShaftOrHousingModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to AbstractShaftOrHousingModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4677.AbstractShaftOrHousingModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_agma_gleason_conical_gear_modal_analysis(self) -> '_4679.AGMAGleasonConicalGearModalAnalysis':
        '''AGMAGleasonConicalGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4679.AGMAGleasonConicalGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to AGMAGleasonConicalGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4679.AGMAGleasonConicalGearModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_agma_gleason_conical_gear_set_modal_analysis(self) -> '_4680.AGMAGleasonConicalGearSetModalAnalysis':
        '''AGMAGleasonConicalGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4680.AGMAGleasonConicalGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to AGMAGleasonConicalGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4680.AGMAGleasonConicalGearSetModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_assembly_modal_analysis(self) -> '_4681.AssemblyModalAnalysis':
        '''AssemblyModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4681.AssemblyModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to AssemblyModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4681.AssemblyModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_bearing_modal_analysis(self) -> '_4682.BearingModalAnalysis':
        '''BearingModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4682.BearingModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to BearingModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4682.BearingModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_belt_drive_modal_analysis(self) -> '_4684.BeltDriveModalAnalysis':
        '''BeltDriveModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4684.BeltDriveModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to BeltDriveModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4684.BeltDriveModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_bevel_differential_gear_modal_analysis(self) -> '_4686.BevelDifferentialGearModalAnalysis':
        '''BevelDifferentialGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4686.BevelDifferentialGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to BevelDifferentialGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4686.BevelDifferentialGearModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_bevel_differential_gear_set_modal_analysis(self) -> '_4687.BevelDifferentialGearSetModalAnalysis':
        '''BevelDifferentialGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4687.BevelDifferentialGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to BevelDifferentialGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4687.BevelDifferentialGearSetModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_bevel_differential_planet_gear_modal_analysis(self) -> '_4688.BevelDifferentialPlanetGearModalAnalysis':
        '''BevelDifferentialPlanetGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4688.BevelDifferentialPlanetGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to BevelDifferentialPlanetGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4688.BevelDifferentialPlanetGearModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_bevel_differential_sun_gear_modal_analysis(self) -> '_4689.BevelDifferentialSunGearModalAnalysis':
        '''BevelDifferentialSunGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4689.BevelDifferentialSunGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to BevelDifferentialSunGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4689.BevelDifferentialSunGearModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_bevel_gear_modal_analysis(self) -> '_4691.BevelGearModalAnalysis':
        '''BevelGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4691.BevelGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to BevelGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4691.BevelGearModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_bevel_gear_set_modal_analysis(self) -> '_4692.BevelGearSetModalAnalysis':
        '''BevelGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4692.BevelGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to BevelGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4692.BevelGearSetModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_bolted_joint_modal_analysis(self) -> '_4693.BoltedJointModalAnalysis':
        '''BoltedJointModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4693.BoltedJointModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to BoltedJointModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4693.BoltedJointModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_bolt_modal_analysis(self) -> '_4694.BoltModalAnalysis':
        '''BoltModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4694.BoltModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to BoltModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4694.BoltModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_clutch_half_modal_analysis(self) -> '_4696.ClutchHalfModalAnalysis':
        '''ClutchHalfModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4696.ClutchHalfModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ClutchHalfModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4696.ClutchHalfModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_clutch_modal_analysis(self) -> '_4697.ClutchModalAnalysis':
        '''ClutchModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4697.ClutchModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ClutchModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4697.ClutchModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_component_modal_analysis(self) -> '_4699.ComponentModalAnalysis':
        '''ComponentModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4699.ComponentModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ComponentModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4699.ComponentModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_concept_coupling_half_modal_analysis(self) -> '_4701.ConceptCouplingHalfModalAnalysis':
        '''ConceptCouplingHalfModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4701.ConceptCouplingHalfModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ConceptCouplingHalfModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4701.ConceptCouplingHalfModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_concept_coupling_modal_analysis(self) -> '_4702.ConceptCouplingModalAnalysis':
        '''ConceptCouplingModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4702.ConceptCouplingModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ConceptCouplingModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4702.ConceptCouplingModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_concept_gear_modal_analysis(self) -> '_4704.ConceptGearModalAnalysis':
        '''ConceptGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4704.ConceptGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ConceptGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4704.ConceptGearModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_concept_gear_set_modal_analysis(self) -> '_4705.ConceptGearSetModalAnalysis':
        '''ConceptGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4705.ConceptGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ConceptGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4705.ConceptGearSetModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_conical_gear_modal_analysis(self) -> '_4707.ConicalGearModalAnalysis':
        '''ConicalGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4707.ConicalGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ConicalGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4707.ConicalGearModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_conical_gear_set_modal_analysis(self) -> '_4708.ConicalGearSetModalAnalysis':
        '''ConicalGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4708.ConicalGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ConicalGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4708.ConicalGearSetModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_connector_modal_analysis(self) -> '_4710.ConnectorModalAnalysis':
        '''ConnectorModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4710.ConnectorModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ConnectorModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4710.ConnectorModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_coupling_half_modal_analysis(self) -> '_4713.CouplingHalfModalAnalysis':
        '''CouplingHalfModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4713.CouplingHalfModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to CouplingHalfModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4713.CouplingHalfModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_coupling_modal_analysis(self) -> '_4714.CouplingModalAnalysis':
        '''CouplingModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4714.CouplingModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to CouplingModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4714.CouplingModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_cvt_modal_analysis(self) -> '_4716.CVTModalAnalysis':
        '''CVTModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4716.CVTModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to CVTModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4716.CVTModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_cvt_pulley_modal_analysis(self) -> '_4717.CVTPulleyModalAnalysis':
        '''CVTPulleyModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4717.CVTPulleyModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to CVTPulleyModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4717.CVTPulleyModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_cylindrical_gear_modal_analysis(self) -> '_4719.CylindricalGearModalAnalysis':
        '''CylindricalGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4719.CylindricalGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to CylindricalGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4719.CylindricalGearModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_cylindrical_gear_set_modal_analysis(self) -> '_4720.CylindricalGearSetModalAnalysis':
        '''CylindricalGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4720.CylindricalGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to CylindricalGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4720.CylindricalGearSetModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_cylindrical_planet_gear_modal_analysis(self) -> '_4721.CylindricalPlanetGearModalAnalysis':
        '''CylindricalPlanetGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4721.CylindricalPlanetGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to CylindricalPlanetGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4721.CylindricalPlanetGearModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_datum_modal_analysis(self) -> '_4722.DatumModalAnalysis':
        '''DatumModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4722.DatumModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to DatumModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4722.DatumModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_external_cad_model_modal_analysis(self) -> '_4723.ExternalCADModelModalAnalysis':
        '''ExternalCADModelModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4723.ExternalCADModelModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ExternalCADModelModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4723.ExternalCADModelModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_face_gear_modal_analysis(self) -> '_4725.FaceGearModalAnalysis':
        '''FaceGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4725.FaceGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to FaceGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4725.FaceGearModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_face_gear_set_modal_analysis(self) -> '_4726.FaceGearSetModalAnalysis':
        '''FaceGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4726.FaceGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to FaceGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4726.FaceGearSetModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_flexible_pin_assembly_modal_analysis(self) -> '_4727.FlexiblePinAssemblyModalAnalysis':
        '''FlexiblePinAssemblyModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4727.FlexiblePinAssemblyModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to FlexiblePinAssemblyModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4727.FlexiblePinAssemblyModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_gear_modal_analysis(self) -> '_4730.GearModalAnalysis':
        '''GearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4730.GearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to GearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4730.GearModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_gear_set_modal_analysis(self) -> '_4731.GearSetModalAnalysis':
        '''GearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4731.GearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to GearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4731.GearSetModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_guide_dxf_model_modal_analysis(self) -> '_4732.GuideDxfModelModalAnalysis':
        '''GuideDxfModelModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4732.GuideDxfModelModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to GuideDxfModelModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4732.GuideDxfModelModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_hypoid_gear_modal_analysis(self) -> '_4734.HypoidGearModalAnalysis':
        '''HypoidGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4734.HypoidGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to HypoidGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4734.HypoidGearModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_hypoid_gear_set_modal_analysis(self) -> '_4735.HypoidGearSetModalAnalysis':
        '''HypoidGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4735.HypoidGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to HypoidGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4735.HypoidGearSetModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_imported_fe_component_modal_analysis(self) -> '_4736.ImportedFEComponentModalAnalysis':
        '''ImportedFEComponentModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4736.ImportedFEComponentModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ImportedFEComponentModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4736.ImportedFEComponentModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_klingelnberg_cyclo_palloid_conical_gear_modal_analysis(self) -> '_4739.KlingelnbergCycloPalloidConicalGearModalAnalysis':
        '''KlingelnbergCycloPalloidConicalGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4739.KlingelnbergCycloPalloidConicalGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to KlingelnbergCycloPalloidConicalGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4739.KlingelnbergCycloPalloidConicalGearModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_klingelnberg_cyclo_palloid_conical_gear_set_modal_analysis(self) -> '_4740.KlingelnbergCycloPalloidConicalGearSetModalAnalysis':
        '''KlingelnbergCycloPalloidConicalGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4740.KlingelnbergCycloPalloidConicalGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to KlingelnbergCycloPalloidConicalGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4740.KlingelnbergCycloPalloidConicalGearSetModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_klingelnberg_cyclo_palloid_hypoid_gear_modal_analysis(self) -> '_4742.KlingelnbergCycloPalloidHypoidGearModalAnalysis':
        '''KlingelnbergCycloPalloidHypoidGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4742.KlingelnbergCycloPalloidHypoidGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to KlingelnbergCycloPalloidHypoidGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4742.KlingelnbergCycloPalloidHypoidGearModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_modal_analysis(self) -> '_4743.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis':
        '''KlingelnbergCycloPalloidHypoidGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4743.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to KlingelnbergCycloPalloidHypoidGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4743.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_modal_analysis(self) -> '_4745.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis':
        '''KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4745.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4745.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_modal_analysis(self) -> '_4746.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4746.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4746.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_mass_disc_modal_analysis(self) -> '_4747.MassDiscModalAnalysis':
        '''MassDiscModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4747.MassDiscModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to MassDiscModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4747.MassDiscModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_measurement_component_modal_analysis(self) -> '_4748.MeasurementComponentModalAnalysis':
        '''MeasurementComponentModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4748.MeasurementComponentModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to MeasurementComponentModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4748.MeasurementComponentModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_mountable_component_modal_analysis(self) -> '_4753.MountableComponentModalAnalysis':
        '''MountableComponentModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4753.MountableComponentModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to MountableComponentModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4753.MountableComponentModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_oil_seal_modal_analysis(self) -> '_4754.OilSealModalAnalysis':
        '''OilSealModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4754.OilSealModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to OilSealModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4754.OilSealModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_part_to_part_shear_coupling_half_modal_analysis(self) -> '_4758.PartToPartShearCouplingHalfModalAnalysis':
        '''PartToPartShearCouplingHalfModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4758.PartToPartShearCouplingHalfModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to PartToPartShearCouplingHalfModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4758.PartToPartShearCouplingHalfModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_part_to_part_shear_coupling_modal_analysis(self) -> '_4759.PartToPartShearCouplingModalAnalysis':
        '''PartToPartShearCouplingModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4759.PartToPartShearCouplingModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to PartToPartShearCouplingModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4759.PartToPartShearCouplingModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_planetary_gear_set_modal_analysis(self) -> '_4761.PlanetaryGearSetModalAnalysis':
        '''PlanetaryGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4761.PlanetaryGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to PlanetaryGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4761.PlanetaryGearSetModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_planet_carrier_modal_analysis(self) -> '_4762.PlanetCarrierModalAnalysis':
        '''PlanetCarrierModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4762.PlanetCarrierModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to PlanetCarrierModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4762.PlanetCarrierModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_point_load_modal_analysis(self) -> '_4763.PointLoadModalAnalysis':
        '''PointLoadModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4763.PointLoadModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to PointLoadModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4763.PointLoadModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_power_load_modal_analysis(self) -> '_4764.PowerLoadModalAnalysis':
        '''PowerLoadModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4764.PowerLoadModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to PowerLoadModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4764.PowerLoadModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_pulley_modal_analysis(self) -> '_4765.PulleyModalAnalysis':
        '''PulleyModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4765.PulleyModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to PulleyModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4765.PulleyModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_rolling_ring_assembly_modal_analysis(self) -> '_4766.RollingRingAssemblyModalAnalysis':
        '''RollingRingAssemblyModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4766.RollingRingAssemblyModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to RollingRingAssemblyModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4766.RollingRingAssemblyModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_rolling_ring_modal_analysis(self) -> '_4768.RollingRingModalAnalysis':
        '''RollingRingModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4768.RollingRingModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to RollingRingModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4768.RollingRingModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_root_assembly_modal_analysis(self) -> '_4769.RootAssemblyModalAnalysis':
        '''RootAssemblyModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4769.RootAssemblyModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to RootAssemblyModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4769.RootAssemblyModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_shaft_hub_connection_modal_analysis(self) -> '_4770.ShaftHubConnectionModalAnalysis':
        '''ShaftHubConnectionModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4770.ShaftHubConnectionModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ShaftHubConnectionModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4770.ShaftHubConnectionModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_shaft_modal_analysis(self) -> '_4771.ShaftModalAnalysis':
        '''ShaftModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4771.ShaftModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ShaftModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4771.ShaftModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_specialised_assembly_modal_analysis(self) -> '_4774.SpecialisedAssemblyModalAnalysis':
        '''SpecialisedAssemblyModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4774.SpecialisedAssemblyModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to SpecialisedAssemblyModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4774.SpecialisedAssemblyModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_spiral_bevel_gear_modal_analysis(self) -> '_4776.SpiralBevelGearModalAnalysis':
        '''SpiralBevelGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4776.SpiralBevelGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to SpiralBevelGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4776.SpiralBevelGearModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_spiral_bevel_gear_set_modal_analysis(self) -> '_4777.SpiralBevelGearSetModalAnalysis':
        '''SpiralBevelGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4777.SpiralBevelGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to SpiralBevelGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4777.SpiralBevelGearSetModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_spring_damper_half_modal_analysis(self) -> '_4779.SpringDamperHalfModalAnalysis':
        '''SpringDamperHalfModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4779.SpringDamperHalfModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to SpringDamperHalfModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4779.SpringDamperHalfModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_spring_damper_modal_analysis(self) -> '_4780.SpringDamperModalAnalysis':
        '''SpringDamperModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4780.SpringDamperModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to SpringDamperModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4780.SpringDamperModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_straight_bevel_diff_gear_modal_analysis(self) -> '_4782.StraightBevelDiffGearModalAnalysis':
        '''StraightBevelDiffGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4782.StraightBevelDiffGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to StraightBevelDiffGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4782.StraightBevelDiffGearModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_straight_bevel_diff_gear_set_modal_analysis(self) -> '_4783.StraightBevelDiffGearSetModalAnalysis':
        '''StraightBevelDiffGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4783.StraightBevelDiffGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to StraightBevelDiffGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4783.StraightBevelDiffGearSetModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_straight_bevel_gear_modal_analysis(self) -> '_4785.StraightBevelGearModalAnalysis':
        '''StraightBevelGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4785.StraightBevelGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to StraightBevelGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4785.StraightBevelGearModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_straight_bevel_gear_set_modal_analysis(self) -> '_4786.StraightBevelGearSetModalAnalysis':
        '''StraightBevelGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4786.StraightBevelGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to StraightBevelGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4786.StraightBevelGearSetModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_straight_bevel_planet_gear_modal_analysis(self) -> '_4787.StraightBevelPlanetGearModalAnalysis':
        '''StraightBevelPlanetGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4787.StraightBevelPlanetGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to StraightBevelPlanetGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4787.StraightBevelPlanetGearModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_straight_bevel_sun_gear_modal_analysis(self) -> '_4788.StraightBevelSunGearModalAnalysis':
        '''StraightBevelSunGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4788.StraightBevelSunGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to StraightBevelSunGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4788.StraightBevelSunGearModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_synchroniser_half_modal_analysis(self) -> '_4789.SynchroniserHalfModalAnalysis':
        '''SynchroniserHalfModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4789.SynchroniserHalfModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to SynchroniserHalfModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4789.SynchroniserHalfModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_synchroniser_modal_analysis(self) -> '_4790.SynchroniserModalAnalysis':
        '''SynchroniserModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4790.SynchroniserModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to SynchroniserModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4790.SynchroniserModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_synchroniser_part_modal_analysis(self) -> '_4791.SynchroniserPartModalAnalysis':
        '''SynchroniserPartModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4791.SynchroniserPartModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to SynchroniserPartModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4791.SynchroniserPartModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_synchroniser_sleeve_modal_analysis(self) -> '_4792.SynchroniserSleeveModalAnalysis':
        '''SynchroniserSleeveModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4792.SynchroniserSleeveModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to SynchroniserSleeveModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4792.SynchroniserSleeveModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_torque_converter_modal_analysis(self) -> '_4794.TorqueConverterModalAnalysis':
        '''TorqueConverterModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4794.TorqueConverterModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to TorqueConverterModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4794.TorqueConverterModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_torque_converter_pump_modal_analysis(self) -> '_4795.TorqueConverterPumpModalAnalysis':
        '''TorqueConverterPumpModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4795.TorqueConverterPumpModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to TorqueConverterPumpModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4795.TorqueConverterPumpModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_torque_converter_turbine_modal_analysis(self) -> '_4796.TorqueConverterTurbineModalAnalysis':
        '''TorqueConverterTurbineModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4796.TorqueConverterTurbineModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to TorqueConverterTurbineModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4796.TorqueConverterTurbineModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_unbalanced_mass_modal_analysis(self) -> '_4797.UnbalancedMassModalAnalysis':
        '''UnbalancedMassModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4797.UnbalancedMassModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to UnbalancedMassModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4797.UnbalancedMassModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_virtual_component_modal_analysis(self) -> '_4798.VirtualComponentModalAnalysis':
        '''VirtualComponentModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4798.VirtualComponentModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to VirtualComponentModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4798.VirtualComponentModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_worm_gear_modal_analysis(self) -> '_4805.WormGearModalAnalysis':
        '''WormGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4805.WormGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to WormGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4805.WormGearModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_worm_gear_set_modal_analysis(self) -> '_4806.WormGearSetModalAnalysis':
        '''WormGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4806.WormGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to WormGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4806.WormGearSetModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_zerol_bevel_gear_modal_analysis(self) -> '_4808.ZerolBevelGearModalAnalysis':
        '''ZerolBevelGearModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4808.ZerolBevelGearModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ZerolBevelGearModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4808.ZerolBevelGearModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def uncoupled_modal_analysis_of_type_zerol_bevel_gear_set_modal_analysis(self) -> '_4809.ZerolBevelGearSetModalAnalysis':
        '''ZerolBevelGearSetModalAnalysis: 'UncoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4809.ZerolBevelGearSetModalAnalysis.TYPE not in self.wrapped.UncoupledModalAnalysis.__class__.__mro__:
            raise CastException('Failed to cast uncoupled_modal_analysis to ZerolBevelGearSetModalAnalysis. Expected: {}.'.format(self.wrapped.UncoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_4809.ZerolBevelGearSetModalAnalysis)(self.wrapped.UncoupledModalAnalysis) if self.wrapped.UncoupledModalAnalysis else None

    @property
    def gear_whine_analysis_settings(self) -> '_5301.GearWhineAnalysisOptions':
        '''GearWhineAnalysisOptions: 'GearWhineAnalysisSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5301.GearWhineAnalysisOptions)(self.wrapped.GearWhineAnalysisSettings) if self.wrapped.GearWhineAnalysisSettings else None
