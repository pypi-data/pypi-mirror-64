'''_2169.py

CompoundGearWhineAnalysisAnalysis
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
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import (
    _5642, _5643, _5648, _5659,
    _5660, _5665, _5676, _5687,
    _5688, _5692, _5647, _5696,
    _5700, _5711, _5712, _5713,
    _5714, _5715, _5721, _5722,
    _5723, _5728, _5732, _5755,
    _5756, _5729, _5669, _5671,
    _5689, _5691, _5644, _5646,
    _5651, _5653, _5654, _5655,
    _5656, _5658, _5672, _5674,
    _5683, _5685, _5686, _5693,
    _5695, _5697, _5699, _5702,
    _5704, _5705, _5707, _5708,
    _5710, _5720, _5733, _5735,
    _5739, _5741, _5742, _5744,
    _5745, _5746, _5757, _5759,
    _5760, _5762, _5716, _5718,
    _5650, _5661, _5663, _5666,
    _5668, _5677, _5679, _5681,
    _5682, _5724, _5730, _5726,
    _5725, _5736, _5738, _5747,
    _5748, _5749, _5750, _5751,
    _5753, _5754, _5680, _5649,
    _5664, _5675, _5701, _5719,
    _5727, _5731, _5652, _5670,
    _5690, _5740, _5657, _5673,
    _5645, _5684, _5698, _5703,
    _5706, _5709, _5734, _5743,
    _5758, _5761, _5694, _5717,
    _5662, _5667, _5678, _5737,
    _5752
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

_COMPOUND_GEAR_WHINE_ANALYSIS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundGearWhineAnalysisAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundGearWhineAnalysisAnalysis',)


class CompoundGearWhineAnalysisAnalysis(_2129.CompoundAnalysis):
    '''CompoundGearWhineAnalysisAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_GEAR_WHINE_ANALYSIS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundGearWhineAnalysisAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    def results_for_abstract_assembly(self, design_entity: '_1958.AbstractAssembly') -> 'Iterable[_5642.AbstractAssemblyCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.AbstractAssemblyCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5642.AbstractAssemblyCompoundGearWhineAnalysis))

    def results_for_abstract_shaft_or_housing(self, design_entity: '_1959.AbstractShaftOrHousing') -> 'Iterable[_5643.AbstractShaftOrHousingCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.AbstractShaftOrHousingCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5643.AbstractShaftOrHousingCompoundGearWhineAnalysis))

    def results_for_bearing(self, design_entity: '_1962.Bearing') -> 'Iterable[_5648.BearingCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.BearingCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5648.BearingCompoundGearWhineAnalysis))

    def results_for_bolt(self, design_entity: '_1964.Bolt') -> 'Iterable[_5659.BoltCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.BoltCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5659.BoltCompoundGearWhineAnalysis))

    def results_for_bolted_joint(self, design_entity: '_1965.BoltedJoint') -> 'Iterable[_5660.BoltedJointCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.BoltedJointCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5660.BoltedJointCompoundGearWhineAnalysis))

    def results_for_component(self, design_entity: '_1966.Component') -> 'Iterable[_5665.ComponentCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ComponentCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5665.ComponentCompoundGearWhineAnalysis))

    def results_for_connector(self, design_entity: '_1969.Connector') -> 'Iterable[_5676.ConnectorCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ConnectorCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5676.ConnectorCompoundGearWhineAnalysis))

    def results_for_datum(self, design_entity: '_1970.Datum') -> 'Iterable[_5687.DatumCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.DatumCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5687.DatumCompoundGearWhineAnalysis))

    def results_for_external_cad_model(self, design_entity: '_1973.ExternalCADModel') -> 'Iterable[_5688.ExternalCADModelCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ExternalCADModelCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5688.ExternalCADModelCompoundGearWhineAnalysis))

    def results_for_flexible_pin_assembly(self, design_entity: '_1974.FlexiblePinAssembly') -> 'Iterable[_5692.FlexiblePinAssemblyCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.FlexiblePinAssemblyCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5692.FlexiblePinAssemblyCompoundGearWhineAnalysis))

    def results_for_assembly(self, design_entity: '_1957.Assembly') -> 'Iterable[_5647.AssemblyCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.AssemblyCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5647.AssemblyCompoundGearWhineAnalysis))

    def results_for_guide_dxf_model(self, design_entity: '_1975.GuideDxfModel') -> 'Iterable[_5696.GuideDxfModelCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.GuideDxfModelCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5696.GuideDxfModelCompoundGearWhineAnalysis))

    def results_for_imported_fe_component(self, design_entity: '_1978.ImportedFEComponent') -> 'Iterable[_5700.ImportedFEComponentCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ImportedFEComponentCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5700.ImportedFEComponentCompoundGearWhineAnalysis))

    def results_for_mass_disc(self, design_entity: '_1981.MassDisc') -> 'Iterable[_5711.MassDiscCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.MassDiscCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5711.MassDiscCompoundGearWhineAnalysis))

    def results_for_measurement_component(self, design_entity: '_1982.MeasurementComponent') -> 'Iterable[_5712.MeasurementComponentCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.MeasurementComponentCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5712.MeasurementComponentCompoundGearWhineAnalysis))

    def results_for_mountable_component(self, design_entity: '_1983.MountableComponent') -> 'Iterable[_5713.MountableComponentCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.MountableComponentCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5713.MountableComponentCompoundGearWhineAnalysis))

    def results_for_oil_seal(self, design_entity: '_1985.OilSeal') -> 'Iterable[_5714.OilSealCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.OilSealCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5714.OilSealCompoundGearWhineAnalysis))

    def results_for_part(self, design_entity: '_1986.Part') -> 'Iterable[_5715.PartCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.PartCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5715.PartCompoundGearWhineAnalysis))

    def results_for_planet_carrier(self, design_entity: '_1987.PlanetCarrier') -> 'Iterable[_5721.PlanetCarrierCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.PlanetCarrierCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5721.PlanetCarrierCompoundGearWhineAnalysis))

    def results_for_point_load(self, design_entity: '_1989.PointLoad') -> 'Iterable[_5722.PointLoadCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.PointLoadCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5722.PointLoadCompoundGearWhineAnalysis))

    def results_for_power_load(self, design_entity: '_1990.PowerLoad') -> 'Iterable[_5723.PowerLoadCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.PowerLoadCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5723.PowerLoadCompoundGearWhineAnalysis))

    def results_for_root_assembly(self, design_entity: '_1992.RootAssembly') -> 'Iterable[_5728.RootAssemblyCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.RootAssemblyCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5728.RootAssemblyCompoundGearWhineAnalysis))

    def results_for_specialised_assembly(self, design_entity: '_1994.SpecialisedAssembly') -> 'Iterable[_5732.SpecialisedAssemblyCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.SpecialisedAssemblyCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5732.SpecialisedAssemblyCompoundGearWhineAnalysis))

    def results_for_unbalanced_mass(self, design_entity: '_1995.UnbalancedMass') -> 'Iterable[_5755.UnbalancedMassCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.UnbalancedMassCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5755.UnbalancedMassCompoundGearWhineAnalysis))

    def results_for_virtual_component(self, design_entity: '_1996.VirtualComponent') -> 'Iterable[_5756.VirtualComponentCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.VirtualComponentCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5756.VirtualComponentCompoundGearWhineAnalysis))

    def results_for_shaft(self, design_entity: '_1999.Shaft') -> 'Iterable[_5729.ShaftCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ShaftCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5729.ShaftCompoundGearWhineAnalysis))

    def results_for_concept_gear(self, design_entity: '_2037.ConceptGear') -> 'Iterable[_5669.ConceptGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ConceptGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5669.ConceptGearCompoundGearWhineAnalysis))

    def results_for_concept_gear_set(self, design_entity: '_2038.ConceptGearSet') -> 'Iterable[_5671.ConceptGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ConceptGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5671.ConceptGearSetCompoundGearWhineAnalysis))

    def results_for_face_gear(self, design_entity: '_2044.FaceGear') -> 'Iterable[_5689.FaceGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.FaceGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5689.FaceGearCompoundGearWhineAnalysis))

    def results_for_face_gear_set(self, design_entity: '_2045.FaceGearSet') -> 'Iterable[_5691.FaceGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.FaceGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5691.FaceGearSetCompoundGearWhineAnalysis))

    def results_for_agma_gleason_conical_gear(self, design_entity: '_2029.AGMAGleasonConicalGear') -> 'Iterable[_5644.AGMAGleasonConicalGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.AGMAGleasonConicalGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5644.AGMAGleasonConicalGearCompoundGearWhineAnalysis))

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_2030.AGMAGleasonConicalGearSet') -> 'Iterable[_5646.AGMAGleasonConicalGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.AGMAGleasonConicalGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5646.AGMAGleasonConicalGearSetCompoundGearWhineAnalysis))

    def results_for_bevel_differential_gear(self, design_entity: '_2031.BevelDifferentialGear') -> 'Iterable[_5651.BevelDifferentialGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.BevelDifferentialGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5651.BevelDifferentialGearCompoundGearWhineAnalysis))

    def results_for_bevel_differential_gear_set(self, design_entity: '_2032.BevelDifferentialGearSet') -> 'Iterable[_5653.BevelDifferentialGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.BevelDifferentialGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5653.BevelDifferentialGearSetCompoundGearWhineAnalysis))

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2033.BevelDifferentialPlanetGear') -> 'Iterable[_5654.BevelDifferentialPlanetGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.BevelDifferentialPlanetGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5654.BevelDifferentialPlanetGearCompoundGearWhineAnalysis))

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2034.BevelDifferentialSunGear') -> 'Iterable[_5655.BevelDifferentialSunGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.BevelDifferentialSunGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5655.BevelDifferentialSunGearCompoundGearWhineAnalysis))

    def results_for_bevel_gear(self, design_entity: '_2035.BevelGear') -> 'Iterable[_5656.BevelGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.BevelGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5656.BevelGearCompoundGearWhineAnalysis))

    def results_for_bevel_gear_set(self, design_entity: '_2036.BevelGearSet') -> 'Iterable[_5658.BevelGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.BevelGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5658.BevelGearSetCompoundGearWhineAnalysis))

    def results_for_conical_gear(self, design_entity: '_2039.ConicalGear') -> 'Iterable[_5672.ConicalGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ConicalGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5672.ConicalGearCompoundGearWhineAnalysis))

    def results_for_conical_gear_set(self, design_entity: '_2040.ConicalGearSet') -> 'Iterable[_5674.ConicalGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ConicalGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5674.ConicalGearSetCompoundGearWhineAnalysis))

    def results_for_cylindrical_gear(self, design_entity: '_2041.CylindricalGear') -> 'Iterable[_5683.CylindricalGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.CylindricalGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5683.CylindricalGearCompoundGearWhineAnalysis))

    def results_for_cylindrical_gear_set(self, design_entity: '_2042.CylindricalGearSet') -> 'Iterable[_5685.CylindricalGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.CylindricalGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5685.CylindricalGearSetCompoundGearWhineAnalysis))

    def results_for_cylindrical_planet_gear(self, design_entity: '_2043.CylindricalPlanetGear') -> 'Iterable[_5686.CylindricalPlanetGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.CylindricalPlanetGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5686.CylindricalPlanetGearCompoundGearWhineAnalysis))

    def results_for_gear(self, design_entity: '_2046.Gear') -> 'Iterable[_5693.GearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.GearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5693.GearCompoundGearWhineAnalysis))

    def results_for_gear_set(self, design_entity: '_2048.GearSet') -> 'Iterable[_5695.GearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.GearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5695.GearSetCompoundGearWhineAnalysis))

    def results_for_hypoid_gear(self, design_entity: '_2050.HypoidGear') -> 'Iterable[_5697.HypoidGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.HypoidGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5697.HypoidGearCompoundGearWhineAnalysis))

    def results_for_hypoid_gear_set(self, design_entity: '_2051.HypoidGearSet') -> 'Iterable[_5699.HypoidGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.HypoidGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5699.HypoidGearSetCompoundGearWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2052.KlingelnbergCycloPalloidConicalGear') -> 'Iterable[_5702.KlingelnbergCycloPalloidConicalGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.KlingelnbergCycloPalloidConicalGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5702.KlingelnbergCycloPalloidConicalGearCompoundGearWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2053.KlingelnbergCycloPalloidConicalGearSet') -> 'Iterable[_5704.KlingelnbergCycloPalloidConicalGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.KlingelnbergCycloPalloidConicalGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5704.KlingelnbergCycloPalloidConicalGearSetCompoundGearWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2054.KlingelnbergCycloPalloidHypoidGear') -> 'Iterable[_5705.KlingelnbergCycloPalloidHypoidGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.KlingelnbergCycloPalloidHypoidGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5705.KlingelnbergCycloPalloidHypoidGearCompoundGearWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2055.KlingelnbergCycloPalloidHypoidGearSet') -> 'Iterable[_5707.KlingelnbergCycloPalloidHypoidGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.KlingelnbergCycloPalloidHypoidGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5707.KlingelnbergCycloPalloidHypoidGearSetCompoundGearWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2056.KlingelnbergCycloPalloidSpiralBevelGear') -> 'Iterable[_5708.KlingelnbergCycloPalloidSpiralBevelGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5708.KlingelnbergCycloPalloidSpiralBevelGearCompoundGearWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2057.KlingelnbergCycloPalloidSpiralBevelGearSet') -> 'Iterable[_5710.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5710.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundGearWhineAnalysis))

    def results_for_planetary_gear_set(self, design_entity: '_2058.PlanetaryGearSet') -> 'Iterable[_5720.PlanetaryGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.PlanetaryGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5720.PlanetaryGearSetCompoundGearWhineAnalysis))

    def results_for_spiral_bevel_gear(self, design_entity: '_2059.SpiralBevelGear') -> 'Iterable[_5733.SpiralBevelGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.SpiralBevelGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5733.SpiralBevelGearCompoundGearWhineAnalysis))

    def results_for_spiral_bevel_gear_set(self, design_entity: '_2060.SpiralBevelGearSet') -> 'Iterable[_5735.SpiralBevelGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.SpiralBevelGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5735.SpiralBevelGearSetCompoundGearWhineAnalysis))

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2061.StraightBevelDiffGear') -> 'Iterable[_5739.StraightBevelDiffGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.StraightBevelDiffGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5739.StraightBevelDiffGearCompoundGearWhineAnalysis))

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_2062.StraightBevelDiffGearSet') -> 'Iterable[_5741.StraightBevelDiffGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.StraightBevelDiffGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5741.StraightBevelDiffGearSetCompoundGearWhineAnalysis))

    def results_for_straight_bevel_gear(self, design_entity: '_2063.StraightBevelGear') -> 'Iterable[_5742.StraightBevelGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.StraightBevelGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5742.StraightBevelGearCompoundGearWhineAnalysis))

    def results_for_straight_bevel_gear_set(self, design_entity: '_2064.StraightBevelGearSet') -> 'Iterable[_5744.StraightBevelGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.StraightBevelGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5744.StraightBevelGearSetCompoundGearWhineAnalysis))

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2065.StraightBevelPlanetGear') -> 'Iterable[_5745.StraightBevelPlanetGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.StraightBevelPlanetGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5745.StraightBevelPlanetGearCompoundGearWhineAnalysis))

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2066.StraightBevelSunGear') -> 'Iterable[_5746.StraightBevelSunGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.StraightBevelSunGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5746.StraightBevelSunGearCompoundGearWhineAnalysis))

    def results_for_worm_gear(self, design_entity: '_2067.WormGear') -> 'Iterable[_5757.WormGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.WormGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5757.WormGearCompoundGearWhineAnalysis))

    def results_for_worm_gear_set(self, design_entity: '_2068.WormGearSet') -> 'Iterable[_5759.WormGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.WormGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5759.WormGearSetCompoundGearWhineAnalysis))

    def results_for_zerol_bevel_gear(self, design_entity: '_2069.ZerolBevelGear') -> 'Iterable[_5760.ZerolBevelGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ZerolBevelGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5760.ZerolBevelGearCompoundGearWhineAnalysis))

    def results_for_zerol_bevel_gear_set(self, design_entity: '_2070.ZerolBevelGearSet') -> 'Iterable[_5762.ZerolBevelGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ZerolBevelGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5762.ZerolBevelGearSetCompoundGearWhineAnalysis))

    def results_for_part_to_part_shear_coupling(self, design_entity: '_2099.PartToPartShearCoupling') -> 'Iterable[_5716.PartToPartShearCouplingCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.PartToPartShearCouplingCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5716.PartToPartShearCouplingCompoundGearWhineAnalysis))

    def results_for_part_to_part_shear_coupling_half(self, design_entity: '_2100.PartToPartShearCouplingHalf') -> 'Iterable[_5718.PartToPartShearCouplingHalfCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.PartToPartShearCouplingHalfCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5718.PartToPartShearCouplingHalfCompoundGearWhineAnalysis))

    def results_for_belt_drive(self, design_entity: '_2088.BeltDrive') -> 'Iterable[_5650.BeltDriveCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.BeltDriveCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5650.BeltDriveCompoundGearWhineAnalysis))

    def results_for_clutch(self, design_entity: '_2090.Clutch') -> 'Iterable[_5661.ClutchCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ClutchCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5661.ClutchCompoundGearWhineAnalysis))

    def results_for_clutch_half(self, design_entity: '_2091.ClutchHalf') -> 'Iterable[_5663.ClutchHalfCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ClutchHalfCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5663.ClutchHalfCompoundGearWhineAnalysis))

    def results_for_concept_coupling(self, design_entity: '_2093.ConceptCoupling') -> 'Iterable[_5666.ConceptCouplingCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ConceptCouplingCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5666.ConceptCouplingCompoundGearWhineAnalysis))

    def results_for_concept_coupling_half(self, design_entity: '_2094.ConceptCouplingHalf') -> 'Iterable[_5668.ConceptCouplingHalfCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ConceptCouplingHalfCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5668.ConceptCouplingHalfCompoundGearWhineAnalysis))

    def results_for_coupling(self, design_entity: '_2095.Coupling') -> 'Iterable[_5677.CouplingCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.CouplingCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5677.CouplingCompoundGearWhineAnalysis))

    def results_for_coupling_half(self, design_entity: '_2096.CouplingHalf') -> 'Iterable[_5679.CouplingHalfCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.CouplingHalfCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5679.CouplingHalfCompoundGearWhineAnalysis))

    def results_for_cvt(self, design_entity: '_2097.CVT') -> 'Iterable[_5681.CVTCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.CVTCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5681.CVTCompoundGearWhineAnalysis))

    def results_for_cvt_pulley(self, design_entity: '_2098.CVTPulley') -> 'Iterable[_5682.CVTPulleyCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.CVTPulleyCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5682.CVTPulleyCompoundGearWhineAnalysis))

    def results_for_pulley(self, design_entity: '_2101.Pulley') -> 'Iterable[_5724.PulleyCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.PulleyCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5724.PulleyCompoundGearWhineAnalysis))

    def results_for_shaft_hub_connection(self, design_entity: '_2109.ShaftHubConnection') -> 'Iterable[_5730.ShaftHubConnectionCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ShaftHubConnectionCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5730.ShaftHubConnectionCompoundGearWhineAnalysis))

    def results_for_rolling_ring(self, design_entity: '_2107.RollingRing') -> 'Iterable[_5726.RollingRingCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.RollingRingCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5726.RollingRingCompoundGearWhineAnalysis))

    def results_for_rolling_ring_assembly(self, design_entity: '_2108.RollingRingAssembly') -> 'Iterable[_5725.RollingRingAssemblyCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.RollingRingAssemblyCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5725.RollingRingAssemblyCompoundGearWhineAnalysis))

    def results_for_spring_damper(self, design_entity: '_2110.SpringDamper') -> 'Iterable[_5736.SpringDamperCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.SpringDamperCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5736.SpringDamperCompoundGearWhineAnalysis))

    def results_for_spring_damper_half(self, design_entity: '_2111.SpringDamperHalf') -> 'Iterable[_5738.SpringDamperHalfCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.SpringDamperHalfCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5738.SpringDamperHalfCompoundGearWhineAnalysis))

    def results_for_synchroniser(self, design_entity: '_2112.Synchroniser') -> 'Iterable[_5747.SynchroniserCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.SynchroniserCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5747.SynchroniserCompoundGearWhineAnalysis))

    def results_for_synchroniser_half(self, design_entity: '_2114.SynchroniserHalf') -> 'Iterable[_5748.SynchroniserHalfCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.SynchroniserHalfCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5748.SynchroniserHalfCompoundGearWhineAnalysis))

    def results_for_synchroniser_part(self, design_entity: '_2115.SynchroniserPart') -> 'Iterable[_5749.SynchroniserPartCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.SynchroniserPartCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5749.SynchroniserPartCompoundGearWhineAnalysis))

    def results_for_synchroniser_sleeve(self, design_entity: '_2116.SynchroniserSleeve') -> 'Iterable[_5750.SynchroniserSleeveCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.SynchroniserSleeveCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5750.SynchroniserSleeveCompoundGearWhineAnalysis))

    def results_for_torque_converter(self, design_entity: '_2117.TorqueConverter') -> 'Iterable[_5751.TorqueConverterCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.TorqueConverterCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5751.TorqueConverterCompoundGearWhineAnalysis))

    def results_for_torque_converter_pump(self, design_entity: '_2118.TorqueConverterPump') -> 'Iterable[_5753.TorqueConverterPumpCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.TorqueConverterPumpCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5753.TorqueConverterPumpCompoundGearWhineAnalysis))

    def results_for_torque_converter_turbine(self, design_entity: '_2120.TorqueConverterTurbine') -> 'Iterable[_5754.TorqueConverterTurbineCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.TorqueConverterTurbineCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5754.TorqueConverterTurbineCompoundGearWhineAnalysis))

    def results_for_cvt_belt_connection(self, design_entity: '_1815.CVTBeltConnection') -> 'Iterable[_5680.CVTBeltConnectionCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.CVTBeltConnectionCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5680.CVTBeltConnectionCompoundGearWhineAnalysis))

    def results_for_belt_connection(self, design_entity: '_1810.BeltConnection') -> 'Iterable[_5649.BeltConnectionCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.BeltConnectionCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5649.BeltConnectionCompoundGearWhineAnalysis))

    def results_for_coaxial_connection(self, design_entity: '_1811.CoaxialConnection') -> 'Iterable[_5664.CoaxialConnectionCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.CoaxialConnectionCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5664.CoaxialConnectionCompoundGearWhineAnalysis))

    def results_for_connection(self, design_entity: '_1814.Connection') -> 'Iterable[_5675.ConnectionCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ConnectionCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5675.ConnectionCompoundGearWhineAnalysis))

    def results_for_inter_mountable_component_connection(self, design_entity: '_1823.InterMountableComponentConnection') -> 'Iterable[_5701.InterMountableComponentConnectionCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.InterMountableComponentConnectionCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5701.InterMountableComponentConnectionCompoundGearWhineAnalysis))

    def results_for_planetary_connection(self, design_entity: '_1826.PlanetaryConnection') -> 'Iterable[_5719.PlanetaryConnectionCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.PlanetaryConnectionCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5719.PlanetaryConnectionCompoundGearWhineAnalysis))

    def results_for_rolling_ring_connection(self, design_entity: '_1830.RollingRingConnection') -> 'Iterable[_5727.RollingRingConnectionCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.RollingRingConnectionCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5727.RollingRingConnectionCompoundGearWhineAnalysis))

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1834.ShaftToMountableComponentConnection') -> 'Iterable[_5731.ShaftToMountableComponentConnectionCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ShaftToMountableComponentConnectionCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5731.ShaftToMountableComponentConnectionCompoundGearWhineAnalysis))

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1840.BevelDifferentialGearMesh') -> 'Iterable[_5652.BevelDifferentialGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.BevelDifferentialGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5652.BevelDifferentialGearMeshCompoundGearWhineAnalysis))

    def results_for_concept_gear_mesh(self, design_entity: '_1844.ConceptGearMesh') -> 'Iterable[_5670.ConceptGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ConceptGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5670.ConceptGearMeshCompoundGearWhineAnalysis))

    def results_for_face_gear_mesh(self, design_entity: '_1850.FaceGearMesh') -> 'Iterable[_5690.FaceGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.FaceGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5690.FaceGearMeshCompoundGearWhineAnalysis))

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1864.StraightBevelDiffGearMesh') -> 'Iterable[_5740.StraightBevelDiffGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.StraightBevelDiffGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5740.StraightBevelDiffGearMeshCompoundGearWhineAnalysis))

    def results_for_bevel_gear_mesh(self, design_entity: '_1842.BevelGearMesh') -> 'Iterable[_5657.BevelGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.BevelGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5657.BevelGearMeshCompoundGearWhineAnalysis))

    def results_for_conical_gear_mesh(self, design_entity: '_1846.ConicalGearMesh') -> 'Iterable[_5673.ConicalGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ConicalGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5673.ConicalGearMeshCompoundGearWhineAnalysis))

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1838.AGMAGleasonConicalGearMesh') -> 'Iterable[_5645.AGMAGleasonConicalGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.AGMAGleasonConicalGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5645.AGMAGleasonConicalGearMeshCompoundGearWhineAnalysis))

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1848.CylindricalGearMesh') -> 'Iterable[_5684.CylindricalGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.CylindricalGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5684.CylindricalGearMeshCompoundGearWhineAnalysis))

    def results_for_hypoid_gear_mesh(self, design_entity: '_1854.HypoidGearMesh') -> 'Iterable[_5698.HypoidGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.HypoidGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5698.HypoidGearMeshCompoundGearWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1857.KlingelnbergCycloPalloidConicalGearMesh') -> 'Iterable[_5703.KlingelnbergCycloPalloidConicalGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.KlingelnbergCycloPalloidConicalGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5703.KlingelnbergCycloPalloidConicalGearMeshCompoundGearWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1858.KlingelnbergCycloPalloidHypoidGearMesh') -> 'Iterable[_5706.KlingelnbergCycloPalloidHypoidGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.KlingelnbergCycloPalloidHypoidGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5706.KlingelnbergCycloPalloidHypoidGearMeshCompoundGearWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1859.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> 'Iterable[_5709.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5709.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundGearWhineAnalysis))

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1862.SpiralBevelGearMesh') -> 'Iterable[_5734.SpiralBevelGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.SpiralBevelGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5734.SpiralBevelGearMeshCompoundGearWhineAnalysis))

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1866.StraightBevelGearMesh') -> 'Iterable[_5743.StraightBevelGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.StraightBevelGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5743.StraightBevelGearMeshCompoundGearWhineAnalysis))

    def results_for_worm_gear_mesh(self, design_entity: '_1868.WormGearMesh') -> 'Iterable[_5758.WormGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.WormGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5758.WormGearMeshCompoundGearWhineAnalysis))

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1870.ZerolBevelGearMesh') -> 'Iterable[_5761.ZerolBevelGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ZerolBevelGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5761.ZerolBevelGearMeshCompoundGearWhineAnalysis))

    def results_for_gear_mesh(self, design_entity: '_1852.GearMesh') -> 'Iterable[_5694.GearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.GearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5694.GearMeshCompoundGearWhineAnalysis))

    def results_for_part_to_part_shear_coupling_connection(self, design_entity: '_1878.PartToPartShearCouplingConnection') -> 'Iterable[_5717.PartToPartShearCouplingConnectionCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.PartToPartShearCouplingConnectionCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5717.PartToPartShearCouplingConnectionCompoundGearWhineAnalysis))

    def results_for_clutch_connection(self, design_entity: '_1872.ClutchConnection') -> 'Iterable[_5662.ClutchConnectionCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ClutchConnectionCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5662.ClutchConnectionCompoundGearWhineAnalysis))

    def results_for_concept_coupling_connection(self, design_entity: '_1874.ConceptCouplingConnection') -> 'Iterable[_5667.ConceptCouplingConnectionCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ConceptCouplingConnectionCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5667.ConceptCouplingConnectionCompoundGearWhineAnalysis))

    def results_for_coupling_connection(self, design_entity: '_1876.CouplingConnection') -> 'Iterable[_5678.CouplingConnectionCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.CouplingConnectionCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5678.CouplingConnectionCompoundGearWhineAnalysis))

    def results_for_spring_damper_connection(self, design_entity: '_1880.SpringDamperConnection') -> 'Iterable[_5737.SpringDamperConnectionCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.SpringDamperConnectionCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5737.SpringDamperConnectionCompoundGearWhineAnalysis))

    def results_for_torque_converter_connection(self, design_entity: '_1882.TorqueConverterConnection') -> 'Iterable[_5752.TorqueConverterConnectionCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.TorqueConverterConnectionCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5752.TorqueConverterConnectionCompoundGearWhineAnalysis))
