'''_5533.py

AssemblyCompoundSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _1977
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5410
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import (
    _5534, _5536, _5539, _5545,
    _5546, _5547, _5552, _5557,
    _5567, _5571, _5577, _5578,
    _5585, _5586, _5593, _5596,
    _5597, _5598, _5600, _5602,
    _5607, _5608, _5609, _5616,
    _5611, _5615, _5621, _5622,
    _5627, _5630, _5633, _5637,
    _5641, _5645, _5648, _5528
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'AssemblyCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundSingleMeshWhineAnalysis',)


class AssemblyCompoundSingleMeshWhineAnalysis(_5528.AbstractAssemblyCompoundSingleMeshWhineAnalysis):
    '''AssemblyCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundSingleMeshWhineAnalysis.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_5410.AssemblySingleMeshWhineAnalysis]':
        '''List[AssemblySingleMeshWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5410.AssemblySingleMeshWhineAnalysis))
        return value

    @property
    def assembly_single_mesh_whine_analysis_load_cases(self) -> 'List[_5410.AssemblySingleMeshWhineAnalysis]':
        '''List[AssemblySingleMeshWhineAnalysis]: 'AssemblySingleMeshWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySingleMeshWhineAnalysisLoadCases, constructor.new(_5410.AssemblySingleMeshWhineAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_5534.BearingCompoundSingleMeshWhineAnalysis]':
        '''List[BearingCompoundSingleMeshWhineAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_5534.BearingCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_5536.BeltDriveCompoundSingleMeshWhineAnalysis]':
        '''List[BeltDriveCompoundSingleMeshWhineAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_5536.BeltDriveCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_5539.BevelDifferentialGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[BevelDifferentialGearSetCompoundSingleMeshWhineAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_5539.BevelDifferentialGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_5545.BoltCompoundSingleMeshWhineAnalysis]':
        '''List[BoltCompoundSingleMeshWhineAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_5545.BoltCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_5546.BoltedJointCompoundSingleMeshWhineAnalysis]':
        '''List[BoltedJointCompoundSingleMeshWhineAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_5546.BoltedJointCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_5547.ClutchCompoundSingleMeshWhineAnalysis]':
        '''List[ClutchCompoundSingleMeshWhineAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_5547.ClutchCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_5552.ConceptCouplingCompoundSingleMeshWhineAnalysis]':
        '''List[ConceptCouplingCompoundSingleMeshWhineAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_5552.ConceptCouplingCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_5557.ConceptGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[ConceptGearSetCompoundSingleMeshWhineAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_5557.ConceptGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_5567.CVTCompoundSingleMeshWhineAnalysis]':
        '''List[CVTCompoundSingleMeshWhineAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_5567.CVTCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_5571.CylindricalGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[CylindricalGearSetCompoundSingleMeshWhineAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_5571.CylindricalGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_5577.FaceGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[FaceGearSetCompoundSingleMeshWhineAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_5577.FaceGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_5578.FlexiblePinAssemblyCompoundSingleMeshWhineAnalysis]':
        '''List[FlexiblePinAssemblyCompoundSingleMeshWhineAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_5578.FlexiblePinAssemblyCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_5585.HypoidGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[HypoidGearSetCompoundSingleMeshWhineAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_5585.HypoidGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def imported_fe_components(self) -> 'List[_5586.ImportedFEComponentCompoundSingleMeshWhineAnalysis]':
        '''List[ImportedFEComponentCompoundSingleMeshWhineAnalysis]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_5586.ImportedFEComponentCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_5593.KlingelnbergCycloPalloidHypoidGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundSingleMeshWhineAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_5593.KlingelnbergCycloPalloidHypoidGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_5596.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSingleMeshWhineAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_5596.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_5597.MassDiscCompoundSingleMeshWhineAnalysis]':
        '''List[MassDiscCompoundSingleMeshWhineAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_5597.MassDiscCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_5598.MeasurementComponentCompoundSingleMeshWhineAnalysis]':
        '''List[MeasurementComponentCompoundSingleMeshWhineAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_5598.MeasurementComponentCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_5600.OilSealCompoundSingleMeshWhineAnalysis]':
        '''List[OilSealCompoundSingleMeshWhineAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_5600.OilSealCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_5602.PartToPartShearCouplingCompoundSingleMeshWhineAnalysis]':
        '''List[PartToPartShearCouplingCompoundSingleMeshWhineAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_5602.PartToPartShearCouplingCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_5607.PlanetCarrierCompoundSingleMeshWhineAnalysis]':
        '''List[PlanetCarrierCompoundSingleMeshWhineAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_5607.PlanetCarrierCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_5608.PointLoadCompoundSingleMeshWhineAnalysis]':
        '''List[PointLoadCompoundSingleMeshWhineAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_5608.PointLoadCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_5609.PowerLoadCompoundSingleMeshWhineAnalysis]':
        '''List[PowerLoadCompoundSingleMeshWhineAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_5609.PowerLoadCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_5616.ShaftHubConnectionCompoundSingleMeshWhineAnalysis]':
        '''List[ShaftHubConnectionCompoundSingleMeshWhineAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_5616.ShaftHubConnectionCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_5611.RollingRingAssemblyCompoundSingleMeshWhineAnalysis]':
        '''List[RollingRingAssemblyCompoundSingleMeshWhineAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_5611.RollingRingAssemblyCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_5615.ShaftCompoundSingleMeshWhineAnalysis]':
        '''List[ShaftCompoundSingleMeshWhineAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_5615.ShaftCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_5621.SpiralBevelGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[SpiralBevelGearSetCompoundSingleMeshWhineAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_5621.SpiralBevelGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_5622.SpringDamperCompoundSingleMeshWhineAnalysis]':
        '''List[SpringDamperCompoundSingleMeshWhineAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_5622.SpringDamperCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_5627.StraightBevelDiffGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[StraightBevelDiffGearSetCompoundSingleMeshWhineAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_5627.StraightBevelDiffGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_5630.StraightBevelGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[StraightBevelGearSetCompoundSingleMeshWhineAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_5630.StraightBevelGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_5633.SynchroniserCompoundSingleMeshWhineAnalysis]':
        '''List[SynchroniserCompoundSingleMeshWhineAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_5633.SynchroniserCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_5637.TorqueConverterCompoundSingleMeshWhineAnalysis]':
        '''List[TorqueConverterCompoundSingleMeshWhineAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_5637.TorqueConverterCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_5641.UnbalancedMassCompoundSingleMeshWhineAnalysis]':
        '''List[UnbalancedMassCompoundSingleMeshWhineAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_5641.UnbalancedMassCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_5645.WormGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[WormGearSetCompoundSingleMeshWhineAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_5645.WormGearSetCompoundSingleMeshWhineAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_5648.ZerolBevelGearSetCompoundSingleMeshWhineAnalysis]':
        '''List[ZerolBevelGearSetCompoundSingleMeshWhineAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_5648.ZerolBevelGearSetCompoundSingleMeshWhineAnalysis))
        return value
