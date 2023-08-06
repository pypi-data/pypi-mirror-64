'''_2198.py

CompoundSingleMeshWhineAnalysisAnalysis
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
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import (
    _5528, _5529, _5534, _5545,
    _5546, _5551, _5562, _5573,
    _5574, _5578, _5533, _5582,
    _5586, _5597, _5598, _5599,
    _5600, _5601, _5607, _5608,
    _5609, _5614, _5618, _5641,
    _5642, _5615, _5555, _5557,
    _5575, _5577, _5530, _5532,
    _5537, _5539, _5540, _5541,
    _5542, _5544, _5558, _5560,
    _5569, _5571, _5572, _5579,
    _5581, _5583, _5585, _5588,
    _5590, _5591, _5593, _5594,
    _5596, _5606, _5619, _5621,
    _5625, _5627, _5628, _5630,
    _5631, _5632, _5643, _5645,
    _5646, _5648, _5602, _5604,
    _5536, _5547, _5549, _5552,
    _5554, _5563, _5565, _5567,
    _5568, _5610, _5616, _5612,
    _5611, _5622, _5624, _5633,
    _5634, _5635, _5636, _5637,
    _5639, _5640, _5566, _5535,
    _5550, _5561, _5587, _5605,
    _5613, _5617, _5538, _5556,
    _5576, _5626, _5543, _5559,
    _5531, _5570, _5584, _5589,
    _5592, _5595, _5620, _5629,
    _5644, _5647, _5580, _5603,
    _5548, _5553, _5564, _5623,
    _5638
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

_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundSingleMeshWhineAnalysisAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundSingleMeshWhineAnalysisAnalysis',)


class CompoundSingleMeshWhineAnalysisAnalysis(_2149.CompoundAnalysis):
    '''CompoundSingleMeshWhineAnalysisAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_SINGLE_MESH_WHINE_ANALYSIS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundSingleMeshWhineAnalysisAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    def results_for_abstract_assembly(self, design_entity: '_1978.AbstractAssembly') -> 'Iterable[_5528.AbstractAssemblyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.AbstractAssemblyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5528.AbstractAssemblyCompoundSingleMeshWhineAnalysis))

    def results_for_abstract_shaft_or_housing(self, design_entity: '_1979.AbstractShaftOrHousing') -> 'Iterable[_5529.AbstractShaftOrHousingCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.AbstractShaftOrHousingCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5529.AbstractShaftOrHousingCompoundSingleMeshWhineAnalysis))

    def results_for_bearing(self, design_entity: '_1982.Bearing') -> 'Iterable[_5534.BearingCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BearingCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5534.BearingCompoundSingleMeshWhineAnalysis))

    def results_for_bolt(self, design_entity: '_1984.Bolt') -> 'Iterable[_5545.BoltCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BoltCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5545.BoltCompoundSingleMeshWhineAnalysis))

    def results_for_bolted_joint(self, design_entity: '_1985.BoltedJoint') -> 'Iterable[_5546.BoltedJointCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BoltedJointCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5546.BoltedJointCompoundSingleMeshWhineAnalysis))

    def results_for_component(self, design_entity: '_1986.Component') -> 'Iterable[_5551.ComponentCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ComponentCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5551.ComponentCompoundSingleMeshWhineAnalysis))

    def results_for_connector(self, design_entity: '_1989.Connector') -> 'Iterable[_5562.ConnectorCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConnectorCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5562.ConnectorCompoundSingleMeshWhineAnalysis))

    def results_for_datum(self, design_entity: '_1990.Datum') -> 'Iterable[_5573.DatumCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.DatumCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5573.DatumCompoundSingleMeshWhineAnalysis))

    def results_for_external_cad_model(self, design_entity: '_1993.ExternalCADModel') -> 'Iterable[_5574.ExternalCADModelCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ExternalCADModelCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5574.ExternalCADModelCompoundSingleMeshWhineAnalysis))

    def results_for_flexible_pin_assembly(self, design_entity: '_1994.FlexiblePinAssembly') -> 'Iterable[_5578.FlexiblePinAssemblyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.FlexiblePinAssemblyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5578.FlexiblePinAssemblyCompoundSingleMeshWhineAnalysis))

    def results_for_assembly(self, design_entity: '_1977.Assembly') -> 'Iterable[_5533.AssemblyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.AssemblyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5533.AssemblyCompoundSingleMeshWhineAnalysis))

    def results_for_guide_dxf_model(self, design_entity: '_1995.GuideDxfModel') -> 'Iterable[_5582.GuideDxfModelCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.GuideDxfModelCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5582.GuideDxfModelCompoundSingleMeshWhineAnalysis))

    def results_for_imported_fe_component(self, design_entity: '_1998.ImportedFEComponent') -> 'Iterable[_5586.ImportedFEComponentCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ImportedFEComponentCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5586.ImportedFEComponentCompoundSingleMeshWhineAnalysis))

    def results_for_mass_disc(self, design_entity: '_2001.MassDisc') -> 'Iterable[_5597.MassDiscCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.MassDiscCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5597.MassDiscCompoundSingleMeshWhineAnalysis))

    def results_for_measurement_component(self, design_entity: '_2002.MeasurementComponent') -> 'Iterable[_5598.MeasurementComponentCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.MeasurementComponentCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5598.MeasurementComponentCompoundSingleMeshWhineAnalysis))

    def results_for_mountable_component(self, design_entity: '_2003.MountableComponent') -> 'Iterable[_5599.MountableComponentCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.MountableComponentCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5599.MountableComponentCompoundSingleMeshWhineAnalysis))

    def results_for_oil_seal(self, design_entity: '_2005.OilSeal') -> 'Iterable[_5600.OilSealCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.OilSealCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5600.OilSealCompoundSingleMeshWhineAnalysis))

    def results_for_part(self, design_entity: '_2006.Part') -> 'Iterable[_5601.PartCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PartCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5601.PartCompoundSingleMeshWhineAnalysis))

    def results_for_planet_carrier(self, design_entity: '_2007.PlanetCarrier') -> 'Iterable[_5607.PlanetCarrierCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PlanetCarrierCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5607.PlanetCarrierCompoundSingleMeshWhineAnalysis))

    def results_for_point_load(self, design_entity: '_2009.PointLoad') -> 'Iterable[_5608.PointLoadCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PointLoadCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5608.PointLoadCompoundSingleMeshWhineAnalysis))

    def results_for_power_load(self, design_entity: '_2010.PowerLoad') -> 'Iterable[_5609.PowerLoadCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PowerLoadCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5609.PowerLoadCompoundSingleMeshWhineAnalysis))

    def results_for_root_assembly(self, design_entity: '_2012.RootAssembly') -> 'Iterable[_5614.RootAssemblyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.RootAssemblyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5614.RootAssemblyCompoundSingleMeshWhineAnalysis))

    def results_for_specialised_assembly(self, design_entity: '_2014.SpecialisedAssembly') -> 'Iterable[_5618.SpecialisedAssemblyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SpecialisedAssemblyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5618.SpecialisedAssemblyCompoundSingleMeshWhineAnalysis))

    def results_for_unbalanced_mass(self, design_entity: '_2015.UnbalancedMass') -> 'Iterable[_5641.UnbalancedMassCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.UnbalancedMassCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5641.UnbalancedMassCompoundSingleMeshWhineAnalysis))

    def results_for_virtual_component(self, design_entity: '_2016.VirtualComponent') -> 'Iterable[_5642.VirtualComponentCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.VirtualComponentCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5642.VirtualComponentCompoundSingleMeshWhineAnalysis))

    def results_for_shaft(self, design_entity: '_2019.Shaft') -> 'Iterable[_5615.ShaftCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ShaftCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5615.ShaftCompoundSingleMeshWhineAnalysis))

    def results_for_concept_gear(self, design_entity: '_2057.ConceptGear') -> 'Iterable[_5555.ConceptGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConceptGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5555.ConceptGearCompoundSingleMeshWhineAnalysis))

    def results_for_concept_gear_set(self, design_entity: '_2058.ConceptGearSet') -> 'Iterable[_5557.ConceptGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConceptGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5557.ConceptGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_face_gear(self, design_entity: '_2064.FaceGear') -> 'Iterable[_5575.FaceGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.FaceGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5575.FaceGearCompoundSingleMeshWhineAnalysis))

    def results_for_face_gear_set(self, design_entity: '_2065.FaceGearSet') -> 'Iterable[_5577.FaceGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.FaceGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5577.FaceGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_agma_gleason_conical_gear(self, design_entity: '_2049.AGMAGleasonConicalGear') -> 'Iterable[_5530.AGMAGleasonConicalGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.AGMAGleasonConicalGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5530.AGMAGleasonConicalGearCompoundSingleMeshWhineAnalysis))

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_2050.AGMAGleasonConicalGearSet') -> 'Iterable[_5532.AGMAGleasonConicalGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.AGMAGleasonConicalGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5532.AGMAGleasonConicalGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_differential_gear(self, design_entity: '_2051.BevelDifferentialGear') -> 'Iterable[_5537.BevelDifferentialGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelDifferentialGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5537.BevelDifferentialGearCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_differential_gear_set(self, design_entity: '_2052.BevelDifferentialGearSet') -> 'Iterable[_5539.BevelDifferentialGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelDifferentialGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5539.BevelDifferentialGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2053.BevelDifferentialPlanetGear') -> 'Iterable[_5540.BevelDifferentialPlanetGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelDifferentialPlanetGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5540.BevelDifferentialPlanetGearCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2054.BevelDifferentialSunGear') -> 'Iterable[_5541.BevelDifferentialSunGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelDifferentialSunGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5541.BevelDifferentialSunGearCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_gear(self, design_entity: '_2055.BevelGear') -> 'Iterable[_5542.BevelGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5542.BevelGearCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_gear_set(self, design_entity: '_2056.BevelGearSet') -> 'Iterable[_5544.BevelGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5544.BevelGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_conical_gear(self, design_entity: '_2059.ConicalGear') -> 'Iterable[_5558.ConicalGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConicalGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5558.ConicalGearCompoundSingleMeshWhineAnalysis))

    def results_for_conical_gear_set(self, design_entity: '_2060.ConicalGearSet') -> 'Iterable[_5560.ConicalGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConicalGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5560.ConicalGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_cylindrical_gear(self, design_entity: '_2061.CylindricalGear') -> 'Iterable[_5569.CylindricalGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CylindricalGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5569.CylindricalGearCompoundSingleMeshWhineAnalysis))

    def results_for_cylindrical_gear_set(self, design_entity: '_2062.CylindricalGearSet') -> 'Iterable[_5571.CylindricalGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CylindricalGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5571.CylindricalGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_cylindrical_planet_gear(self, design_entity: '_2063.CylindricalPlanetGear') -> 'Iterable[_5572.CylindricalPlanetGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CylindricalPlanetGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5572.CylindricalPlanetGearCompoundSingleMeshWhineAnalysis))

    def results_for_gear(self, design_entity: '_2066.Gear') -> 'Iterable[_5579.GearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.GearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5579.GearCompoundSingleMeshWhineAnalysis))

    def results_for_gear_set(self, design_entity: '_2068.GearSet') -> 'Iterable[_5581.GearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.GearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5581.GearSetCompoundSingleMeshWhineAnalysis))

    def results_for_hypoid_gear(self, design_entity: '_2070.HypoidGear') -> 'Iterable[_5583.HypoidGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.HypoidGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5583.HypoidGearCompoundSingleMeshWhineAnalysis))

    def results_for_hypoid_gear_set(self, design_entity: '_2071.HypoidGearSet') -> 'Iterable[_5585.HypoidGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.HypoidGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5585.HypoidGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2072.KlingelnbergCycloPalloidConicalGear') -> 'Iterable[_5588.KlingelnbergCycloPalloidConicalGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidConicalGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5588.KlingelnbergCycloPalloidConicalGearCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2073.KlingelnbergCycloPalloidConicalGearSet') -> 'Iterable[_5590.KlingelnbergCycloPalloidConicalGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidConicalGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5590.KlingelnbergCycloPalloidConicalGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2074.KlingelnbergCycloPalloidHypoidGear') -> 'Iterable[_5591.KlingelnbergCycloPalloidHypoidGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidHypoidGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5591.KlingelnbergCycloPalloidHypoidGearCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2075.KlingelnbergCycloPalloidHypoidGearSet') -> 'Iterable[_5593.KlingelnbergCycloPalloidHypoidGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidHypoidGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5593.KlingelnbergCycloPalloidHypoidGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2076.KlingelnbergCycloPalloidSpiralBevelGear') -> 'Iterable[_5594.KlingelnbergCycloPalloidSpiralBevelGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5594.KlingelnbergCycloPalloidSpiralBevelGearCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2077.KlingelnbergCycloPalloidSpiralBevelGearSet') -> 'Iterable[_5596.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5596.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_planetary_gear_set(self, design_entity: '_2078.PlanetaryGearSet') -> 'Iterable[_5606.PlanetaryGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PlanetaryGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5606.PlanetaryGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_spiral_bevel_gear(self, design_entity: '_2079.SpiralBevelGear') -> 'Iterable[_5619.SpiralBevelGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SpiralBevelGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5619.SpiralBevelGearCompoundSingleMeshWhineAnalysis))

    def results_for_spiral_bevel_gear_set(self, design_entity: '_2080.SpiralBevelGearSet') -> 'Iterable[_5621.SpiralBevelGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SpiralBevelGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5621.SpiralBevelGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2081.StraightBevelDiffGear') -> 'Iterable[_5625.StraightBevelDiffGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelDiffGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5625.StraightBevelDiffGearCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_2082.StraightBevelDiffGearSet') -> 'Iterable[_5627.StraightBevelDiffGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelDiffGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5627.StraightBevelDiffGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_gear(self, design_entity: '_2083.StraightBevelGear') -> 'Iterable[_5628.StraightBevelGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5628.StraightBevelGearCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_gear_set(self, design_entity: '_2084.StraightBevelGearSet') -> 'Iterable[_5630.StraightBevelGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5630.StraightBevelGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2085.StraightBevelPlanetGear') -> 'Iterable[_5631.StraightBevelPlanetGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelPlanetGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5631.StraightBevelPlanetGearCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2086.StraightBevelSunGear') -> 'Iterable[_5632.StraightBevelSunGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelSunGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5632.StraightBevelSunGearCompoundSingleMeshWhineAnalysis))

    def results_for_worm_gear(self, design_entity: '_2087.WormGear') -> 'Iterable[_5643.WormGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.WormGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5643.WormGearCompoundSingleMeshWhineAnalysis))

    def results_for_worm_gear_set(self, design_entity: '_2088.WormGearSet') -> 'Iterable[_5645.WormGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.WormGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5645.WormGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_zerol_bevel_gear(self, design_entity: '_2089.ZerolBevelGear') -> 'Iterable[_5646.ZerolBevelGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ZerolBevelGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5646.ZerolBevelGearCompoundSingleMeshWhineAnalysis))

    def results_for_zerol_bevel_gear_set(self, design_entity: '_2090.ZerolBevelGearSet') -> 'Iterable[_5648.ZerolBevelGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ZerolBevelGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5648.ZerolBevelGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_part_to_part_shear_coupling(self, design_entity: '_2119.PartToPartShearCoupling') -> 'Iterable[_5602.PartToPartShearCouplingCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PartToPartShearCouplingCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5602.PartToPartShearCouplingCompoundSingleMeshWhineAnalysis))

    def results_for_part_to_part_shear_coupling_half(self, design_entity: '_2120.PartToPartShearCouplingHalf') -> 'Iterable[_5604.PartToPartShearCouplingHalfCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PartToPartShearCouplingHalfCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5604.PartToPartShearCouplingHalfCompoundSingleMeshWhineAnalysis))

    def results_for_belt_drive(self, design_entity: '_2108.BeltDrive') -> 'Iterable[_5536.BeltDriveCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BeltDriveCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5536.BeltDriveCompoundSingleMeshWhineAnalysis))

    def results_for_clutch(self, design_entity: '_2110.Clutch') -> 'Iterable[_5547.ClutchCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ClutchCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5547.ClutchCompoundSingleMeshWhineAnalysis))

    def results_for_clutch_half(self, design_entity: '_2111.ClutchHalf') -> 'Iterable[_5549.ClutchHalfCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ClutchHalfCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5549.ClutchHalfCompoundSingleMeshWhineAnalysis))

    def results_for_concept_coupling(self, design_entity: '_2113.ConceptCoupling') -> 'Iterable[_5552.ConceptCouplingCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConceptCouplingCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5552.ConceptCouplingCompoundSingleMeshWhineAnalysis))

    def results_for_concept_coupling_half(self, design_entity: '_2114.ConceptCouplingHalf') -> 'Iterable[_5554.ConceptCouplingHalfCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConceptCouplingHalfCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5554.ConceptCouplingHalfCompoundSingleMeshWhineAnalysis))

    def results_for_coupling(self, design_entity: '_2115.Coupling') -> 'Iterable[_5563.CouplingCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CouplingCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5563.CouplingCompoundSingleMeshWhineAnalysis))

    def results_for_coupling_half(self, design_entity: '_2116.CouplingHalf') -> 'Iterable[_5565.CouplingHalfCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CouplingHalfCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5565.CouplingHalfCompoundSingleMeshWhineAnalysis))

    def results_for_cvt(self, design_entity: '_2117.CVT') -> 'Iterable[_5567.CVTCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CVTCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5567.CVTCompoundSingleMeshWhineAnalysis))

    def results_for_cvt_pulley(self, design_entity: '_2118.CVTPulley') -> 'Iterable[_5568.CVTPulleyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CVTPulleyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5568.CVTPulleyCompoundSingleMeshWhineAnalysis))

    def results_for_pulley(self, design_entity: '_2121.Pulley') -> 'Iterable[_5610.PulleyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PulleyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5610.PulleyCompoundSingleMeshWhineAnalysis))

    def results_for_shaft_hub_connection(self, design_entity: '_2129.ShaftHubConnection') -> 'Iterable[_5616.ShaftHubConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ShaftHubConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5616.ShaftHubConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_rolling_ring(self, design_entity: '_2127.RollingRing') -> 'Iterable[_5612.RollingRingCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.RollingRingCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5612.RollingRingCompoundSingleMeshWhineAnalysis))

    def results_for_rolling_ring_assembly(self, design_entity: '_2128.RollingRingAssembly') -> 'Iterable[_5611.RollingRingAssemblyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.RollingRingAssemblyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5611.RollingRingAssemblyCompoundSingleMeshWhineAnalysis))

    def results_for_spring_damper(self, design_entity: '_2130.SpringDamper') -> 'Iterable[_5622.SpringDamperCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SpringDamperCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5622.SpringDamperCompoundSingleMeshWhineAnalysis))

    def results_for_spring_damper_half(self, design_entity: '_2131.SpringDamperHalf') -> 'Iterable[_5624.SpringDamperHalfCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SpringDamperHalfCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5624.SpringDamperHalfCompoundSingleMeshWhineAnalysis))

    def results_for_synchroniser(self, design_entity: '_2132.Synchroniser') -> 'Iterable[_5633.SynchroniserCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SynchroniserCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5633.SynchroniserCompoundSingleMeshWhineAnalysis))

    def results_for_synchroniser_half(self, design_entity: '_2134.SynchroniserHalf') -> 'Iterable[_5634.SynchroniserHalfCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SynchroniserHalfCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5634.SynchroniserHalfCompoundSingleMeshWhineAnalysis))

    def results_for_synchroniser_part(self, design_entity: '_2135.SynchroniserPart') -> 'Iterable[_5635.SynchroniserPartCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SynchroniserPartCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5635.SynchroniserPartCompoundSingleMeshWhineAnalysis))

    def results_for_synchroniser_sleeve(self, design_entity: '_2136.SynchroniserSleeve') -> 'Iterable[_5636.SynchroniserSleeveCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SynchroniserSleeveCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5636.SynchroniserSleeveCompoundSingleMeshWhineAnalysis))

    def results_for_torque_converter(self, design_entity: '_2137.TorqueConverter') -> 'Iterable[_5637.TorqueConverterCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.TorqueConverterCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5637.TorqueConverterCompoundSingleMeshWhineAnalysis))

    def results_for_torque_converter_pump(self, design_entity: '_2138.TorqueConverterPump') -> 'Iterable[_5639.TorqueConverterPumpCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.TorqueConverterPumpCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5639.TorqueConverterPumpCompoundSingleMeshWhineAnalysis))

    def results_for_torque_converter_turbine(self, design_entity: '_2140.TorqueConverterTurbine') -> 'Iterable[_5640.TorqueConverterTurbineCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.TorqueConverterTurbineCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5640.TorqueConverterTurbineCompoundSingleMeshWhineAnalysis))

    def results_for_cvt_belt_connection(self, design_entity: '_1835.CVTBeltConnection') -> 'Iterable[_5566.CVTBeltConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CVTBeltConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5566.CVTBeltConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_belt_connection(self, design_entity: '_1830.BeltConnection') -> 'Iterable[_5535.BeltConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BeltConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5535.BeltConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_coaxial_connection(self, design_entity: '_1831.CoaxialConnection') -> 'Iterable[_5550.CoaxialConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CoaxialConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5550.CoaxialConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_connection(self, design_entity: '_1834.Connection') -> 'Iterable[_5561.ConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5561.ConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_inter_mountable_component_connection(self, design_entity: '_1843.InterMountableComponentConnection') -> 'Iterable[_5587.InterMountableComponentConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.InterMountableComponentConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5587.InterMountableComponentConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_planetary_connection(self, design_entity: '_1846.PlanetaryConnection') -> 'Iterable[_5605.PlanetaryConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PlanetaryConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5605.PlanetaryConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_rolling_ring_connection(self, design_entity: '_1850.RollingRingConnection') -> 'Iterable[_5613.RollingRingConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.RollingRingConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5613.RollingRingConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1854.ShaftToMountableComponentConnection') -> 'Iterable[_5617.ShaftToMountableComponentConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ShaftToMountableComponentConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5617.ShaftToMountableComponentConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1860.BevelDifferentialGearMesh') -> 'Iterable[_5538.BevelDifferentialGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelDifferentialGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5538.BevelDifferentialGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_concept_gear_mesh(self, design_entity: '_1864.ConceptGearMesh') -> 'Iterable[_5556.ConceptGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConceptGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5556.ConceptGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_face_gear_mesh(self, design_entity: '_1870.FaceGearMesh') -> 'Iterable[_5576.FaceGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.FaceGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5576.FaceGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1884.StraightBevelDiffGearMesh') -> 'Iterable[_5626.StraightBevelDiffGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelDiffGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5626.StraightBevelDiffGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_gear_mesh(self, design_entity: '_1862.BevelGearMesh') -> 'Iterable[_5543.BevelGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5543.BevelGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_conical_gear_mesh(self, design_entity: '_1866.ConicalGearMesh') -> 'Iterable[_5559.ConicalGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConicalGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5559.ConicalGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1858.AGMAGleasonConicalGearMesh') -> 'Iterable[_5531.AGMAGleasonConicalGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.AGMAGleasonConicalGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5531.AGMAGleasonConicalGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1868.CylindricalGearMesh') -> 'Iterable[_5570.CylindricalGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CylindricalGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5570.CylindricalGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_hypoid_gear_mesh(self, design_entity: '_1874.HypoidGearMesh') -> 'Iterable[_5584.HypoidGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.HypoidGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5584.HypoidGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1877.KlingelnbergCycloPalloidConicalGearMesh') -> 'Iterable[_5589.KlingelnbergCycloPalloidConicalGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidConicalGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5589.KlingelnbergCycloPalloidConicalGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1878.KlingelnbergCycloPalloidHypoidGearMesh') -> 'Iterable[_5592.KlingelnbergCycloPalloidHypoidGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidHypoidGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5592.KlingelnbergCycloPalloidHypoidGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1879.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> 'Iterable[_5595.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5595.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1882.SpiralBevelGearMesh') -> 'Iterable[_5620.SpiralBevelGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SpiralBevelGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5620.SpiralBevelGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1886.StraightBevelGearMesh') -> 'Iterable[_5629.StraightBevelGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5629.StraightBevelGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_worm_gear_mesh(self, design_entity: '_1888.WormGearMesh') -> 'Iterable[_5644.WormGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.WormGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5644.WormGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1890.ZerolBevelGearMesh') -> 'Iterable[_5647.ZerolBevelGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ZerolBevelGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5647.ZerolBevelGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_gear_mesh(self, design_entity: '_1872.GearMesh') -> 'Iterable[_5580.GearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.GearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5580.GearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_part_to_part_shear_coupling_connection(self, design_entity: '_1898.PartToPartShearCouplingConnection') -> 'Iterable[_5603.PartToPartShearCouplingConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PartToPartShearCouplingConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5603.PartToPartShearCouplingConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_clutch_connection(self, design_entity: '_1892.ClutchConnection') -> 'Iterable[_5548.ClutchConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ClutchConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5548.ClutchConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_concept_coupling_connection(self, design_entity: '_1894.ConceptCouplingConnection') -> 'Iterable[_5553.ConceptCouplingConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConceptCouplingConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5553.ConceptCouplingConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_coupling_connection(self, design_entity: '_1896.CouplingConnection') -> 'Iterable[_5564.CouplingConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CouplingConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5564.CouplingConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_spring_damper_connection(self, design_entity: '_1900.SpringDamperConnection') -> 'Iterable[_5623.SpringDamperConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SpringDamperConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5623.SpringDamperConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_torque_converter_connection(self, design_entity: '_1902.TorqueConverterConnection') -> 'Iterable[_5638.TorqueConverterConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.TorqueConverterConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5638.TorqueConverterConnectionCompoundSingleMeshWhineAnalysis))
