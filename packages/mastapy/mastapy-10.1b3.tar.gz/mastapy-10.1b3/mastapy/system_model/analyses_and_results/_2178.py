'''_2178.py

CompoundSingleMeshWhineAnalysisAnalysis
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
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import (
    _5508, _5509, _5514, _5525,
    _5526, _5531, _5542, _5553,
    _5554, _5558, _5513, _5562,
    _5566, _5577, _5578, _5579,
    _5580, _5581, _5587, _5588,
    _5589, _5594, _5598, _5621,
    _5622, _5595, _5535, _5537,
    _5555, _5557, _5510, _5512,
    _5517, _5519, _5520, _5521,
    _5522, _5524, _5538, _5540,
    _5549, _5551, _5552, _5559,
    _5561, _5563, _5565, _5568,
    _5570, _5571, _5573, _5574,
    _5576, _5586, _5599, _5601,
    _5605, _5607, _5608, _5610,
    _5611, _5612, _5623, _5625,
    _5626, _5628, _5582, _5584,
    _5516, _5527, _5529, _5532,
    _5534, _5543, _5545, _5547,
    _5548, _5590, _5596, _5592,
    _5591, _5602, _5604, _5613,
    _5614, _5615, _5616, _5617,
    _5619, _5620, _5546, _5515,
    _5530, _5541, _5567, _5585,
    _5593, _5597, _5518, _5536,
    _5556, _5606, _5523, _5539,
    _5511, _5550, _5564, _5569,
    _5572, _5575, _5600, _5609,
    _5624, _5627, _5560, _5583,
    _5528, _5533, _5544, _5603,
    _5618
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

_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundSingleMeshWhineAnalysisAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundSingleMeshWhineAnalysisAnalysis',)


class CompoundSingleMeshWhineAnalysisAnalysis(_2129.CompoundAnalysis):
    '''CompoundSingleMeshWhineAnalysisAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_SINGLE_MESH_WHINE_ANALYSIS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundSingleMeshWhineAnalysisAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    def results_for_abstract_assembly(self, design_entity: '_1958.AbstractAssembly') -> 'Iterable[_5508.AbstractAssemblyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.AbstractAssemblyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5508.AbstractAssemblyCompoundSingleMeshWhineAnalysis))

    def results_for_abstract_shaft_or_housing(self, design_entity: '_1959.AbstractShaftOrHousing') -> 'Iterable[_5509.AbstractShaftOrHousingCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.AbstractShaftOrHousingCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5509.AbstractShaftOrHousingCompoundSingleMeshWhineAnalysis))

    def results_for_bearing(self, design_entity: '_1962.Bearing') -> 'Iterable[_5514.BearingCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BearingCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5514.BearingCompoundSingleMeshWhineAnalysis))

    def results_for_bolt(self, design_entity: '_1964.Bolt') -> 'Iterable[_5525.BoltCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BoltCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5525.BoltCompoundSingleMeshWhineAnalysis))

    def results_for_bolted_joint(self, design_entity: '_1965.BoltedJoint') -> 'Iterable[_5526.BoltedJointCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BoltedJointCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5526.BoltedJointCompoundSingleMeshWhineAnalysis))

    def results_for_component(self, design_entity: '_1966.Component') -> 'Iterable[_5531.ComponentCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ComponentCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5531.ComponentCompoundSingleMeshWhineAnalysis))

    def results_for_connector(self, design_entity: '_1969.Connector') -> 'Iterable[_5542.ConnectorCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConnectorCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5542.ConnectorCompoundSingleMeshWhineAnalysis))

    def results_for_datum(self, design_entity: '_1970.Datum') -> 'Iterable[_5553.DatumCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.DatumCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5553.DatumCompoundSingleMeshWhineAnalysis))

    def results_for_external_cad_model(self, design_entity: '_1973.ExternalCADModel') -> 'Iterable[_5554.ExternalCADModelCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ExternalCADModelCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5554.ExternalCADModelCompoundSingleMeshWhineAnalysis))

    def results_for_flexible_pin_assembly(self, design_entity: '_1974.FlexiblePinAssembly') -> 'Iterable[_5558.FlexiblePinAssemblyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.FlexiblePinAssemblyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5558.FlexiblePinAssemblyCompoundSingleMeshWhineAnalysis))

    def results_for_assembly(self, design_entity: '_1957.Assembly') -> 'Iterable[_5513.AssemblyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.AssemblyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5513.AssemblyCompoundSingleMeshWhineAnalysis))

    def results_for_guide_dxf_model(self, design_entity: '_1975.GuideDxfModel') -> 'Iterable[_5562.GuideDxfModelCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.GuideDxfModelCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5562.GuideDxfModelCompoundSingleMeshWhineAnalysis))

    def results_for_imported_fe_component(self, design_entity: '_1978.ImportedFEComponent') -> 'Iterable[_5566.ImportedFEComponentCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ImportedFEComponentCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5566.ImportedFEComponentCompoundSingleMeshWhineAnalysis))

    def results_for_mass_disc(self, design_entity: '_1981.MassDisc') -> 'Iterable[_5577.MassDiscCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.MassDiscCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5577.MassDiscCompoundSingleMeshWhineAnalysis))

    def results_for_measurement_component(self, design_entity: '_1982.MeasurementComponent') -> 'Iterable[_5578.MeasurementComponentCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.MeasurementComponentCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5578.MeasurementComponentCompoundSingleMeshWhineAnalysis))

    def results_for_mountable_component(self, design_entity: '_1983.MountableComponent') -> 'Iterable[_5579.MountableComponentCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.MountableComponentCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5579.MountableComponentCompoundSingleMeshWhineAnalysis))

    def results_for_oil_seal(self, design_entity: '_1985.OilSeal') -> 'Iterable[_5580.OilSealCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.OilSealCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5580.OilSealCompoundSingleMeshWhineAnalysis))

    def results_for_part(self, design_entity: '_1986.Part') -> 'Iterable[_5581.PartCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PartCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5581.PartCompoundSingleMeshWhineAnalysis))

    def results_for_planet_carrier(self, design_entity: '_1987.PlanetCarrier') -> 'Iterable[_5587.PlanetCarrierCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PlanetCarrierCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5587.PlanetCarrierCompoundSingleMeshWhineAnalysis))

    def results_for_point_load(self, design_entity: '_1989.PointLoad') -> 'Iterable[_5588.PointLoadCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PointLoadCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5588.PointLoadCompoundSingleMeshWhineAnalysis))

    def results_for_power_load(self, design_entity: '_1990.PowerLoad') -> 'Iterable[_5589.PowerLoadCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PowerLoadCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5589.PowerLoadCompoundSingleMeshWhineAnalysis))

    def results_for_root_assembly(self, design_entity: '_1992.RootAssembly') -> 'Iterable[_5594.RootAssemblyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.RootAssemblyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5594.RootAssemblyCompoundSingleMeshWhineAnalysis))

    def results_for_specialised_assembly(self, design_entity: '_1994.SpecialisedAssembly') -> 'Iterable[_5598.SpecialisedAssemblyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SpecialisedAssemblyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5598.SpecialisedAssemblyCompoundSingleMeshWhineAnalysis))

    def results_for_unbalanced_mass(self, design_entity: '_1995.UnbalancedMass') -> 'Iterable[_5621.UnbalancedMassCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.UnbalancedMassCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5621.UnbalancedMassCompoundSingleMeshWhineAnalysis))

    def results_for_virtual_component(self, design_entity: '_1996.VirtualComponent') -> 'Iterable[_5622.VirtualComponentCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.VirtualComponentCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5622.VirtualComponentCompoundSingleMeshWhineAnalysis))

    def results_for_shaft(self, design_entity: '_1999.Shaft') -> 'Iterable[_5595.ShaftCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ShaftCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5595.ShaftCompoundSingleMeshWhineAnalysis))

    def results_for_concept_gear(self, design_entity: '_2037.ConceptGear') -> 'Iterable[_5535.ConceptGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConceptGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5535.ConceptGearCompoundSingleMeshWhineAnalysis))

    def results_for_concept_gear_set(self, design_entity: '_2038.ConceptGearSet') -> 'Iterable[_5537.ConceptGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConceptGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5537.ConceptGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_face_gear(self, design_entity: '_2044.FaceGear') -> 'Iterable[_5555.FaceGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.FaceGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5555.FaceGearCompoundSingleMeshWhineAnalysis))

    def results_for_face_gear_set(self, design_entity: '_2045.FaceGearSet') -> 'Iterable[_5557.FaceGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.FaceGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5557.FaceGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_agma_gleason_conical_gear(self, design_entity: '_2029.AGMAGleasonConicalGear') -> 'Iterable[_5510.AGMAGleasonConicalGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.AGMAGleasonConicalGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5510.AGMAGleasonConicalGearCompoundSingleMeshWhineAnalysis))

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_2030.AGMAGleasonConicalGearSet') -> 'Iterable[_5512.AGMAGleasonConicalGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.AGMAGleasonConicalGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5512.AGMAGleasonConicalGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_differential_gear(self, design_entity: '_2031.BevelDifferentialGear') -> 'Iterable[_5517.BevelDifferentialGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelDifferentialGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5517.BevelDifferentialGearCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_differential_gear_set(self, design_entity: '_2032.BevelDifferentialGearSet') -> 'Iterable[_5519.BevelDifferentialGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelDifferentialGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5519.BevelDifferentialGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2033.BevelDifferentialPlanetGear') -> 'Iterable[_5520.BevelDifferentialPlanetGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelDifferentialPlanetGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5520.BevelDifferentialPlanetGearCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2034.BevelDifferentialSunGear') -> 'Iterable[_5521.BevelDifferentialSunGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelDifferentialSunGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5521.BevelDifferentialSunGearCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_gear(self, design_entity: '_2035.BevelGear') -> 'Iterable[_5522.BevelGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5522.BevelGearCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_gear_set(self, design_entity: '_2036.BevelGearSet') -> 'Iterable[_5524.BevelGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5524.BevelGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_conical_gear(self, design_entity: '_2039.ConicalGear') -> 'Iterable[_5538.ConicalGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConicalGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5538.ConicalGearCompoundSingleMeshWhineAnalysis))

    def results_for_conical_gear_set(self, design_entity: '_2040.ConicalGearSet') -> 'Iterable[_5540.ConicalGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConicalGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5540.ConicalGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_cylindrical_gear(self, design_entity: '_2041.CylindricalGear') -> 'Iterable[_5549.CylindricalGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CylindricalGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5549.CylindricalGearCompoundSingleMeshWhineAnalysis))

    def results_for_cylindrical_gear_set(self, design_entity: '_2042.CylindricalGearSet') -> 'Iterable[_5551.CylindricalGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CylindricalGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5551.CylindricalGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_cylindrical_planet_gear(self, design_entity: '_2043.CylindricalPlanetGear') -> 'Iterable[_5552.CylindricalPlanetGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CylindricalPlanetGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5552.CylindricalPlanetGearCompoundSingleMeshWhineAnalysis))

    def results_for_gear(self, design_entity: '_2046.Gear') -> 'Iterable[_5559.GearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.GearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5559.GearCompoundSingleMeshWhineAnalysis))

    def results_for_gear_set(self, design_entity: '_2048.GearSet') -> 'Iterable[_5561.GearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.GearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5561.GearSetCompoundSingleMeshWhineAnalysis))

    def results_for_hypoid_gear(self, design_entity: '_2050.HypoidGear') -> 'Iterable[_5563.HypoidGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.HypoidGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5563.HypoidGearCompoundSingleMeshWhineAnalysis))

    def results_for_hypoid_gear_set(self, design_entity: '_2051.HypoidGearSet') -> 'Iterable[_5565.HypoidGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.HypoidGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5565.HypoidGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2052.KlingelnbergCycloPalloidConicalGear') -> 'Iterable[_5568.KlingelnbergCycloPalloidConicalGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidConicalGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5568.KlingelnbergCycloPalloidConicalGearCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2053.KlingelnbergCycloPalloidConicalGearSet') -> 'Iterable[_5570.KlingelnbergCycloPalloidConicalGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidConicalGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5570.KlingelnbergCycloPalloidConicalGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2054.KlingelnbergCycloPalloidHypoidGear') -> 'Iterable[_5571.KlingelnbergCycloPalloidHypoidGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidHypoidGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5571.KlingelnbergCycloPalloidHypoidGearCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2055.KlingelnbergCycloPalloidHypoidGearSet') -> 'Iterable[_5573.KlingelnbergCycloPalloidHypoidGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidHypoidGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5573.KlingelnbergCycloPalloidHypoidGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2056.KlingelnbergCycloPalloidSpiralBevelGear') -> 'Iterable[_5574.KlingelnbergCycloPalloidSpiralBevelGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5574.KlingelnbergCycloPalloidSpiralBevelGearCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2057.KlingelnbergCycloPalloidSpiralBevelGearSet') -> 'Iterable[_5576.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5576.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_planetary_gear_set(self, design_entity: '_2058.PlanetaryGearSet') -> 'Iterable[_5586.PlanetaryGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PlanetaryGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5586.PlanetaryGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_spiral_bevel_gear(self, design_entity: '_2059.SpiralBevelGear') -> 'Iterable[_5599.SpiralBevelGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SpiralBevelGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5599.SpiralBevelGearCompoundSingleMeshWhineAnalysis))

    def results_for_spiral_bevel_gear_set(self, design_entity: '_2060.SpiralBevelGearSet') -> 'Iterable[_5601.SpiralBevelGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SpiralBevelGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5601.SpiralBevelGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2061.StraightBevelDiffGear') -> 'Iterable[_5605.StraightBevelDiffGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelDiffGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5605.StraightBevelDiffGearCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_2062.StraightBevelDiffGearSet') -> 'Iterable[_5607.StraightBevelDiffGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelDiffGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5607.StraightBevelDiffGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_gear(self, design_entity: '_2063.StraightBevelGear') -> 'Iterable[_5608.StraightBevelGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5608.StraightBevelGearCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_gear_set(self, design_entity: '_2064.StraightBevelGearSet') -> 'Iterable[_5610.StraightBevelGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5610.StraightBevelGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2065.StraightBevelPlanetGear') -> 'Iterable[_5611.StraightBevelPlanetGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelPlanetGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5611.StraightBevelPlanetGearCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2066.StraightBevelSunGear') -> 'Iterable[_5612.StraightBevelSunGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelSunGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5612.StraightBevelSunGearCompoundSingleMeshWhineAnalysis))

    def results_for_worm_gear(self, design_entity: '_2067.WormGear') -> 'Iterable[_5623.WormGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.WormGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5623.WormGearCompoundSingleMeshWhineAnalysis))

    def results_for_worm_gear_set(self, design_entity: '_2068.WormGearSet') -> 'Iterable[_5625.WormGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.WormGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5625.WormGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_zerol_bevel_gear(self, design_entity: '_2069.ZerolBevelGear') -> 'Iterable[_5626.ZerolBevelGearCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ZerolBevelGearCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5626.ZerolBevelGearCompoundSingleMeshWhineAnalysis))

    def results_for_zerol_bevel_gear_set(self, design_entity: '_2070.ZerolBevelGearSet') -> 'Iterable[_5628.ZerolBevelGearSetCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ZerolBevelGearSetCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5628.ZerolBevelGearSetCompoundSingleMeshWhineAnalysis))

    def results_for_part_to_part_shear_coupling(self, design_entity: '_2099.PartToPartShearCoupling') -> 'Iterable[_5582.PartToPartShearCouplingCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PartToPartShearCouplingCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5582.PartToPartShearCouplingCompoundSingleMeshWhineAnalysis))

    def results_for_part_to_part_shear_coupling_half(self, design_entity: '_2100.PartToPartShearCouplingHalf') -> 'Iterable[_5584.PartToPartShearCouplingHalfCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PartToPartShearCouplingHalfCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5584.PartToPartShearCouplingHalfCompoundSingleMeshWhineAnalysis))

    def results_for_belt_drive(self, design_entity: '_2088.BeltDrive') -> 'Iterable[_5516.BeltDriveCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BeltDriveCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5516.BeltDriveCompoundSingleMeshWhineAnalysis))

    def results_for_clutch(self, design_entity: '_2090.Clutch') -> 'Iterable[_5527.ClutchCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ClutchCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5527.ClutchCompoundSingleMeshWhineAnalysis))

    def results_for_clutch_half(self, design_entity: '_2091.ClutchHalf') -> 'Iterable[_5529.ClutchHalfCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ClutchHalfCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5529.ClutchHalfCompoundSingleMeshWhineAnalysis))

    def results_for_concept_coupling(self, design_entity: '_2093.ConceptCoupling') -> 'Iterable[_5532.ConceptCouplingCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConceptCouplingCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5532.ConceptCouplingCompoundSingleMeshWhineAnalysis))

    def results_for_concept_coupling_half(self, design_entity: '_2094.ConceptCouplingHalf') -> 'Iterable[_5534.ConceptCouplingHalfCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConceptCouplingHalfCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5534.ConceptCouplingHalfCompoundSingleMeshWhineAnalysis))

    def results_for_coupling(self, design_entity: '_2095.Coupling') -> 'Iterable[_5543.CouplingCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CouplingCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5543.CouplingCompoundSingleMeshWhineAnalysis))

    def results_for_coupling_half(self, design_entity: '_2096.CouplingHalf') -> 'Iterable[_5545.CouplingHalfCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CouplingHalfCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5545.CouplingHalfCompoundSingleMeshWhineAnalysis))

    def results_for_cvt(self, design_entity: '_2097.CVT') -> 'Iterable[_5547.CVTCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CVTCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5547.CVTCompoundSingleMeshWhineAnalysis))

    def results_for_cvt_pulley(self, design_entity: '_2098.CVTPulley') -> 'Iterable[_5548.CVTPulleyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CVTPulleyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5548.CVTPulleyCompoundSingleMeshWhineAnalysis))

    def results_for_pulley(self, design_entity: '_2101.Pulley') -> 'Iterable[_5590.PulleyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PulleyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5590.PulleyCompoundSingleMeshWhineAnalysis))

    def results_for_shaft_hub_connection(self, design_entity: '_2109.ShaftHubConnection') -> 'Iterable[_5596.ShaftHubConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ShaftHubConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5596.ShaftHubConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_rolling_ring(self, design_entity: '_2107.RollingRing') -> 'Iterable[_5592.RollingRingCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.RollingRingCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5592.RollingRingCompoundSingleMeshWhineAnalysis))

    def results_for_rolling_ring_assembly(self, design_entity: '_2108.RollingRingAssembly') -> 'Iterable[_5591.RollingRingAssemblyCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.RollingRingAssemblyCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5591.RollingRingAssemblyCompoundSingleMeshWhineAnalysis))

    def results_for_spring_damper(self, design_entity: '_2110.SpringDamper') -> 'Iterable[_5602.SpringDamperCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SpringDamperCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5602.SpringDamperCompoundSingleMeshWhineAnalysis))

    def results_for_spring_damper_half(self, design_entity: '_2111.SpringDamperHalf') -> 'Iterable[_5604.SpringDamperHalfCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SpringDamperHalfCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5604.SpringDamperHalfCompoundSingleMeshWhineAnalysis))

    def results_for_synchroniser(self, design_entity: '_2112.Synchroniser') -> 'Iterable[_5613.SynchroniserCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SynchroniserCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5613.SynchroniserCompoundSingleMeshWhineAnalysis))

    def results_for_synchroniser_half(self, design_entity: '_2114.SynchroniserHalf') -> 'Iterable[_5614.SynchroniserHalfCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SynchroniserHalfCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5614.SynchroniserHalfCompoundSingleMeshWhineAnalysis))

    def results_for_synchroniser_part(self, design_entity: '_2115.SynchroniserPart') -> 'Iterable[_5615.SynchroniserPartCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SynchroniserPartCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5615.SynchroniserPartCompoundSingleMeshWhineAnalysis))

    def results_for_synchroniser_sleeve(self, design_entity: '_2116.SynchroniserSleeve') -> 'Iterable[_5616.SynchroniserSleeveCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SynchroniserSleeveCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5616.SynchroniserSleeveCompoundSingleMeshWhineAnalysis))

    def results_for_torque_converter(self, design_entity: '_2117.TorqueConverter') -> 'Iterable[_5617.TorqueConverterCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.TorqueConverterCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5617.TorqueConverterCompoundSingleMeshWhineAnalysis))

    def results_for_torque_converter_pump(self, design_entity: '_2118.TorqueConverterPump') -> 'Iterable[_5619.TorqueConverterPumpCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.TorqueConverterPumpCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5619.TorqueConverterPumpCompoundSingleMeshWhineAnalysis))

    def results_for_torque_converter_turbine(self, design_entity: '_2120.TorqueConverterTurbine') -> 'Iterable[_5620.TorqueConverterTurbineCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.TorqueConverterTurbineCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5620.TorqueConverterTurbineCompoundSingleMeshWhineAnalysis))

    def results_for_cvt_belt_connection(self, design_entity: '_1815.CVTBeltConnection') -> 'Iterable[_5546.CVTBeltConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CVTBeltConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5546.CVTBeltConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_belt_connection(self, design_entity: '_1810.BeltConnection') -> 'Iterable[_5515.BeltConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BeltConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5515.BeltConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_coaxial_connection(self, design_entity: '_1811.CoaxialConnection') -> 'Iterable[_5530.CoaxialConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CoaxialConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5530.CoaxialConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_connection(self, design_entity: '_1814.Connection') -> 'Iterable[_5541.ConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5541.ConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_inter_mountable_component_connection(self, design_entity: '_1823.InterMountableComponentConnection') -> 'Iterable[_5567.InterMountableComponentConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.InterMountableComponentConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5567.InterMountableComponentConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_planetary_connection(self, design_entity: '_1826.PlanetaryConnection') -> 'Iterable[_5585.PlanetaryConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PlanetaryConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5585.PlanetaryConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_rolling_ring_connection(self, design_entity: '_1830.RollingRingConnection') -> 'Iterable[_5593.RollingRingConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.RollingRingConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5593.RollingRingConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1834.ShaftToMountableComponentConnection') -> 'Iterable[_5597.ShaftToMountableComponentConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ShaftToMountableComponentConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5597.ShaftToMountableComponentConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1840.BevelDifferentialGearMesh') -> 'Iterable[_5518.BevelDifferentialGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelDifferentialGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5518.BevelDifferentialGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_concept_gear_mesh(self, design_entity: '_1844.ConceptGearMesh') -> 'Iterable[_5536.ConceptGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConceptGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5536.ConceptGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_face_gear_mesh(self, design_entity: '_1850.FaceGearMesh') -> 'Iterable[_5556.FaceGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.FaceGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5556.FaceGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1864.StraightBevelDiffGearMesh') -> 'Iterable[_5606.StraightBevelDiffGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelDiffGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5606.StraightBevelDiffGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_bevel_gear_mesh(self, design_entity: '_1842.BevelGearMesh') -> 'Iterable[_5523.BevelGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.BevelGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5523.BevelGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_conical_gear_mesh(self, design_entity: '_1846.ConicalGearMesh') -> 'Iterable[_5539.ConicalGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConicalGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5539.ConicalGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1838.AGMAGleasonConicalGearMesh') -> 'Iterable[_5511.AGMAGleasonConicalGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.AGMAGleasonConicalGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5511.AGMAGleasonConicalGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1848.CylindricalGearMesh') -> 'Iterable[_5550.CylindricalGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CylindricalGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5550.CylindricalGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_hypoid_gear_mesh(self, design_entity: '_1854.HypoidGearMesh') -> 'Iterable[_5564.HypoidGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.HypoidGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5564.HypoidGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1857.KlingelnbergCycloPalloidConicalGearMesh') -> 'Iterable[_5569.KlingelnbergCycloPalloidConicalGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidConicalGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5569.KlingelnbergCycloPalloidConicalGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1858.KlingelnbergCycloPalloidHypoidGearMesh') -> 'Iterable[_5572.KlingelnbergCycloPalloidHypoidGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidHypoidGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5572.KlingelnbergCycloPalloidHypoidGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1859.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> 'Iterable[_5575.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5575.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1862.SpiralBevelGearMesh') -> 'Iterable[_5600.SpiralBevelGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SpiralBevelGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5600.SpiralBevelGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1866.StraightBevelGearMesh') -> 'Iterable[_5609.StraightBevelGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.StraightBevelGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5609.StraightBevelGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_worm_gear_mesh(self, design_entity: '_1868.WormGearMesh') -> 'Iterable[_5624.WormGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.WormGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5624.WormGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1870.ZerolBevelGearMesh') -> 'Iterable[_5627.ZerolBevelGearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ZerolBevelGearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5627.ZerolBevelGearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_gear_mesh(self, design_entity: '_1852.GearMesh') -> 'Iterable[_5560.GearMeshCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.GearMeshCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5560.GearMeshCompoundSingleMeshWhineAnalysis))

    def results_for_part_to_part_shear_coupling_connection(self, design_entity: '_1878.PartToPartShearCouplingConnection') -> 'Iterable[_5583.PartToPartShearCouplingConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.PartToPartShearCouplingConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5583.PartToPartShearCouplingConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_clutch_connection(self, design_entity: '_1872.ClutchConnection') -> 'Iterable[_5528.ClutchConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ClutchConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5528.ClutchConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_concept_coupling_connection(self, design_entity: '_1874.ConceptCouplingConnection') -> 'Iterable[_5533.ConceptCouplingConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.ConceptCouplingConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5533.ConceptCouplingConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_coupling_connection(self, design_entity: '_1876.CouplingConnection') -> 'Iterable[_5544.CouplingConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.CouplingConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5544.CouplingConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_spring_damper_connection(self, design_entity: '_1880.SpringDamperConnection') -> 'Iterable[_5603.SpringDamperConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.SpringDamperConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5603.SpringDamperConnectionCompoundSingleMeshWhineAnalysis))

    def results_for_torque_converter_connection(self, design_entity: '_1882.TorqueConverterConnection') -> 'Iterable[_5618.TorqueConverterConnectionCompoundSingleMeshWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound.TorqueConverterConnectionCompoundSingleMeshWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5618.TorqueConverterConnectionCompoundSingleMeshWhineAnalysis))
