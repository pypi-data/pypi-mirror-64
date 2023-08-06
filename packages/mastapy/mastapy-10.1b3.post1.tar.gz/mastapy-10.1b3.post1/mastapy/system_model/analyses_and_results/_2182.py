'''_2182.py

CompoundAdvancedSystemDeflectionAnalysis
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
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
    _6357, _6358, _6363, _6374,
    _6375, _6380, _6391, _6402,
    _6403, _6407, _6362, _6411,
    _6415, _6426, _6427, _6428,
    _6429, _6430, _6436, _6437,
    _6438, _6443, _6447, _6470,
    _6471, _6444, _6384, _6386,
    _6404, _6406, _6359, _6361,
    _6366, _6368, _6369, _6370,
    _6371, _6373, _6387, _6389,
    _6398, _6400, _6401, _6408,
    _6410, _6412, _6414, _6417,
    _6419, _6420, _6422, _6423,
    _6425, _6435, _6448, _6450,
    _6454, _6456, _6457, _6459,
    _6460, _6461, _6472, _6474,
    _6475, _6477, _6431, _6433,
    _6365, _6376, _6378, _6381,
    _6383, _6392, _6394, _6396,
    _6397, _6439, _6445, _6441,
    _6440, _6451, _6453, _6462,
    _6463, _6464, _6465, _6466,
    _6468, _6469, _6395, _6364,
    _6379, _6390, _6416, _6434,
    _6442, _6446, _6367, _6385,
    _6405, _6455, _6372, _6388,
    _6360, _6399, _6413, _6418,
    _6421, _6424, _6449, _6458,
    _6473, _6476, _6409, _6432,
    _6377, _6382, _6393, _6452,
    _6467
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

_COMPOUND_ADVANCED_SYSTEM_DEFLECTION_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundAdvancedSystemDeflectionAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundAdvancedSystemDeflectionAnalysis',)


class CompoundAdvancedSystemDeflectionAnalysis(_2149.CompoundAnalysis):
    '''CompoundAdvancedSystemDeflectionAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_ADVANCED_SYSTEM_DEFLECTION_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundAdvancedSystemDeflectionAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    def results_for_abstract_assembly(self, design_entity: '_1978.AbstractAssembly') -> 'Iterable[_6357.AbstractAssemblyCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.AbstractAssemblyCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6357.AbstractAssemblyCompoundAdvancedSystemDeflection))

    def results_for_abstract_shaft_or_housing(self, design_entity: '_1979.AbstractShaftOrHousing') -> 'Iterable[_6358.AbstractShaftOrHousingCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.AbstractShaftOrHousingCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6358.AbstractShaftOrHousingCompoundAdvancedSystemDeflection))

    def results_for_bearing(self, design_entity: '_1982.Bearing') -> 'Iterable[_6363.BearingCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BearingCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6363.BearingCompoundAdvancedSystemDeflection))

    def results_for_bolt(self, design_entity: '_1984.Bolt') -> 'Iterable[_6374.BoltCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BoltCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6374.BoltCompoundAdvancedSystemDeflection))

    def results_for_bolted_joint(self, design_entity: '_1985.BoltedJoint') -> 'Iterable[_6375.BoltedJointCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BoltedJointCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6375.BoltedJointCompoundAdvancedSystemDeflection))

    def results_for_component(self, design_entity: '_1986.Component') -> 'Iterable[_6380.ComponentCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ComponentCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6380.ComponentCompoundAdvancedSystemDeflection))

    def results_for_connector(self, design_entity: '_1989.Connector') -> 'Iterable[_6391.ConnectorCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConnectorCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6391.ConnectorCompoundAdvancedSystemDeflection))

    def results_for_datum(self, design_entity: '_1990.Datum') -> 'Iterable[_6402.DatumCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.DatumCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6402.DatumCompoundAdvancedSystemDeflection))

    def results_for_external_cad_model(self, design_entity: '_1993.ExternalCADModel') -> 'Iterable[_6403.ExternalCADModelCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ExternalCADModelCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6403.ExternalCADModelCompoundAdvancedSystemDeflection))

    def results_for_flexible_pin_assembly(self, design_entity: '_1994.FlexiblePinAssembly') -> 'Iterable[_6407.FlexiblePinAssemblyCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.FlexiblePinAssemblyCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6407.FlexiblePinAssemblyCompoundAdvancedSystemDeflection))

    def results_for_assembly(self, design_entity: '_1977.Assembly') -> 'Iterable[_6362.AssemblyCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.AssemblyCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6362.AssemblyCompoundAdvancedSystemDeflection))

    def results_for_guide_dxf_model(self, design_entity: '_1995.GuideDxfModel') -> 'Iterable[_6411.GuideDxfModelCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.GuideDxfModelCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6411.GuideDxfModelCompoundAdvancedSystemDeflection))

    def results_for_imported_fe_component(self, design_entity: '_1998.ImportedFEComponent') -> 'Iterable[_6415.ImportedFEComponentCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ImportedFEComponentCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6415.ImportedFEComponentCompoundAdvancedSystemDeflection))

    def results_for_mass_disc(self, design_entity: '_2001.MassDisc') -> 'Iterable[_6426.MassDiscCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.MassDiscCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6426.MassDiscCompoundAdvancedSystemDeflection))

    def results_for_measurement_component(self, design_entity: '_2002.MeasurementComponent') -> 'Iterable[_6427.MeasurementComponentCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.MeasurementComponentCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6427.MeasurementComponentCompoundAdvancedSystemDeflection))

    def results_for_mountable_component(self, design_entity: '_2003.MountableComponent') -> 'Iterable[_6428.MountableComponentCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.MountableComponentCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6428.MountableComponentCompoundAdvancedSystemDeflection))

    def results_for_oil_seal(self, design_entity: '_2005.OilSeal') -> 'Iterable[_6429.OilSealCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.OilSealCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6429.OilSealCompoundAdvancedSystemDeflection))

    def results_for_part(self, design_entity: '_2006.Part') -> 'Iterable[_6430.PartCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PartCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6430.PartCompoundAdvancedSystemDeflection))

    def results_for_planet_carrier(self, design_entity: '_2007.PlanetCarrier') -> 'Iterable[_6436.PlanetCarrierCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PlanetCarrierCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6436.PlanetCarrierCompoundAdvancedSystemDeflection))

    def results_for_point_load(self, design_entity: '_2009.PointLoad') -> 'Iterable[_6437.PointLoadCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PointLoadCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6437.PointLoadCompoundAdvancedSystemDeflection))

    def results_for_power_load(self, design_entity: '_2010.PowerLoad') -> 'Iterable[_6438.PowerLoadCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PowerLoadCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6438.PowerLoadCompoundAdvancedSystemDeflection))

    def results_for_root_assembly(self, design_entity: '_2012.RootAssembly') -> 'Iterable[_6443.RootAssemblyCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.RootAssemblyCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6443.RootAssemblyCompoundAdvancedSystemDeflection))

    def results_for_specialised_assembly(self, design_entity: '_2014.SpecialisedAssembly') -> 'Iterable[_6447.SpecialisedAssemblyCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SpecialisedAssemblyCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6447.SpecialisedAssemblyCompoundAdvancedSystemDeflection))

    def results_for_unbalanced_mass(self, design_entity: '_2015.UnbalancedMass') -> 'Iterable[_6470.UnbalancedMassCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.UnbalancedMassCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6470.UnbalancedMassCompoundAdvancedSystemDeflection))

    def results_for_virtual_component(self, design_entity: '_2016.VirtualComponent') -> 'Iterable[_6471.VirtualComponentCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.VirtualComponentCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6471.VirtualComponentCompoundAdvancedSystemDeflection))

    def results_for_shaft(self, design_entity: '_2019.Shaft') -> 'Iterable[_6444.ShaftCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ShaftCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6444.ShaftCompoundAdvancedSystemDeflection))

    def results_for_concept_gear(self, design_entity: '_2057.ConceptGear') -> 'Iterable[_6384.ConceptGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConceptGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6384.ConceptGearCompoundAdvancedSystemDeflection))

    def results_for_concept_gear_set(self, design_entity: '_2058.ConceptGearSet') -> 'Iterable[_6386.ConceptGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConceptGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6386.ConceptGearSetCompoundAdvancedSystemDeflection))

    def results_for_face_gear(self, design_entity: '_2064.FaceGear') -> 'Iterable[_6404.FaceGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.FaceGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6404.FaceGearCompoundAdvancedSystemDeflection))

    def results_for_face_gear_set(self, design_entity: '_2065.FaceGearSet') -> 'Iterable[_6406.FaceGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.FaceGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6406.FaceGearSetCompoundAdvancedSystemDeflection))

    def results_for_agma_gleason_conical_gear(self, design_entity: '_2049.AGMAGleasonConicalGear') -> 'Iterable[_6359.AGMAGleasonConicalGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.AGMAGleasonConicalGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6359.AGMAGleasonConicalGearCompoundAdvancedSystemDeflection))

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_2050.AGMAGleasonConicalGearSet') -> 'Iterable[_6361.AGMAGleasonConicalGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.AGMAGleasonConicalGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6361.AGMAGleasonConicalGearSetCompoundAdvancedSystemDeflection))

    def results_for_bevel_differential_gear(self, design_entity: '_2051.BevelDifferentialGear') -> 'Iterable[_6366.BevelDifferentialGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BevelDifferentialGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6366.BevelDifferentialGearCompoundAdvancedSystemDeflection))

    def results_for_bevel_differential_gear_set(self, design_entity: '_2052.BevelDifferentialGearSet') -> 'Iterable[_6368.BevelDifferentialGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BevelDifferentialGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6368.BevelDifferentialGearSetCompoundAdvancedSystemDeflection))

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2053.BevelDifferentialPlanetGear') -> 'Iterable[_6369.BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6369.BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection))

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2054.BevelDifferentialSunGear') -> 'Iterable[_6370.BevelDifferentialSunGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BevelDifferentialSunGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6370.BevelDifferentialSunGearCompoundAdvancedSystemDeflection))

    def results_for_bevel_gear(self, design_entity: '_2055.BevelGear') -> 'Iterable[_6371.BevelGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BevelGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6371.BevelGearCompoundAdvancedSystemDeflection))

    def results_for_bevel_gear_set(self, design_entity: '_2056.BevelGearSet') -> 'Iterable[_6373.BevelGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BevelGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6373.BevelGearSetCompoundAdvancedSystemDeflection))

    def results_for_conical_gear(self, design_entity: '_2059.ConicalGear') -> 'Iterable[_6387.ConicalGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConicalGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6387.ConicalGearCompoundAdvancedSystemDeflection))

    def results_for_conical_gear_set(self, design_entity: '_2060.ConicalGearSet') -> 'Iterable[_6389.ConicalGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConicalGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6389.ConicalGearSetCompoundAdvancedSystemDeflection))

    def results_for_cylindrical_gear(self, design_entity: '_2061.CylindricalGear') -> 'Iterable[_6398.CylindricalGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CylindricalGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6398.CylindricalGearCompoundAdvancedSystemDeflection))

    def results_for_cylindrical_gear_set(self, design_entity: '_2062.CylindricalGearSet') -> 'Iterable[_6400.CylindricalGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CylindricalGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6400.CylindricalGearSetCompoundAdvancedSystemDeflection))

    def results_for_cylindrical_planet_gear(self, design_entity: '_2063.CylindricalPlanetGear') -> 'Iterable[_6401.CylindricalPlanetGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CylindricalPlanetGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6401.CylindricalPlanetGearCompoundAdvancedSystemDeflection))

    def results_for_gear(self, design_entity: '_2066.Gear') -> 'Iterable[_6408.GearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.GearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6408.GearCompoundAdvancedSystemDeflection))

    def results_for_gear_set(self, design_entity: '_2068.GearSet') -> 'Iterable[_6410.GearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.GearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6410.GearSetCompoundAdvancedSystemDeflection))

    def results_for_hypoid_gear(self, design_entity: '_2070.HypoidGear') -> 'Iterable[_6412.HypoidGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.HypoidGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6412.HypoidGearCompoundAdvancedSystemDeflection))

    def results_for_hypoid_gear_set(self, design_entity: '_2071.HypoidGearSet') -> 'Iterable[_6414.HypoidGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.HypoidGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6414.HypoidGearSetCompoundAdvancedSystemDeflection))

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2072.KlingelnbergCycloPalloidConicalGear') -> 'Iterable[_6417.KlingelnbergCycloPalloidConicalGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.KlingelnbergCycloPalloidConicalGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6417.KlingelnbergCycloPalloidConicalGearCompoundAdvancedSystemDeflection))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2073.KlingelnbergCycloPalloidConicalGearSet') -> 'Iterable[_6419.KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6419.KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2074.KlingelnbergCycloPalloidHypoidGear') -> 'Iterable[_6420.KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6420.KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2075.KlingelnbergCycloPalloidHypoidGearSet') -> 'Iterable[_6422.KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6422.KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedSystemDeflection))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2076.KlingelnbergCycloPalloidSpiralBevelGear') -> 'Iterable[_6423.KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6423.KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedSystemDeflection))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2077.KlingelnbergCycloPalloidSpiralBevelGearSet') -> 'Iterable[_6425.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6425.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection))

    def results_for_planetary_gear_set(self, design_entity: '_2078.PlanetaryGearSet') -> 'Iterable[_6435.PlanetaryGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PlanetaryGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6435.PlanetaryGearSetCompoundAdvancedSystemDeflection))

    def results_for_spiral_bevel_gear(self, design_entity: '_2079.SpiralBevelGear') -> 'Iterable[_6448.SpiralBevelGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SpiralBevelGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6448.SpiralBevelGearCompoundAdvancedSystemDeflection))

    def results_for_spiral_bevel_gear_set(self, design_entity: '_2080.SpiralBevelGearSet') -> 'Iterable[_6450.SpiralBevelGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SpiralBevelGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6450.SpiralBevelGearSetCompoundAdvancedSystemDeflection))

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2081.StraightBevelDiffGear') -> 'Iterable[_6454.StraightBevelDiffGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.StraightBevelDiffGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6454.StraightBevelDiffGearCompoundAdvancedSystemDeflection))

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_2082.StraightBevelDiffGearSet') -> 'Iterable[_6456.StraightBevelDiffGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.StraightBevelDiffGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6456.StraightBevelDiffGearSetCompoundAdvancedSystemDeflection))

    def results_for_straight_bevel_gear(self, design_entity: '_2083.StraightBevelGear') -> 'Iterable[_6457.StraightBevelGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.StraightBevelGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6457.StraightBevelGearCompoundAdvancedSystemDeflection))

    def results_for_straight_bevel_gear_set(self, design_entity: '_2084.StraightBevelGearSet') -> 'Iterable[_6459.StraightBevelGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.StraightBevelGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6459.StraightBevelGearSetCompoundAdvancedSystemDeflection))

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2085.StraightBevelPlanetGear') -> 'Iterable[_6460.StraightBevelPlanetGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.StraightBevelPlanetGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6460.StraightBevelPlanetGearCompoundAdvancedSystemDeflection))

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2086.StraightBevelSunGear') -> 'Iterable[_6461.StraightBevelSunGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.StraightBevelSunGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6461.StraightBevelSunGearCompoundAdvancedSystemDeflection))

    def results_for_worm_gear(self, design_entity: '_2087.WormGear') -> 'Iterable[_6472.WormGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.WormGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6472.WormGearCompoundAdvancedSystemDeflection))

    def results_for_worm_gear_set(self, design_entity: '_2088.WormGearSet') -> 'Iterable[_6474.WormGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.WormGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6474.WormGearSetCompoundAdvancedSystemDeflection))

    def results_for_zerol_bevel_gear(self, design_entity: '_2089.ZerolBevelGear') -> 'Iterable[_6475.ZerolBevelGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ZerolBevelGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6475.ZerolBevelGearCompoundAdvancedSystemDeflection))

    def results_for_zerol_bevel_gear_set(self, design_entity: '_2090.ZerolBevelGearSet') -> 'Iterable[_6477.ZerolBevelGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ZerolBevelGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6477.ZerolBevelGearSetCompoundAdvancedSystemDeflection))

    def results_for_part_to_part_shear_coupling(self, design_entity: '_2119.PartToPartShearCoupling') -> 'Iterable[_6431.PartToPartShearCouplingCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PartToPartShearCouplingCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6431.PartToPartShearCouplingCompoundAdvancedSystemDeflection))

    def results_for_part_to_part_shear_coupling_half(self, design_entity: '_2120.PartToPartShearCouplingHalf') -> 'Iterable[_6433.PartToPartShearCouplingHalfCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PartToPartShearCouplingHalfCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6433.PartToPartShearCouplingHalfCompoundAdvancedSystemDeflection))

    def results_for_belt_drive(self, design_entity: '_2108.BeltDrive') -> 'Iterable[_6365.BeltDriveCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BeltDriveCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6365.BeltDriveCompoundAdvancedSystemDeflection))

    def results_for_clutch(self, design_entity: '_2110.Clutch') -> 'Iterable[_6376.ClutchCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ClutchCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6376.ClutchCompoundAdvancedSystemDeflection))

    def results_for_clutch_half(self, design_entity: '_2111.ClutchHalf') -> 'Iterable[_6378.ClutchHalfCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ClutchHalfCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6378.ClutchHalfCompoundAdvancedSystemDeflection))

    def results_for_concept_coupling(self, design_entity: '_2113.ConceptCoupling') -> 'Iterable[_6381.ConceptCouplingCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConceptCouplingCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6381.ConceptCouplingCompoundAdvancedSystemDeflection))

    def results_for_concept_coupling_half(self, design_entity: '_2114.ConceptCouplingHalf') -> 'Iterable[_6383.ConceptCouplingHalfCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConceptCouplingHalfCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6383.ConceptCouplingHalfCompoundAdvancedSystemDeflection))

    def results_for_coupling(self, design_entity: '_2115.Coupling') -> 'Iterable[_6392.CouplingCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CouplingCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6392.CouplingCompoundAdvancedSystemDeflection))

    def results_for_coupling_half(self, design_entity: '_2116.CouplingHalf') -> 'Iterable[_6394.CouplingHalfCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CouplingHalfCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6394.CouplingHalfCompoundAdvancedSystemDeflection))

    def results_for_cvt(self, design_entity: '_2117.CVT') -> 'Iterable[_6396.CVTCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CVTCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6396.CVTCompoundAdvancedSystemDeflection))

    def results_for_cvt_pulley(self, design_entity: '_2118.CVTPulley') -> 'Iterable[_6397.CVTPulleyCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CVTPulleyCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6397.CVTPulleyCompoundAdvancedSystemDeflection))

    def results_for_pulley(self, design_entity: '_2121.Pulley') -> 'Iterable[_6439.PulleyCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PulleyCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6439.PulleyCompoundAdvancedSystemDeflection))

    def results_for_shaft_hub_connection(self, design_entity: '_2129.ShaftHubConnection') -> 'Iterable[_6445.ShaftHubConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ShaftHubConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6445.ShaftHubConnectionCompoundAdvancedSystemDeflection))

    def results_for_rolling_ring(self, design_entity: '_2127.RollingRing') -> 'Iterable[_6441.RollingRingCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.RollingRingCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6441.RollingRingCompoundAdvancedSystemDeflection))

    def results_for_rolling_ring_assembly(self, design_entity: '_2128.RollingRingAssembly') -> 'Iterable[_6440.RollingRingAssemblyCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.RollingRingAssemblyCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6440.RollingRingAssemblyCompoundAdvancedSystemDeflection))

    def results_for_spring_damper(self, design_entity: '_2130.SpringDamper') -> 'Iterable[_6451.SpringDamperCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SpringDamperCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6451.SpringDamperCompoundAdvancedSystemDeflection))

    def results_for_spring_damper_half(self, design_entity: '_2131.SpringDamperHalf') -> 'Iterable[_6453.SpringDamperHalfCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SpringDamperHalfCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6453.SpringDamperHalfCompoundAdvancedSystemDeflection))

    def results_for_synchroniser(self, design_entity: '_2132.Synchroniser') -> 'Iterable[_6462.SynchroniserCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SynchroniserCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6462.SynchroniserCompoundAdvancedSystemDeflection))

    def results_for_synchroniser_half(self, design_entity: '_2134.SynchroniserHalf') -> 'Iterable[_6463.SynchroniserHalfCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SynchroniserHalfCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6463.SynchroniserHalfCompoundAdvancedSystemDeflection))

    def results_for_synchroniser_part(self, design_entity: '_2135.SynchroniserPart') -> 'Iterable[_6464.SynchroniserPartCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SynchroniserPartCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6464.SynchroniserPartCompoundAdvancedSystemDeflection))

    def results_for_synchroniser_sleeve(self, design_entity: '_2136.SynchroniserSleeve') -> 'Iterable[_6465.SynchroniserSleeveCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SynchroniserSleeveCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6465.SynchroniserSleeveCompoundAdvancedSystemDeflection))

    def results_for_torque_converter(self, design_entity: '_2137.TorqueConverter') -> 'Iterable[_6466.TorqueConverterCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.TorqueConverterCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6466.TorqueConverterCompoundAdvancedSystemDeflection))

    def results_for_torque_converter_pump(self, design_entity: '_2138.TorqueConverterPump') -> 'Iterable[_6468.TorqueConverterPumpCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.TorqueConverterPumpCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6468.TorqueConverterPumpCompoundAdvancedSystemDeflection))

    def results_for_torque_converter_turbine(self, design_entity: '_2140.TorqueConverterTurbine') -> 'Iterable[_6469.TorqueConverterTurbineCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.TorqueConverterTurbineCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6469.TorqueConverterTurbineCompoundAdvancedSystemDeflection))

    def results_for_cvt_belt_connection(self, design_entity: '_1835.CVTBeltConnection') -> 'Iterable[_6395.CVTBeltConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CVTBeltConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6395.CVTBeltConnectionCompoundAdvancedSystemDeflection))

    def results_for_belt_connection(self, design_entity: '_1830.BeltConnection') -> 'Iterable[_6364.BeltConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BeltConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6364.BeltConnectionCompoundAdvancedSystemDeflection))

    def results_for_coaxial_connection(self, design_entity: '_1831.CoaxialConnection') -> 'Iterable[_6379.CoaxialConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CoaxialConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6379.CoaxialConnectionCompoundAdvancedSystemDeflection))

    def results_for_connection(self, design_entity: '_1834.Connection') -> 'Iterable[_6390.ConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6390.ConnectionCompoundAdvancedSystemDeflection))

    def results_for_inter_mountable_component_connection(self, design_entity: '_1843.InterMountableComponentConnection') -> 'Iterable[_6416.InterMountableComponentConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.InterMountableComponentConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6416.InterMountableComponentConnectionCompoundAdvancedSystemDeflection))

    def results_for_planetary_connection(self, design_entity: '_1846.PlanetaryConnection') -> 'Iterable[_6434.PlanetaryConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PlanetaryConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6434.PlanetaryConnectionCompoundAdvancedSystemDeflection))

    def results_for_rolling_ring_connection(self, design_entity: '_1850.RollingRingConnection') -> 'Iterable[_6442.RollingRingConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.RollingRingConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6442.RollingRingConnectionCompoundAdvancedSystemDeflection))

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1854.ShaftToMountableComponentConnection') -> 'Iterable[_6446.ShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6446.ShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection))

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1860.BevelDifferentialGearMesh') -> 'Iterable[_6367.BevelDifferentialGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BevelDifferentialGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6367.BevelDifferentialGearMeshCompoundAdvancedSystemDeflection))

    def results_for_concept_gear_mesh(self, design_entity: '_1864.ConceptGearMesh') -> 'Iterable[_6385.ConceptGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConceptGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6385.ConceptGearMeshCompoundAdvancedSystemDeflection))

    def results_for_face_gear_mesh(self, design_entity: '_1870.FaceGearMesh') -> 'Iterable[_6405.FaceGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.FaceGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6405.FaceGearMeshCompoundAdvancedSystemDeflection))

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1884.StraightBevelDiffGearMesh') -> 'Iterable[_6455.StraightBevelDiffGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.StraightBevelDiffGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6455.StraightBevelDiffGearMeshCompoundAdvancedSystemDeflection))

    def results_for_bevel_gear_mesh(self, design_entity: '_1862.BevelGearMesh') -> 'Iterable[_6372.BevelGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BevelGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6372.BevelGearMeshCompoundAdvancedSystemDeflection))

    def results_for_conical_gear_mesh(self, design_entity: '_1866.ConicalGearMesh') -> 'Iterable[_6388.ConicalGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConicalGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6388.ConicalGearMeshCompoundAdvancedSystemDeflection))

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1858.AGMAGleasonConicalGearMesh') -> 'Iterable[_6360.AGMAGleasonConicalGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.AGMAGleasonConicalGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6360.AGMAGleasonConicalGearMeshCompoundAdvancedSystemDeflection))

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1868.CylindricalGearMesh') -> 'Iterable[_6399.CylindricalGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CylindricalGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6399.CylindricalGearMeshCompoundAdvancedSystemDeflection))

    def results_for_hypoid_gear_mesh(self, design_entity: '_1874.HypoidGearMesh') -> 'Iterable[_6413.HypoidGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.HypoidGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6413.HypoidGearMeshCompoundAdvancedSystemDeflection))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1877.KlingelnbergCycloPalloidConicalGearMesh') -> 'Iterable[_6418.KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6418.KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedSystemDeflection))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1878.KlingelnbergCycloPalloidHypoidGearMesh') -> 'Iterable[_6421.KlingelnbergCycloPalloidHypoidGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.KlingelnbergCycloPalloidHypoidGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6421.KlingelnbergCycloPalloidHypoidGearMeshCompoundAdvancedSystemDeflection))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1879.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> 'Iterable[_6424.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6424.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundAdvancedSystemDeflection))

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1882.SpiralBevelGearMesh') -> 'Iterable[_6449.SpiralBevelGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SpiralBevelGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6449.SpiralBevelGearMeshCompoundAdvancedSystemDeflection))

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1886.StraightBevelGearMesh') -> 'Iterable[_6458.StraightBevelGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.StraightBevelGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6458.StraightBevelGearMeshCompoundAdvancedSystemDeflection))

    def results_for_worm_gear_mesh(self, design_entity: '_1888.WormGearMesh') -> 'Iterable[_6473.WormGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.WormGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6473.WormGearMeshCompoundAdvancedSystemDeflection))

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1890.ZerolBevelGearMesh') -> 'Iterable[_6476.ZerolBevelGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ZerolBevelGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6476.ZerolBevelGearMeshCompoundAdvancedSystemDeflection))

    def results_for_gear_mesh(self, design_entity: '_1872.GearMesh') -> 'Iterable[_6409.GearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.GearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6409.GearMeshCompoundAdvancedSystemDeflection))

    def results_for_part_to_part_shear_coupling_connection(self, design_entity: '_1898.PartToPartShearCouplingConnection') -> 'Iterable[_6432.PartToPartShearCouplingConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PartToPartShearCouplingConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6432.PartToPartShearCouplingConnectionCompoundAdvancedSystemDeflection))

    def results_for_clutch_connection(self, design_entity: '_1892.ClutchConnection') -> 'Iterable[_6377.ClutchConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ClutchConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6377.ClutchConnectionCompoundAdvancedSystemDeflection))

    def results_for_concept_coupling_connection(self, design_entity: '_1894.ConceptCouplingConnection') -> 'Iterable[_6382.ConceptCouplingConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConceptCouplingConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6382.ConceptCouplingConnectionCompoundAdvancedSystemDeflection))

    def results_for_coupling_connection(self, design_entity: '_1896.CouplingConnection') -> 'Iterable[_6393.CouplingConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CouplingConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6393.CouplingConnectionCompoundAdvancedSystemDeflection))

    def results_for_spring_damper_connection(self, design_entity: '_1900.SpringDamperConnection') -> 'Iterable[_6452.SpringDamperConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SpringDamperConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6452.SpringDamperConnectionCompoundAdvancedSystemDeflection))

    def results_for_torque_converter_connection(self, design_entity: '_1902.TorqueConverterConnection') -> 'Iterable[_6467.TorqueConverterConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.TorqueConverterConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6467.TorqueConverterConnectionCompoundAdvancedSystemDeflection))
