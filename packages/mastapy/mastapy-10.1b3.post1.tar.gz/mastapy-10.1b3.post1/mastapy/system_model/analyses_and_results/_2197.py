'''_2197.py

CompoundPowerFlowAnalysis
'''


from typing import Iterable

from mastapy.system_model.part_model import (
    _1978, _1979, _1982, _1984,
    _1985, _1986, _1989, _1990,
    _1993, _1994, _1977, _1995,
    _1998, _2001, _2002, _2003,
    _2005, _2006, _2007, _2009,
    _2010, _2012, _2014, _2015,
    _2016
)
from mastapy.system_model.analyses_and_results.power_flows.compound import (
    _3338, _3339, _3344, _3355,
    _3356, _3362, _3373, _3384,
    _3385, _3389, _3343, _3393,
    _3397, _3408, _3409, _3410,
    _3411, _3412, _3418, _3419,
    _3420, _3425, _3429, _3452,
    _3453, _3426, _3366, _3368,
    _3386, _3388, _3340, _3342,
    _3347, _3349, _3350, _3351,
    _3352, _3354, _3369, _3371,
    _3380, _3382, _3383, _3390,
    _3392, _3394, _3396, _3399,
    _3401, _3402, _3404, _3405,
    _3407, _3417, _3430, _3432,
    _3436, _3438, _3439, _3441,
    _3442, _3443, _3454, _3456,
    _3457, _3459, _3413, _3415,
    _3346, _3358, _3360, _3363,
    _3365, _3374, _3376, _3378,
    _3379, _3421, _3427, _3423,
    _3422, _3433, _3435, _3444,
    _3445, _3446, _3447, _3448,
    _3450, _3451, _3377, _3345,
    _3361, _3372, _3398, _3416,
    _3424, _3428, _3348, _3367,
    _3387, _3437, _3353, _3370,
    _3341, _3381, _3395, _3400,
    _3403, _3406, _3431, _3440,
    _3455, _3458, _3391, _3414,
    _3359, _3364, _3375, _3434,
    _3449
)
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.shaft_model import _2019
from mastapy.system_model.part_model.gears import (
    _2057, _2058, _2064, _2065,
    _2049, _2050, _2051, _2052,
    _2053, _2054, _2055, _2056,
    _2059, _2060, _2061, _2062,
    _2063, _2066, _2068, _2070,
    _2071, _2072, _2073, _2074,
    _2075, _2076, _2077, _2078,
    _2079, _2080, _2081, _2082,
    _2083, _2084, _2085, _2086,
    _2087, _2088, _2089, _2090
)
from mastapy.system_model.part_model.couplings import (
    _2119, _2120, _2108, _2110,
    _2111, _2113, _2114, _2115,
    _2116, _2117, _2118, _2121,
    _2129, _2127, _2128, _2130,
    _2131, _2132, _2134, _2135,
    _2136, _2137, _2138, _2140
)
from mastapy.system_model.connections_and_sockets import (
    _1835, _1830, _1831, _1834,
    _1843, _1846, _1850, _1854
)
from mastapy.system_model.connections_and_sockets.gears import (
    _1860, _1864, _1870, _1884,
    _1862, _1866, _1858, _1868,
    _1874, _1877, _1878, _1879,
    _1882, _1886, _1888, _1890,
    _1872
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _1898, _1892, _1894, _1896,
    _1900, _1902
)
from mastapy.system_model.analyses_and_results import _2149
from mastapy._internal.python_net import python_net_import

_COMPOUND_POWER_FLOW_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundPowerFlowAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundPowerFlowAnalysis',)


class CompoundPowerFlowAnalysis(_2149.CompoundAnalysis):
    '''CompoundPowerFlowAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_POWER_FLOW_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundPowerFlowAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    def results_for_abstract_assembly(self, design_entity: '_1978.AbstractAssembly') -> 'Iterable[_3338.AbstractAssemblyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.AbstractAssemblyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3338.AbstractAssemblyCompoundPowerFlow))

    def results_for_abstract_shaft_or_housing(self, design_entity: '_1979.AbstractShaftOrHousing') -> 'Iterable[_3339.AbstractShaftOrHousingCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.AbstractShaftOrHousingCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3339.AbstractShaftOrHousingCompoundPowerFlow))

    def results_for_bearing(self, design_entity: '_1982.Bearing') -> 'Iterable[_3344.BearingCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BearingCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3344.BearingCompoundPowerFlow))

    def results_for_bolt(self, design_entity: '_1984.Bolt') -> 'Iterable[_3355.BoltCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BoltCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3355.BoltCompoundPowerFlow))

    def results_for_bolted_joint(self, design_entity: '_1985.BoltedJoint') -> 'Iterable[_3356.BoltedJointCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BoltedJointCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3356.BoltedJointCompoundPowerFlow))

    def results_for_component(self, design_entity: '_1986.Component') -> 'Iterable[_3362.ComponentCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ComponentCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3362.ComponentCompoundPowerFlow))

    def results_for_connector(self, design_entity: '_1989.Connector') -> 'Iterable[_3373.ConnectorCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConnectorCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3373.ConnectorCompoundPowerFlow))

    def results_for_datum(self, design_entity: '_1990.Datum') -> 'Iterable[_3384.DatumCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.DatumCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3384.DatumCompoundPowerFlow))

    def results_for_external_cad_model(self, design_entity: '_1993.ExternalCADModel') -> 'Iterable[_3385.ExternalCADModelCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ExternalCADModelCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3385.ExternalCADModelCompoundPowerFlow))

    def results_for_flexible_pin_assembly(self, design_entity: '_1994.FlexiblePinAssembly') -> 'Iterable[_3389.FlexiblePinAssemblyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.FlexiblePinAssemblyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3389.FlexiblePinAssemblyCompoundPowerFlow))

    def results_for_assembly(self, design_entity: '_1977.Assembly') -> 'Iterable[_3343.AssemblyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.AssemblyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3343.AssemblyCompoundPowerFlow))

    def results_for_guide_dxf_model(self, design_entity: '_1995.GuideDxfModel') -> 'Iterable[_3393.GuideDxfModelCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.GuideDxfModelCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3393.GuideDxfModelCompoundPowerFlow))

    def results_for_imported_fe_component(self, design_entity: '_1998.ImportedFEComponent') -> 'Iterable[_3397.ImportedFEComponentCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ImportedFEComponentCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3397.ImportedFEComponentCompoundPowerFlow))

    def results_for_mass_disc(self, design_entity: '_2001.MassDisc') -> 'Iterable[_3408.MassDiscCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.MassDiscCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3408.MassDiscCompoundPowerFlow))

    def results_for_measurement_component(self, design_entity: '_2002.MeasurementComponent') -> 'Iterable[_3409.MeasurementComponentCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.MeasurementComponentCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3409.MeasurementComponentCompoundPowerFlow))

    def results_for_mountable_component(self, design_entity: '_2003.MountableComponent') -> 'Iterable[_3410.MountableComponentCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.MountableComponentCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3410.MountableComponentCompoundPowerFlow))

    def results_for_oil_seal(self, design_entity: '_2005.OilSeal') -> 'Iterable[_3411.OilSealCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.OilSealCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3411.OilSealCompoundPowerFlow))

    def results_for_part(self, design_entity: '_2006.Part') -> 'Iterable[_3412.PartCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PartCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3412.PartCompoundPowerFlow))

    def results_for_planet_carrier(self, design_entity: '_2007.PlanetCarrier') -> 'Iterable[_3418.PlanetCarrierCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PlanetCarrierCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3418.PlanetCarrierCompoundPowerFlow))

    def results_for_point_load(self, design_entity: '_2009.PointLoad') -> 'Iterable[_3419.PointLoadCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PointLoadCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3419.PointLoadCompoundPowerFlow))

    def results_for_power_load(self, design_entity: '_2010.PowerLoad') -> 'Iterable[_3420.PowerLoadCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PowerLoadCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3420.PowerLoadCompoundPowerFlow))

    def results_for_root_assembly(self, design_entity: '_2012.RootAssembly') -> 'Iterable[_3425.RootAssemblyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.RootAssemblyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3425.RootAssemblyCompoundPowerFlow))

    def results_for_specialised_assembly(self, design_entity: '_2014.SpecialisedAssembly') -> 'Iterable[_3429.SpecialisedAssemblyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SpecialisedAssemblyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3429.SpecialisedAssemblyCompoundPowerFlow))

    def results_for_unbalanced_mass(self, design_entity: '_2015.UnbalancedMass') -> 'Iterable[_3452.UnbalancedMassCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.UnbalancedMassCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3452.UnbalancedMassCompoundPowerFlow))

    def results_for_virtual_component(self, design_entity: '_2016.VirtualComponent') -> 'Iterable[_3453.VirtualComponentCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.VirtualComponentCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3453.VirtualComponentCompoundPowerFlow))

    def results_for_shaft(self, design_entity: '_2019.Shaft') -> 'Iterable[_3426.ShaftCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ShaftCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3426.ShaftCompoundPowerFlow))

    def results_for_concept_gear(self, design_entity: '_2057.ConceptGear') -> 'Iterable[_3366.ConceptGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConceptGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3366.ConceptGearCompoundPowerFlow))

    def results_for_concept_gear_set(self, design_entity: '_2058.ConceptGearSet') -> 'Iterable[_3368.ConceptGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConceptGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3368.ConceptGearSetCompoundPowerFlow))

    def results_for_face_gear(self, design_entity: '_2064.FaceGear') -> 'Iterable[_3386.FaceGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.FaceGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3386.FaceGearCompoundPowerFlow))

    def results_for_face_gear_set(self, design_entity: '_2065.FaceGearSet') -> 'Iterable[_3388.FaceGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.FaceGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3388.FaceGearSetCompoundPowerFlow))

    def results_for_agma_gleason_conical_gear(self, design_entity: '_2049.AGMAGleasonConicalGear') -> 'Iterable[_3340.AGMAGleasonConicalGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.AGMAGleasonConicalGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3340.AGMAGleasonConicalGearCompoundPowerFlow))

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_2050.AGMAGleasonConicalGearSet') -> 'Iterable[_3342.AGMAGleasonConicalGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.AGMAGleasonConicalGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3342.AGMAGleasonConicalGearSetCompoundPowerFlow))

    def results_for_bevel_differential_gear(self, design_entity: '_2051.BevelDifferentialGear') -> 'Iterable[_3347.BevelDifferentialGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelDifferentialGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3347.BevelDifferentialGearCompoundPowerFlow))

    def results_for_bevel_differential_gear_set(self, design_entity: '_2052.BevelDifferentialGearSet') -> 'Iterable[_3349.BevelDifferentialGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelDifferentialGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3349.BevelDifferentialGearSetCompoundPowerFlow))

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2053.BevelDifferentialPlanetGear') -> 'Iterable[_3350.BevelDifferentialPlanetGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelDifferentialPlanetGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3350.BevelDifferentialPlanetGearCompoundPowerFlow))

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2054.BevelDifferentialSunGear') -> 'Iterable[_3351.BevelDifferentialSunGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelDifferentialSunGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3351.BevelDifferentialSunGearCompoundPowerFlow))

    def results_for_bevel_gear(self, design_entity: '_2055.BevelGear') -> 'Iterable[_3352.BevelGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3352.BevelGearCompoundPowerFlow))

    def results_for_bevel_gear_set(self, design_entity: '_2056.BevelGearSet') -> 'Iterable[_3354.BevelGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3354.BevelGearSetCompoundPowerFlow))

    def results_for_conical_gear(self, design_entity: '_2059.ConicalGear') -> 'Iterable[_3369.ConicalGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConicalGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3369.ConicalGearCompoundPowerFlow))

    def results_for_conical_gear_set(self, design_entity: '_2060.ConicalGearSet') -> 'Iterable[_3371.ConicalGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConicalGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3371.ConicalGearSetCompoundPowerFlow))

    def results_for_cylindrical_gear(self, design_entity: '_2061.CylindricalGear') -> 'Iterable[_3380.CylindricalGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CylindricalGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3380.CylindricalGearCompoundPowerFlow))

    def results_for_cylindrical_gear_set(self, design_entity: '_2062.CylindricalGearSet') -> 'Iterable[_3382.CylindricalGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CylindricalGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3382.CylindricalGearSetCompoundPowerFlow))

    def results_for_cylindrical_planet_gear(self, design_entity: '_2063.CylindricalPlanetGear') -> 'Iterable[_3383.CylindricalPlanetGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CylindricalPlanetGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3383.CylindricalPlanetGearCompoundPowerFlow))

    def results_for_gear(self, design_entity: '_2066.Gear') -> 'Iterable[_3390.GearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.GearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3390.GearCompoundPowerFlow))

    def results_for_gear_set(self, design_entity: '_2068.GearSet') -> 'Iterable[_3392.GearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.GearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3392.GearSetCompoundPowerFlow))

    def results_for_hypoid_gear(self, design_entity: '_2070.HypoidGear') -> 'Iterable[_3394.HypoidGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.HypoidGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3394.HypoidGearCompoundPowerFlow))

    def results_for_hypoid_gear_set(self, design_entity: '_2071.HypoidGearSet') -> 'Iterable[_3396.HypoidGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.HypoidGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3396.HypoidGearSetCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2072.KlingelnbergCycloPalloidConicalGear') -> 'Iterable[_3399.KlingelnbergCycloPalloidConicalGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidConicalGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3399.KlingelnbergCycloPalloidConicalGearCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2073.KlingelnbergCycloPalloidConicalGearSet') -> 'Iterable[_3401.KlingelnbergCycloPalloidConicalGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidConicalGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3401.KlingelnbergCycloPalloidConicalGearSetCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2074.KlingelnbergCycloPalloidHypoidGear') -> 'Iterable[_3402.KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3402.KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2075.KlingelnbergCycloPalloidHypoidGearSet') -> 'Iterable[_3404.KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3404.KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2076.KlingelnbergCycloPalloidSpiralBevelGear') -> 'Iterable[_3405.KlingelnbergCycloPalloidSpiralBevelGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidSpiralBevelGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3405.KlingelnbergCycloPalloidSpiralBevelGearCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2077.KlingelnbergCycloPalloidSpiralBevelGearSet') -> 'Iterable[_3407.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3407.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow))

    def results_for_planetary_gear_set(self, design_entity: '_2078.PlanetaryGearSet') -> 'Iterable[_3417.PlanetaryGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PlanetaryGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3417.PlanetaryGearSetCompoundPowerFlow))

    def results_for_spiral_bevel_gear(self, design_entity: '_2079.SpiralBevelGear') -> 'Iterable[_3430.SpiralBevelGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SpiralBevelGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3430.SpiralBevelGearCompoundPowerFlow))

    def results_for_spiral_bevel_gear_set(self, design_entity: '_2080.SpiralBevelGearSet') -> 'Iterable[_3432.SpiralBevelGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SpiralBevelGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3432.SpiralBevelGearSetCompoundPowerFlow))

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2081.StraightBevelDiffGear') -> 'Iterable[_3436.StraightBevelDiffGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelDiffGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3436.StraightBevelDiffGearCompoundPowerFlow))

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_2082.StraightBevelDiffGearSet') -> 'Iterable[_3438.StraightBevelDiffGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelDiffGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3438.StraightBevelDiffGearSetCompoundPowerFlow))

    def results_for_straight_bevel_gear(self, design_entity: '_2083.StraightBevelGear') -> 'Iterable[_3439.StraightBevelGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3439.StraightBevelGearCompoundPowerFlow))

    def results_for_straight_bevel_gear_set(self, design_entity: '_2084.StraightBevelGearSet') -> 'Iterable[_3441.StraightBevelGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3441.StraightBevelGearSetCompoundPowerFlow))

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2085.StraightBevelPlanetGear') -> 'Iterable[_3442.StraightBevelPlanetGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelPlanetGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3442.StraightBevelPlanetGearCompoundPowerFlow))

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2086.StraightBevelSunGear') -> 'Iterable[_3443.StraightBevelSunGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelSunGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3443.StraightBevelSunGearCompoundPowerFlow))

    def results_for_worm_gear(self, design_entity: '_2087.WormGear') -> 'Iterable[_3454.WormGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.WormGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3454.WormGearCompoundPowerFlow))

    def results_for_worm_gear_set(self, design_entity: '_2088.WormGearSet') -> 'Iterable[_3456.WormGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.WormGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3456.WormGearSetCompoundPowerFlow))

    def results_for_zerol_bevel_gear(self, design_entity: '_2089.ZerolBevelGear') -> 'Iterable[_3457.ZerolBevelGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ZerolBevelGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3457.ZerolBevelGearCompoundPowerFlow))

    def results_for_zerol_bevel_gear_set(self, design_entity: '_2090.ZerolBevelGearSet') -> 'Iterable[_3459.ZerolBevelGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ZerolBevelGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3459.ZerolBevelGearSetCompoundPowerFlow))

    def results_for_part_to_part_shear_coupling(self, design_entity: '_2119.PartToPartShearCoupling') -> 'Iterable[_3413.PartToPartShearCouplingCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PartToPartShearCouplingCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3413.PartToPartShearCouplingCompoundPowerFlow))

    def results_for_part_to_part_shear_coupling_half(self, design_entity: '_2120.PartToPartShearCouplingHalf') -> 'Iterable[_3415.PartToPartShearCouplingHalfCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PartToPartShearCouplingHalfCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3415.PartToPartShearCouplingHalfCompoundPowerFlow))

    def results_for_belt_drive(self, design_entity: '_2108.BeltDrive') -> 'Iterable[_3346.BeltDriveCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BeltDriveCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3346.BeltDriveCompoundPowerFlow))

    def results_for_clutch(self, design_entity: '_2110.Clutch') -> 'Iterable[_3358.ClutchCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ClutchCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3358.ClutchCompoundPowerFlow))

    def results_for_clutch_half(self, design_entity: '_2111.ClutchHalf') -> 'Iterable[_3360.ClutchHalfCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ClutchHalfCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3360.ClutchHalfCompoundPowerFlow))

    def results_for_concept_coupling(self, design_entity: '_2113.ConceptCoupling') -> 'Iterable[_3363.ConceptCouplingCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConceptCouplingCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3363.ConceptCouplingCompoundPowerFlow))

    def results_for_concept_coupling_half(self, design_entity: '_2114.ConceptCouplingHalf') -> 'Iterable[_3365.ConceptCouplingHalfCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConceptCouplingHalfCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3365.ConceptCouplingHalfCompoundPowerFlow))

    def results_for_coupling(self, design_entity: '_2115.Coupling') -> 'Iterable[_3374.CouplingCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CouplingCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3374.CouplingCompoundPowerFlow))

    def results_for_coupling_half(self, design_entity: '_2116.CouplingHalf') -> 'Iterable[_3376.CouplingHalfCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CouplingHalfCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3376.CouplingHalfCompoundPowerFlow))

    def results_for_cvt(self, design_entity: '_2117.CVT') -> 'Iterable[_3378.CVTCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CVTCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3378.CVTCompoundPowerFlow))

    def results_for_cvt_pulley(self, design_entity: '_2118.CVTPulley') -> 'Iterable[_3379.CVTPulleyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CVTPulleyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3379.CVTPulleyCompoundPowerFlow))

    def results_for_pulley(self, design_entity: '_2121.Pulley') -> 'Iterable[_3421.PulleyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PulleyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3421.PulleyCompoundPowerFlow))

    def results_for_shaft_hub_connection(self, design_entity: '_2129.ShaftHubConnection') -> 'Iterable[_3427.ShaftHubConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ShaftHubConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3427.ShaftHubConnectionCompoundPowerFlow))

    def results_for_rolling_ring(self, design_entity: '_2127.RollingRing') -> 'Iterable[_3423.RollingRingCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.RollingRingCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3423.RollingRingCompoundPowerFlow))

    def results_for_rolling_ring_assembly(self, design_entity: '_2128.RollingRingAssembly') -> 'Iterable[_3422.RollingRingAssemblyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.RollingRingAssemblyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3422.RollingRingAssemblyCompoundPowerFlow))

    def results_for_spring_damper(self, design_entity: '_2130.SpringDamper') -> 'Iterable[_3433.SpringDamperCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SpringDamperCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3433.SpringDamperCompoundPowerFlow))

    def results_for_spring_damper_half(self, design_entity: '_2131.SpringDamperHalf') -> 'Iterable[_3435.SpringDamperHalfCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SpringDamperHalfCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3435.SpringDamperHalfCompoundPowerFlow))

    def results_for_synchroniser(self, design_entity: '_2132.Synchroniser') -> 'Iterable[_3444.SynchroniserCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SynchroniserCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3444.SynchroniserCompoundPowerFlow))

    def results_for_synchroniser_half(self, design_entity: '_2134.SynchroniserHalf') -> 'Iterable[_3445.SynchroniserHalfCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SynchroniserHalfCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3445.SynchroniserHalfCompoundPowerFlow))

    def results_for_synchroniser_part(self, design_entity: '_2135.SynchroniserPart') -> 'Iterable[_3446.SynchroniserPartCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SynchroniserPartCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3446.SynchroniserPartCompoundPowerFlow))

    def results_for_synchroniser_sleeve(self, design_entity: '_2136.SynchroniserSleeve') -> 'Iterable[_3447.SynchroniserSleeveCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SynchroniserSleeveCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3447.SynchroniserSleeveCompoundPowerFlow))

    def results_for_torque_converter(self, design_entity: '_2137.TorqueConverter') -> 'Iterable[_3448.TorqueConverterCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.TorqueConverterCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3448.TorqueConverterCompoundPowerFlow))

    def results_for_torque_converter_pump(self, design_entity: '_2138.TorqueConverterPump') -> 'Iterable[_3450.TorqueConverterPumpCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.TorqueConverterPumpCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3450.TorqueConverterPumpCompoundPowerFlow))

    def results_for_torque_converter_turbine(self, design_entity: '_2140.TorqueConverterTurbine') -> 'Iterable[_3451.TorqueConverterTurbineCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.TorqueConverterTurbineCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3451.TorqueConverterTurbineCompoundPowerFlow))

    def results_for_cvt_belt_connection(self, design_entity: '_1835.CVTBeltConnection') -> 'Iterable[_3377.CVTBeltConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CVTBeltConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3377.CVTBeltConnectionCompoundPowerFlow))

    def results_for_belt_connection(self, design_entity: '_1830.BeltConnection') -> 'Iterable[_3345.BeltConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BeltConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3345.BeltConnectionCompoundPowerFlow))

    def results_for_coaxial_connection(self, design_entity: '_1831.CoaxialConnection') -> 'Iterable[_3361.CoaxialConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CoaxialConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3361.CoaxialConnectionCompoundPowerFlow))

    def results_for_connection(self, design_entity: '_1834.Connection') -> 'Iterable[_3372.ConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3372.ConnectionCompoundPowerFlow))

    def results_for_inter_mountable_component_connection(self, design_entity: '_1843.InterMountableComponentConnection') -> 'Iterable[_3398.InterMountableComponentConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.InterMountableComponentConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3398.InterMountableComponentConnectionCompoundPowerFlow))

    def results_for_planetary_connection(self, design_entity: '_1846.PlanetaryConnection') -> 'Iterable[_3416.PlanetaryConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PlanetaryConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3416.PlanetaryConnectionCompoundPowerFlow))

    def results_for_rolling_ring_connection(self, design_entity: '_1850.RollingRingConnection') -> 'Iterable[_3424.RollingRingConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.RollingRingConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3424.RollingRingConnectionCompoundPowerFlow))

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1854.ShaftToMountableComponentConnection') -> 'Iterable[_3428.ShaftToMountableComponentConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ShaftToMountableComponentConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3428.ShaftToMountableComponentConnectionCompoundPowerFlow))

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1860.BevelDifferentialGearMesh') -> 'Iterable[_3348.BevelDifferentialGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelDifferentialGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3348.BevelDifferentialGearMeshCompoundPowerFlow))

    def results_for_concept_gear_mesh(self, design_entity: '_1864.ConceptGearMesh') -> 'Iterable[_3367.ConceptGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConceptGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3367.ConceptGearMeshCompoundPowerFlow))

    def results_for_face_gear_mesh(self, design_entity: '_1870.FaceGearMesh') -> 'Iterable[_3387.FaceGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.FaceGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3387.FaceGearMeshCompoundPowerFlow))

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1884.StraightBevelDiffGearMesh') -> 'Iterable[_3437.StraightBevelDiffGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelDiffGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3437.StraightBevelDiffGearMeshCompoundPowerFlow))

    def results_for_bevel_gear_mesh(self, design_entity: '_1862.BevelGearMesh') -> 'Iterable[_3353.BevelGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3353.BevelGearMeshCompoundPowerFlow))

    def results_for_conical_gear_mesh(self, design_entity: '_1866.ConicalGearMesh') -> 'Iterable[_3370.ConicalGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConicalGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3370.ConicalGearMeshCompoundPowerFlow))

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1858.AGMAGleasonConicalGearMesh') -> 'Iterable[_3341.AGMAGleasonConicalGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.AGMAGleasonConicalGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3341.AGMAGleasonConicalGearMeshCompoundPowerFlow))

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1868.CylindricalGearMesh') -> 'Iterable[_3381.CylindricalGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CylindricalGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3381.CylindricalGearMeshCompoundPowerFlow))

    def results_for_hypoid_gear_mesh(self, design_entity: '_1874.HypoidGearMesh') -> 'Iterable[_3395.HypoidGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.HypoidGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3395.HypoidGearMeshCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1877.KlingelnbergCycloPalloidConicalGearMesh') -> 'Iterable[_3400.KlingelnbergCycloPalloidConicalGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidConicalGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3400.KlingelnbergCycloPalloidConicalGearMeshCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1878.KlingelnbergCycloPalloidHypoidGearMesh') -> 'Iterable[_3403.KlingelnbergCycloPalloidHypoidGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidHypoidGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3403.KlingelnbergCycloPalloidHypoidGearMeshCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1879.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> 'Iterable[_3406.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3406.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow))

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1882.SpiralBevelGearMesh') -> 'Iterable[_3431.SpiralBevelGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SpiralBevelGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3431.SpiralBevelGearMeshCompoundPowerFlow))

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1886.StraightBevelGearMesh') -> 'Iterable[_3440.StraightBevelGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3440.StraightBevelGearMeshCompoundPowerFlow))

    def results_for_worm_gear_mesh(self, design_entity: '_1888.WormGearMesh') -> 'Iterable[_3455.WormGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.WormGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3455.WormGearMeshCompoundPowerFlow))

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1890.ZerolBevelGearMesh') -> 'Iterable[_3458.ZerolBevelGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ZerolBevelGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3458.ZerolBevelGearMeshCompoundPowerFlow))

    def results_for_gear_mesh(self, design_entity: '_1872.GearMesh') -> 'Iterable[_3391.GearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.GearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3391.GearMeshCompoundPowerFlow))

    def results_for_part_to_part_shear_coupling_connection(self, design_entity: '_1898.PartToPartShearCouplingConnection') -> 'Iterable[_3414.PartToPartShearCouplingConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PartToPartShearCouplingConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3414.PartToPartShearCouplingConnectionCompoundPowerFlow))

    def results_for_clutch_connection(self, design_entity: '_1892.ClutchConnection') -> 'Iterable[_3359.ClutchConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ClutchConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3359.ClutchConnectionCompoundPowerFlow))

    def results_for_concept_coupling_connection(self, design_entity: '_1894.ConceptCouplingConnection') -> 'Iterable[_3364.ConceptCouplingConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConceptCouplingConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3364.ConceptCouplingConnectionCompoundPowerFlow))

    def results_for_coupling_connection(self, design_entity: '_1896.CouplingConnection') -> 'Iterable[_3375.CouplingConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CouplingConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3375.CouplingConnectionCompoundPowerFlow))

    def results_for_spring_damper_connection(self, design_entity: '_1900.SpringDamperConnection') -> 'Iterable[_3434.SpringDamperConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SpringDamperConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3434.SpringDamperConnectionCompoundPowerFlow))

    def results_for_torque_converter_connection(self, design_entity: '_1902.TorqueConverterConnection') -> 'Iterable[_3449.TorqueConverterConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.TorqueConverterConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3449.TorqueConverterConnectionCompoundPowerFlow))
