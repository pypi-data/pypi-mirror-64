'''_2182.py

CompoundSystemDeflectionAnalysis
'''


from typing import Iterable

from mastapy.system_model.part_model import (
    _1958, _1959, _1962, _1964,
    _1965, _1966, _1969, _1970,
    _1973, _1974, _1957, _1975,
    _1978, _1981, _1982, _1983,
    _1985, _1986, _1987, _1989,
    _1990, _1992, _1994, _1995,
    _1996
)
from mastapy.system_model.analyses_and_results.system_deflections.compound import (
    _2332, _2333, _2338, _2349,
    _2350, _2355, _2366, _2377,
    _2378, _2382, _2337, _2386,
    _2390, _2401, _2402, _2403,
    _2404, _2405, _2411, _2412,
    _2413, _2418, _2423, _2446,
    _2447, _2419, _2359, _2361,
    _2379, _2381, _2334, _2336,
    _2341, _2343, _2344, _2345,
    _2346, _2348, _2362, _2364,
    _2373, _2375, _2376, _2383,
    _2385, _2387, _2389, _2392,
    _2394, _2395, _2397, _2398,
    _2400, _2410, _2424, _2426,
    _2430, _2432, _2433, _2435,
    _2436, _2437, _2448, _2450,
    _2451, _2453, _2406, _2408,
    _2340, _2351, _2353, _2356,
    _2358, _2367, _2369, _2371,
    _2372, _2414, _2421, _2416,
    _2415, _2427, _2429, _2438,
    _2439, _2440, _2441, _2442,
    _2444, _2445, _2370, _2339,
    _2354, _2365, _2391, _2409,
    _2417, _2422, _2342, _2360,
    _2380, _2431, _2347, _2363,
    _2335, _2374, _2388, _2393,
    _2396, _2399, _2425, _2434,
    _2449, _2452, _2384, _2407,
    _2352, _2357, _2368, _2428,
    _2443
)
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.shaft_model import _1999
from mastapy.system_model.part_model.gears import (
    _2037, _2038, _2044, _2045,
    _2029, _2030, _2031, _2032,
    _2033, _2034, _2035, _2036,
    _2039, _2040, _2041, _2042,
    _2043, _2046, _2048, _2050,
    _2051, _2052, _2053, _2054,
    _2055, _2056, _2057, _2058,
    _2059, _2060, _2061, _2062,
    _2063, _2064, _2065, _2066,
    _2067, _2068, _2069, _2070
)
from mastapy.system_model.part_model.couplings import (
    _2099, _2100, _2088, _2090,
    _2091, _2093, _2094, _2095,
    _2096, _2097, _2098, _2101,
    _2109, _2107, _2108, _2110,
    _2111, _2112, _2114, _2115,
    _2116, _2117, _2118, _2120
)
from mastapy.system_model.connections_and_sockets import (
    _1815, _1810, _1811, _1814,
    _1823, _1826, _1830, _1834
)
from mastapy.system_model.connections_and_sockets.gears import (
    _1840, _1844, _1850, _1864,
    _1842, _1846, _1838, _1848,
    _1854, _1857, _1858, _1859,
    _1862, _1866, _1868, _1870,
    _1852
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _1878, _1872, _1874, _1876,
    _1880, _1882
)
from mastapy.system_model.analyses_and_results import _2129
from mastapy._internal.python_net import python_net_import

_COMPOUND_SYSTEM_DEFLECTION_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundSystemDeflectionAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundSystemDeflectionAnalysis',)


class CompoundSystemDeflectionAnalysis(_2129.CompoundAnalysis):
    '''CompoundSystemDeflectionAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_SYSTEM_DEFLECTION_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundSystemDeflectionAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    def results_for_abstract_assembly(self, design_entity: '_1958.AbstractAssembly') -> 'Iterable[_2332.AbstractAssemblyCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.AbstractAssemblyCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2332.AbstractAssemblyCompoundSystemDeflection))

    def results_for_abstract_shaft_or_housing(self, design_entity: '_1959.AbstractShaftOrHousing') -> 'Iterable[_2333.AbstractShaftOrHousingCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.AbstractShaftOrHousingCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2333.AbstractShaftOrHousingCompoundSystemDeflection))

    def results_for_bearing(self, design_entity: '_1962.Bearing') -> 'Iterable[_2338.BearingCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.BearingCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2338.BearingCompoundSystemDeflection))

    def results_for_bolt(self, design_entity: '_1964.Bolt') -> 'Iterable[_2349.BoltCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.BoltCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2349.BoltCompoundSystemDeflection))

    def results_for_bolted_joint(self, design_entity: '_1965.BoltedJoint') -> 'Iterable[_2350.BoltedJointCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.BoltedJointCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2350.BoltedJointCompoundSystemDeflection))

    def results_for_component(self, design_entity: '_1966.Component') -> 'Iterable[_2355.ComponentCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.ComponentCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2355.ComponentCompoundSystemDeflection))

    def results_for_connector(self, design_entity: '_1969.Connector') -> 'Iterable[_2366.ConnectorCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.ConnectorCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2366.ConnectorCompoundSystemDeflection))

    def results_for_datum(self, design_entity: '_1970.Datum') -> 'Iterable[_2377.DatumCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.DatumCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2377.DatumCompoundSystemDeflection))

    def results_for_external_cad_model(self, design_entity: '_1973.ExternalCADModel') -> 'Iterable[_2378.ExternalCADModelCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.ExternalCADModelCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2378.ExternalCADModelCompoundSystemDeflection))

    def results_for_flexible_pin_assembly(self, design_entity: '_1974.FlexiblePinAssembly') -> 'Iterable[_2382.FlexiblePinAssemblyCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.FlexiblePinAssemblyCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2382.FlexiblePinAssemblyCompoundSystemDeflection))

    def results_for_assembly(self, design_entity: '_1957.Assembly') -> 'Iterable[_2337.AssemblyCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.AssemblyCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2337.AssemblyCompoundSystemDeflection))

    def results_for_guide_dxf_model(self, design_entity: '_1975.GuideDxfModel') -> 'Iterable[_2386.GuideDxfModelCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.GuideDxfModelCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2386.GuideDxfModelCompoundSystemDeflection))

    def results_for_imported_fe_component(self, design_entity: '_1978.ImportedFEComponent') -> 'Iterable[_2390.ImportedFEComponentCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.ImportedFEComponentCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2390.ImportedFEComponentCompoundSystemDeflection))

    def results_for_mass_disc(self, design_entity: '_1981.MassDisc') -> 'Iterable[_2401.MassDiscCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.MassDiscCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2401.MassDiscCompoundSystemDeflection))

    def results_for_measurement_component(self, design_entity: '_1982.MeasurementComponent') -> 'Iterable[_2402.MeasurementComponentCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.MeasurementComponentCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2402.MeasurementComponentCompoundSystemDeflection))

    def results_for_mountable_component(self, design_entity: '_1983.MountableComponent') -> 'Iterable[_2403.MountableComponentCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.MountableComponentCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2403.MountableComponentCompoundSystemDeflection))

    def results_for_oil_seal(self, design_entity: '_1985.OilSeal') -> 'Iterable[_2404.OilSealCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.OilSealCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2404.OilSealCompoundSystemDeflection))

    def results_for_part(self, design_entity: '_1986.Part') -> 'Iterable[_2405.PartCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.PartCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2405.PartCompoundSystemDeflection))

    def results_for_planet_carrier(self, design_entity: '_1987.PlanetCarrier') -> 'Iterable[_2411.PlanetCarrierCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.PlanetCarrierCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2411.PlanetCarrierCompoundSystemDeflection))

    def results_for_point_load(self, design_entity: '_1989.PointLoad') -> 'Iterable[_2412.PointLoadCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.PointLoadCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2412.PointLoadCompoundSystemDeflection))

    def results_for_power_load(self, design_entity: '_1990.PowerLoad') -> 'Iterable[_2413.PowerLoadCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.PowerLoadCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2413.PowerLoadCompoundSystemDeflection))

    def results_for_root_assembly(self, design_entity: '_1992.RootAssembly') -> 'Iterable[_2418.RootAssemblyCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.RootAssemblyCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2418.RootAssemblyCompoundSystemDeflection))

    def results_for_specialised_assembly(self, design_entity: '_1994.SpecialisedAssembly') -> 'Iterable[_2423.SpecialisedAssemblyCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.SpecialisedAssemblyCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2423.SpecialisedAssemblyCompoundSystemDeflection))

    def results_for_unbalanced_mass(self, design_entity: '_1995.UnbalancedMass') -> 'Iterable[_2446.UnbalancedMassCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.UnbalancedMassCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2446.UnbalancedMassCompoundSystemDeflection))

    def results_for_virtual_component(self, design_entity: '_1996.VirtualComponent') -> 'Iterable[_2447.VirtualComponentCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.VirtualComponentCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2447.VirtualComponentCompoundSystemDeflection))

    def results_for_shaft(self, design_entity: '_1999.Shaft') -> 'Iterable[_2419.ShaftCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.ShaftCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2419.ShaftCompoundSystemDeflection))

    def results_for_concept_gear(self, design_entity: '_2037.ConceptGear') -> 'Iterable[_2359.ConceptGearCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.ConceptGearCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2359.ConceptGearCompoundSystemDeflection))

    def results_for_concept_gear_set(self, design_entity: '_2038.ConceptGearSet') -> 'Iterable[_2361.ConceptGearSetCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.ConceptGearSetCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2361.ConceptGearSetCompoundSystemDeflection))

    def results_for_face_gear(self, design_entity: '_2044.FaceGear') -> 'Iterable[_2379.FaceGearCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.FaceGearCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2379.FaceGearCompoundSystemDeflection))

    def results_for_face_gear_set(self, design_entity: '_2045.FaceGearSet') -> 'Iterable[_2381.FaceGearSetCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.FaceGearSetCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2381.FaceGearSetCompoundSystemDeflection))

    def results_for_agma_gleason_conical_gear(self, design_entity: '_2029.AGMAGleasonConicalGear') -> 'Iterable[_2334.AGMAGleasonConicalGearCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.AGMAGleasonConicalGearCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2334.AGMAGleasonConicalGearCompoundSystemDeflection))

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_2030.AGMAGleasonConicalGearSet') -> 'Iterable[_2336.AGMAGleasonConicalGearSetCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.AGMAGleasonConicalGearSetCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2336.AGMAGleasonConicalGearSetCompoundSystemDeflection))

    def results_for_bevel_differential_gear(self, design_entity: '_2031.BevelDifferentialGear') -> 'Iterable[_2341.BevelDifferentialGearCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.BevelDifferentialGearCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2341.BevelDifferentialGearCompoundSystemDeflection))

    def results_for_bevel_differential_gear_set(self, design_entity: '_2032.BevelDifferentialGearSet') -> 'Iterable[_2343.BevelDifferentialGearSetCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.BevelDifferentialGearSetCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2343.BevelDifferentialGearSetCompoundSystemDeflection))

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2033.BevelDifferentialPlanetGear') -> 'Iterable[_2344.BevelDifferentialPlanetGearCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.BevelDifferentialPlanetGearCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2344.BevelDifferentialPlanetGearCompoundSystemDeflection))

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2034.BevelDifferentialSunGear') -> 'Iterable[_2345.BevelDifferentialSunGearCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.BevelDifferentialSunGearCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2345.BevelDifferentialSunGearCompoundSystemDeflection))

    def results_for_bevel_gear(self, design_entity: '_2035.BevelGear') -> 'Iterable[_2346.BevelGearCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.BevelGearCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2346.BevelGearCompoundSystemDeflection))

    def results_for_bevel_gear_set(self, design_entity: '_2036.BevelGearSet') -> 'Iterable[_2348.BevelGearSetCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.BevelGearSetCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2348.BevelGearSetCompoundSystemDeflection))

    def results_for_conical_gear(self, design_entity: '_2039.ConicalGear') -> 'Iterable[_2362.ConicalGearCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.ConicalGearCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2362.ConicalGearCompoundSystemDeflection))

    def results_for_conical_gear_set(self, design_entity: '_2040.ConicalGearSet') -> 'Iterable[_2364.ConicalGearSetCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.ConicalGearSetCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2364.ConicalGearSetCompoundSystemDeflection))

    def results_for_cylindrical_gear(self, design_entity: '_2041.CylindricalGear') -> 'Iterable[_2373.CylindricalGearCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.CylindricalGearCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2373.CylindricalGearCompoundSystemDeflection))

    def results_for_cylindrical_gear_set(self, design_entity: '_2042.CylindricalGearSet') -> 'Iterable[_2375.CylindricalGearSetCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.CylindricalGearSetCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2375.CylindricalGearSetCompoundSystemDeflection))

    def results_for_cylindrical_planet_gear(self, design_entity: '_2043.CylindricalPlanetGear') -> 'Iterable[_2376.CylindricalPlanetGearCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.CylindricalPlanetGearCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2376.CylindricalPlanetGearCompoundSystemDeflection))

    def results_for_gear(self, design_entity: '_2046.Gear') -> 'Iterable[_2383.GearCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.GearCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2383.GearCompoundSystemDeflection))

    def results_for_gear_set(self, design_entity: '_2048.GearSet') -> 'Iterable[_2385.GearSetCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.GearSetCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2385.GearSetCompoundSystemDeflection))

    def results_for_hypoid_gear(self, design_entity: '_2050.HypoidGear') -> 'Iterable[_2387.HypoidGearCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.HypoidGearCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2387.HypoidGearCompoundSystemDeflection))

    def results_for_hypoid_gear_set(self, design_entity: '_2051.HypoidGearSet') -> 'Iterable[_2389.HypoidGearSetCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.HypoidGearSetCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2389.HypoidGearSetCompoundSystemDeflection))

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2052.KlingelnbergCycloPalloidConicalGear') -> 'Iterable[_2392.KlingelnbergCycloPalloidConicalGearCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.KlingelnbergCycloPalloidConicalGearCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2392.KlingelnbergCycloPalloidConicalGearCompoundSystemDeflection))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2053.KlingelnbergCycloPalloidConicalGearSet') -> 'Iterable[_2394.KlingelnbergCycloPalloidConicalGearSetCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.KlingelnbergCycloPalloidConicalGearSetCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2394.KlingelnbergCycloPalloidConicalGearSetCompoundSystemDeflection))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2054.KlingelnbergCycloPalloidHypoidGear') -> 'Iterable[_2395.KlingelnbergCycloPalloidHypoidGearCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.KlingelnbergCycloPalloidHypoidGearCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2395.KlingelnbergCycloPalloidHypoidGearCompoundSystemDeflection))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2055.KlingelnbergCycloPalloidHypoidGearSet') -> 'Iterable[_2397.KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2397.KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2056.KlingelnbergCycloPalloidSpiralBevelGear') -> 'Iterable[_2398.KlingelnbergCycloPalloidSpiralBevelGearCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.KlingelnbergCycloPalloidSpiralBevelGearCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2398.KlingelnbergCycloPalloidSpiralBevelGearCompoundSystemDeflection))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2057.KlingelnbergCycloPalloidSpiralBevelGearSet') -> 'Iterable[_2400.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2400.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSystemDeflection))

    def results_for_planetary_gear_set(self, design_entity: '_2058.PlanetaryGearSet') -> 'Iterable[_2410.PlanetaryGearSetCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.PlanetaryGearSetCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2410.PlanetaryGearSetCompoundSystemDeflection))

    def results_for_spiral_bevel_gear(self, design_entity: '_2059.SpiralBevelGear') -> 'Iterable[_2424.SpiralBevelGearCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.SpiralBevelGearCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2424.SpiralBevelGearCompoundSystemDeflection))

    def results_for_spiral_bevel_gear_set(self, design_entity: '_2060.SpiralBevelGearSet') -> 'Iterable[_2426.SpiralBevelGearSetCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.SpiralBevelGearSetCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2426.SpiralBevelGearSetCompoundSystemDeflection))

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2061.StraightBevelDiffGear') -> 'Iterable[_2430.StraightBevelDiffGearCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.StraightBevelDiffGearCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2430.StraightBevelDiffGearCompoundSystemDeflection))

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_2062.StraightBevelDiffGearSet') -> 'Iterable[_2432.StraightBevelDiffGearSetCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.StraightBevelDiffGearSetCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2432.StraightBevelDiffGearSetCompoundSystemDeflection))

    def results_for_straight_bevel_gear(self, design_entity: '_2063.StraightBevelGear') -> 'Iterable[_2433.StraightBevelGearCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.StraightBevelGearCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2433.StraightBevelGearCompoundSystemDeflection))

    def results_for_straight_bevel_gear_set(self, design_entity: '_2064.StraightBevelGearSet') -> 'Iterable[_2435.StraightBevelGearSetCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.StraightBevelGearSetCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2435.StraightBevelGearSetCompoundSystemDeflection))

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2065.StraightBevelPlanetGear') -> 'Iterable[_2436.StraightBevelPlanetGearCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.StraightBevelPlanetGearCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2436.StraightBevelPlanetGearCompoundSystemDeflection))

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2066.StraightBevelSunGear') -> 'Iterable[_2437.StraightBevelSunGearCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.StraightBevelSunGearCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2437.StraightBevelSunGearCompoundSystemDeflection))

    def results_for_worm_gear(self, design_entity: '_2067.WormGear') -> 'Iterable[_2448.WormGearCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.WormGearCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2448.WormGearCompoundSystemDeflection))

    def results_for_worm_gear_set(self, design_entity: '_2068.WormGearSet') -> 'Iterable[_2450.WormGearSetCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.WormGearSetCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2450.WormGearSetCompoundSystemDeflection))

    def results_for_zerol_bevel_gear(self, design_entity: '_2069.ZerolBevelGear') -> 'Iterable[_2451.ZerolBevelGearCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.ZerolBevelGearCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2451.ZerolBevelGearCompoundSystemDeflection))

    def results_for_zerol_bevel_gear_set(self, design_entity: '_2070.ZerolBevelGearSet') -> 'Iterable[_2453.ZerolBevelGearSetCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.ZerolBevelGearSetCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2453.ZerolBevelGearSetCompoundSystemDeflection))

    def results_for_part_to_part_shear_coupling(self, design_entity: '_2099.PartToPartShearCoupling') -> 'Iterable[_2406.PartToPartShearCouplingCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.PartToPartShearCouplingCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2406.PartToPartShearCouplingCompoundSystemDeflection))

    def results_for_part_to_part_shear_coupling_half(self, design_entity: '_2100.PartToPartShearCouplingHalf') -> 'Iterable[_2408.PartToPartShearCouplingHalfCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.PartToPartShearCouplingHalfCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2408.PartToPartShearCouplingHalfCompoundSystemDeflection))

    def results_for_belt_drive(self, design_entity: '_2088.BeltDrive') -> 'Iterable[_2340.BeltDriveCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.BeltDriveCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2340.BeltDriveCompoundSystemDeflection))

    def results_for_clutch(self, design_entity: '_2090.Clutch') -> 'Iterable[_2351.ClutchCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.ClutchCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2351.ClutchCompoundSystemDeflection))

    def results_for_clutch_half(self, design_entity: '_2091.ClutchHalf') -> 'Iterable[_2353.ClutchHalfCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.ClutchHalfCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2353.ClutchHalfCompoundSystemDeflection))

    def results_for_concept_coupling(self, design_entity: '_2093.ConceptCoupling') -> 'Iterable[_2356.ConceptCouplingCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.ConceptCouplingCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2356.ConceptCouplingCompoundSystemDeflection))

    def results_for_concept_coupling_half(self, design_entity: '_2094.ConceptCouplingHalf') -> 'Iterable[_2358.ConceptCouplingHalfCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.ConceptCouplingHalfCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2358.ConceptCouplingHalfCompoundSystemDeflection))

    def results_for_coupling(self, design_entity: '_2095.Coupling') -> 'Iterable[_2367.CouplingCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.CouplingCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2367.CouplingCompoundSystemDeflection))

    def results_for_coupling_half(self, design_entity: '_2096.CouplingHalf') -> 'Iterable[_2369.CouplingHalfCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.CouplingHalfCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2369.CouplingHalfCompoundSystemDeflection))

    def results_for_cvt(self, design_entity: '_2097.CVT') -> 'Iterable[_2371.CVTCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.CVTCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2371.CVTCompoundSystemDeflection))

    def results_for_cvt_pulley(self, design_entity: '_2098.CVTPulley') -> 'Iterable[_2372.CVTPulleyCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.CVTPulleyCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2372.CVTPulleyCompoundSystemDeflection))

    def results_for_pulley(self, design_entity: '_2101.Pulley') -> 'Iterable[_2414.PulleyCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.PulleyCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2414.PulleyCompoundSystemDeflection))

    def results_for_shaft_hub_connection(self, design_entity: '_2109.ShaftHubConnection') -> 'Iterable[_2421.ShaftHubConnectionCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.ShaftHubConnectionCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2421.ShaftHubConnectionCompoundSystemDeflection))

    def results_for_rolling_ring(self, design_entity: '_2107.RollingRing') -> 'Iterable[_2416.RollingRingCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.RollingRingCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2416.RollingRingCompoundSystemDeflection))

    def results_for_rolling_ring_assembly(self, design_entity: '_2108.RollingRingAssembly') -> 'Iterable[_2415.RollingRingAssemblyCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.RollingRingAssemblyCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2415.RollingRingAssemblyCompoundSystemDeflection))

    def results_for_spring_damper(self, design_entity: '_2110.SpringDamper') -> 'Iterable[_2427.SpringDamperCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.SpringDamperCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2427.SpringDamperCompoundSystemDeflection))

    def results_for_spring_damper_half(self, design_entity: '_2111.SpringDamperHalf') -> 'Iterable[_2429.SpringDamperHalfCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.SpringDamperHalfCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2429.SpringDamperHalfCompoundSystemDeflection))

    def results_for_synchroniser(self, design_entity: '_2112.Synchroniser') -> 'Iterable[_2438.SynchroniserCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.SynchroniserCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2438.SynchroniserCompoundSystemDeflection))

    def results_for_synchroniser_half(self, design_entity: '_2114.SynchroniserHalf') -> 'Iterable[_2439.SynchroniserHalfCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.SynchroniserHalfCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2439.SynchroniserHalfCompoundSystemDeflection))

    def results_for_synchroniser_part(self, design_entity: '_2115.SynchroniserPart') -> 'Iterable[_2440.SynchroniserPartCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.SynchroniserPartCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2440.SynchroniserPartCompoundSystemDeflection))

    def results_for_synchroniser_sleeve(self, design_entity: '_2116.SynchroniserSleeve') -> 'Iterable[_2441.SynchroniserSleeveCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.SynchroniserSleeveCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2441.SynchroniserSleeveCompoundSystemDeflection))

    def results_for_torque_converter(self, design_entity: '_2117.TorqueConverter') -> 'Iterable[_2442.TorqueConverterCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.TorqueConverterCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2442.TorqueConverterCompoundSystemDeflection))

    def results_for_torque_converter_pump(self, design_entity: '_2118.TorqueConverterPump') -> 'Iterable[_2444.TorqueConverterPumpCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.TorqueConverterPumpCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2444.TorqueConverterPumpCompoundSystemDeflection))

    def results_for_torque_converter_turbine(self, design_entity: '_2120.TorqueConverterTurbine') -> 'Iterable[_2445.TorqueConverterTurbineCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.TorqueConverterTurbineCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2445.TorqueConverterTurbineCompoundSystemDeflection))

    def results_for_cvt_belt_connection(self, design_entity: '_1815.CVTBeltConnection') -> 'Iterable[_2370.CVTBeltConnectionCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.CVTBeltConnectionCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2370.CVTBeltConnectionCompoundSystemDeflection))

    def results_for_belt_connection(self, design_entity: '_1810.BeltConnection') -> 'Iterable[_2339.BeltConnectionCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.BeltConnectionCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2339.BeltConnectionCompoundSystemDeflection))

    def results_for_coaxial_connection(self, design_entity: '_1811.CoaxialConnection') -> 'Iterable[_2354.CoaxialConnectionCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.CoaxialConnectionCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2354.CoaxialConnectionCompoundSystemDeflection))

    def results_for_connection(self, design_entity: '_1814.Connection') -> 'Iterable[_2365.ConnectionCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.ConnectionCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2365.ConnectionCompoundSystemDeflection))

    def results_for_inter_mountable_component_connection(self, design_entity: '_1823.InterMountableComponentConnection') -> 'Iterable[_2391.InterMountableComponentConnectionCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.InterMountableComponentConnectionCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2391.InterMountableComponentConnectionCompoundSystemDeflection))

    def results_for_planetary_connection(self, design_entity: '_1826.PlanetaryConnection') -> 'Iterable[_2409.PlanetaryConnectionCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.PlanetaryConnectionCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2409.PlanetaryConnectionCompoundSystemDeflection))

    def results_for_rolling_ring_connection(self, design_entity: '_1830.RollingRingConnection') -> 'Iterable[_2417.RollingRingConnectionCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.RollingRingConnectionCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2417.RollingRingConnectionCompoundSystemDeflection))

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1834.ShaftToMountableComponentConnection') -> 'Iterable[_2422.ShaftToMountableComponentConnectionCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.ShaftToMountableComponentConnectionCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2422.ShaftToMountableComponentConnectionCompoundSystemDeflection))

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1840.BevelDifferentialGearMesh') -> 'Iterable[_2342.BevelDifferentialGearMeshCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.BevelDifferentialGearMeshCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2342.BevelDifferentialGearMeshCompoundSystemDeflection))

    def results_for_concept_gear_mesh(self, design_entity: '_1844.ConceptGearMesh') -> 'Iterable[_2360.ConceptGearMeshCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.ConceptGearMeshCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2360.ConceptGearMeshCompoundSystemDeflection))

    def results_for_face_gear_mesh(self, design_entity: '_1850.FaceGearMesh') -> 'Iterable[_2380.FaceGearMeshCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.FaceGearMeshCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2380.FaceGearMeshCompoundSystemDeflection))

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1864.StraightBevelDiffGearMesh') -> 'Iterable[_2431.StraightBevelDiffGearMeshCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.StraightBevelDiffGearMeshCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2431.StraightBevelDiffGearMeshCompoundSystemDeflection))

    def results_for_bevel_gear_mesh(self, design_entity: '_1842.BevelGearMesh') -> 'Iterable[_2347.BevelGearMeshCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.BevelGearMeshCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2347.BevelGearMeshCompoundSystemDeflection))

    def results_for_conical_gear_mesh(self, design_entity: '_1846.ConicalGearMesh') -> 'Iterable[_2363.ConicalGearMeshCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.ConicalGearMeshCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2363.ConicalGearMeshCompoundSystemDeflection))

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1838.AGMAGleasonConicalGearMesh') -> 'Iterable[_2335.AGMAGleasonConicalGearMeshCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.AGMAGleasonConicalGearMeshCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2335.AGMAGleasonConicalGearMeshCompoundSystemDeflection))

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1848.CylindricalGearMesh') -> 'Iterable[_2374.CylindricalGearMeshCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.CylindricalGearMeshCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2374.CylindricalGearMeshCompoundSystemDeflection))

    def results_for_hypoid_gear_mesh(self, design_entity: '_1854.HypoidGearMesh') -> 'Iterable[_2388.HypoidGearMeshCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.HypoidGearMeshCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2388.HypoidGearMeshCompoundSystemDeflection))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1857.KlingelnbergCycloPalloidConicalGearMesh') -> 'Iterable[_2393.KlingelnbergCycloPalloidConicalGearMeshCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.KlingelnbergCycloPalloidConicalGearMeshCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2393.KlingelnbergCycloPalloidConicalGearMeshCompoundSystemDeflection))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1858.KlingelnbergCycloPalloidHypoidGearMesh') -> 'Iterable[_2396.KlingelnbergCycloPalloidHypoidGearMeshCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.KlingelnbergCycloPalloidHypoidGearMeshCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2396.KlingelnbergCycloPalloidHypoidGearMeshCompoundSystemDeflection))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1859.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> 'Iterable[_2399.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2399.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSystemDeflection))

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1862.SpiralBevelGearMesh') -> 'Iterable[_2425.SpiralBevelGearMeshCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.SpiralBevelGearMeshCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2425.SpiralBevelGearMeshCompoundSystemDeflection))

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1866.StraightBevelGearMesh') -> 'Iterable[_2434.StraightBevelGearMeshCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.StraightBevelGearMeshCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2434.StraightBevelGearMeshCompoundSystemDeflection))

    def results_for_worm_gear_mesh(self, design_entity: '_1868.WormGearMesh') -> 'Iterable[_2449.WormGearMeshCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.WormGearMeshCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2449.WormGearMeshCompoundSystemDeflection))

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1870.ZerolBevelGearMesh') -> 'Iterable[_2452.ZerolBevelGearMeshCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.ZerolBevelGearMeshCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2452.ZerolBevelGearMeshCompoundSystemDeflection))

    def results_for_gear_mesh(self, design_entity: '_1852.GearMesh') -> 'Iterable[_2384.GearMeshCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.GearMeshCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2384.GearMeshCompoundSystemDeflection))

    def results_for_part_to_part_shear_coupling_connection(self, design_entity: '_1878.PartToPartShearCouplingConnection') -> 'Iterable[_2407.PartToPartShearCouplingConnectionCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.PartToPartShearCouplingConnectionCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2407.PartToPartShearCouplingConnectionCompoundSystemDeflection))

    def results_for_clutch_connection(self, design_entity: '_1872.ClutchConnection') -> 'Iterable[_2352.ClutchConnectionCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.ClutchConnectionCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2352.ClutchConnectionCompoundSystemDeflection))

    def results_for_concept_coupling_connection(self, design_entity: '_1874.ConceptCouplingConnection') -> 'Iterable[_2357.ConceptCouplingConnectionCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.ConceptCouplingConnectionCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2357.ConceptCouplingConnectionCompoundSystemDeflection))

    def results_for_coupling_connection(self, design_entity: '_1876.CouplingConnection') -> 'Iterable[_2368.CouplingConnectionCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.CouplingConnectionCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2368.CouplingConnectionCompoundSystemDeflection))

    def results_for_spring_damper_connection(self, design_entity: '_1880.SpringDamperConnection') -> 'Iterable[_2428.SpringDamperConnectionCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.SpringDamperConnectionCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2428.SpringDamperConnectionCompoundSystemDeflection))

    def results_for_torque_converter_connection(self, design_entity: '_1882.TorqueConverterConnection') -> 'Iterable[_2443.TorqueConverterConnectionCompoundSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.system_deflections.compound.TorqueConverterConnectionCompoundSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2443.TorqueConverterConnectionCompoundSystemDeflection))
