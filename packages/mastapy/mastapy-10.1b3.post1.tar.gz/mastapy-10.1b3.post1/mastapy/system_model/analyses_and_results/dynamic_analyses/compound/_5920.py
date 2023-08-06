'''_5920.py

AssemblyCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _1977
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5797
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import (
    _5921, _5923, _5926, _5932,
    _5933, _5934, _5939, _5944,
    _5954, _5958, _5964, _5965,
    _5972, _5973, _5980, _5983,
    _5984, _5985, _5987, _5989,
    _5994, _5995, _5996, _6003,
    _5998, _6002, _6008, _6009,
    _6014, _6017, _6020, _6024,
    _6028, _6032, _6035, _5915
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'AssemblyCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundDynamicAnalysis',)


class AssemblyCompoundDynamicAnalysis(_5915.AbstractAssemblyCompoundDynamicAnalysis):
    '''AssemblyCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1977.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1977.Assembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1977.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1977.Assembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5797.AssemblyDynamicAnalysis]':
        '''List[AssemblyDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5797.AssemblyDynamicAnalysis))
        return value

    @property
    def assembly_dynamic_analysis_load_cases(self) -> 'List[_5797.AssemblyDynamicAnalysis]':
        '''List[AssemblyDynamicAnalysis]: 'AssemblyDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyDynamicAnalysisLoadCases, constructor.new(_5797.AssemblyDynamicAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_5921.BearingCompoundDynamicAnalysis]':
        '''List[BearingCompoundDynamicAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_5921.BearingCompoundDynamicAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_5923.BeltDriveCompoundDynamicAnalysis]':
        '''List[BeltDriveCompoundDynamicAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_5923.BeltDriveCompoundDynamicAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_5926.BevelDifferentialGearSetCompoundDynamicAnalysis]':
        '''List[BevelDifferentialGearSetCompoundDynamicAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_5926.BevelDifferentialGearSetCompoundDynamicAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_5932.BoltCompoundDynamicAnalysis]':
        '''List[BoltCompoundDynamicAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_5932.BoltCompoundDynamicAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_5933.BoltedJointCompoundDynamicAnalysis]':
        '''List[BoltedJointCompoundDynamicAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_5933.BoltedJointCompoundDynamicAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_5934.ClutchCompoundDynamicAnalysis]':
        '''List[ClutchCompoundDynamicAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_5934.ClutchCompoundDynamicAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_5939.ConceptCouplingCompoundDynamicAnalysis]':
        '''List[ConceptCouplingCompoundDynamicAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_5939.ConceptCouplingCompoundDynamicAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_5944.ConceptGearSetCompoundDynamicAnalysis]':
        '''List[ConceptGearSetCompoundDynamicAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_5944.ConceptGearSetCompoundDynamicAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_5954.CVTCompoundDynamicAnalysis]':
        '''List[CVTCompoundDynamicAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_5954.CVTCompoundDynamicAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_5958.CylindricalGearSetCompoundDynamicAnalysis]':
        '''List[CylindricalGearSetCompoundDynamicAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_5958.CylindricalGearSetCompoundDynamicAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_5964.FaceGearSetCompoundDynamicAnalysis]':
        '''List[FaceGearSetCompoundDynamicAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_5964.FaceGearSetCompoundDynamicAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_5965.FlexiblePinAssemblyCompoundDynamicAnalysis]':
        '''List[FlexiblePinAssemblyCompoundDynamicAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_5965.FlexiblePinAssemblyCompoundDynamicAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_5972.HypoidGearSetCompoundDynamicAnalysis]':
        '''List[HypoidGearSetCompoundDynamicAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_5972.HypoidGearSetCompoundDynamicAnalysis))
        return value

    @property
    def imported_fe_components(self) -> 'List[_5973.ImportedFEComponentCompoundDynamicAnalysis]':
        '''List[ImportedFEComponentCompoundDynamicAnalysis]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_5973.ImportedFEComponentCompoundDynamicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_5980.KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_5980.KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_5983.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_5983.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_5984.MassDiscCompoundDynamicAnalysis]':
        '''List[MassDiscCompoundDynamicAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_5984.MassDiscCompoundDynamicAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_5985.MeasurementComponentCompoundDynamicAnalysis]':
        '''List[MeasurementComponentCompoundDynamicAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_5985.MeasurementComponentCompoundDynamicAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_5987.OilSealCompoundDynamicAnalysis]':
        '''List[OilSealCompoundDynamicAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_5987.OilSealCompoundDynamicAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_5989.PartToPartShearCouplingCompoundDynamicAnalysis]':
        '''List[PartToPartShearCouplingCompoundDynamicAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_5989.PartToPartShearCouplingCompoundDynamicAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_5994.PlanetCarrierCompoundDynamicAnalysis]':
        '''List[PlanetCarrierCompoundDynamicAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_5994.PlanetCarrierCompoundDynamicAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_5995.PointLoadCompoundDynamicAnalysis]':
        '''List[PointLoadCompoundDynamicAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_5995.PointLoadCompoundDynamicAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_5996.PowerLoadCompoundDynamicAnalysis]':
        '''List[PowerLoadCompoundDynamicAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_5996.PowerLoadCompoundDynamicAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_6003.ShaftHubConnectionCompoundDynamicAnalysis]':
        '''List[ShaftHubConnectionCompoundDynamicAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_6003.ShaftHubConnectionCompoundDynamicAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_5998.RollingRingAssemblyCompoundDynamicAnalysis]':
        '''List[RollingRingAssemblyCompoundDynamicAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_5998.RollingRingAssemblyCompoundDynamicAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_6002.ShaftCompoundDynamicAnalysis]':
        '''List[ShaftCompoundDynamicAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_6002.ShaftCompoundDynamicAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_6008.SpiralBevelGearSetCompoundDynamicAnalysis]':
        '''List[SpiralBevelGearSetCompoundDynamicAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_6008.SpiralBevelGearSetCompoundDynamicAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_6009.SpringDamperCompoundDynamicAnalysis]':
        '''List[SpringDamperCompoundDynamicAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_6009.SpringDamperCompoundDynamicAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_6014.StraightBevelDiffGearSetCompoundDynamicAnalysis]':
        '''List[StraightBevelDiffGearSetCompoundDynamicAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_6014.StraightBevelDiffGearSetCompoundDynamicAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_6017.StraightBevelGearSetCompoundDynamicAnalysis]':
        '''List[StraightBevelGearSetCompoundDynamicAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_6017.StraightBevelGearSetCompoundDynamicAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_6020.SynchroniserCompoundDynamicAnalysis]':
        '''List[SynchroniserCompoundDynamicAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_6020.SynchroniserCompoundDynamicAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_6024.TorqueConverterCompoundDynamicAnalysis]':
        '''List[TorqueConverterCompoundDynamicAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_6024.TorqueConverterCompoundDynamicAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_6028.UnbalancedMassCompoundDynamicAnalysis]':
        '''List[UnbalancedMassCompoundDynamicAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_6028.UnbalancedMassCompoundDynamicAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_6032.WormGearSetCompoundDynamicAnalysis]':
        '''List[WormGearSetCompoundDynamicAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_6032.WormGearSetCompoundDynamicAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_6035.ZerolBevelGearSetCompoundDynamicAnalysis]':
        '''List[ZerolBevelGearSetCompoundDynamicAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_6035.ZerolBevelGearSetCompoundDynamicAnalysis))
        return value
