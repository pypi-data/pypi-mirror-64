'''_2602.py

AssemblyCompoundSteadyStateSynchronousResponseOnAShaft
'''


from typing import List

from mastapy.system_model.part_model import _1977
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2480
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
    _2603, _2605, _2608, _2614,
    _2615, _2616, _2621, _2626,
    _2636, _2640, _2646, _2647,
    _2654, _2655, _2662, _2665,
    _2666, _2667, _2669, _2671,
    _2676, _2677, _2678, _2685,
    _2680, _2684, _2690, _2691,
    _2696, _2699, _2702, _2706,
    _2710, _2714, _2717, _2597
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft.Compound', 'AssemblyCompoundSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundSteadyStateSynchronousResponseOnAShaft',)


class AssemblyCompoundSteadyStateSynchronousResponseOnAShaft(_2597.AbstractAssemblyCompoundSteadyStateSynchronousResponseOnAShaft):
    '''AssemblyCompoundSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundSteadyStateSynchronousResponseOnAShaft.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_2480.AssemblySteadyStateSynchronousResponseOnAShaft]':
        '''List[AssemblySteadyStateSynchronousResponseOnAShaft]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2480.AssemblySteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def assembly_steady_state_synchronous_response_on_a_shaft_load_cases(self) -> 'List[_2480.AssemblySteadyStateSynchronousResponseOnAShaft]':
        '''List[AssemblySteadyStateSynchronousResponseOnAShaft]: 'AssemblySteadyStateSynchronousResponseOnAShaftLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySteadyStateSynchronousResponseOnAShaftLoadCases, constructor.new(_2480.AssemblySteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def bearings(self) -> 'List[_2603.BearingCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[BearingCompoundSteadyStateSynchronousResponseOnAShaft]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_2603.BearingCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def belt_drives(self) -> 'List[_2605.BeltDriveCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[BeltDriveCompoundSteadyStateSynchronousResponseOnAShaft]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_2605.BeltDriveCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_2608.BevelDifferentialGearSetCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[BevelDifferentialGearSetCompoundSteadyStateSynchronousResponseOnAShaft]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_2608.BevelDifferentialGearSetCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def bolts(self) -> 'List[_2614.BoltCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[BoltCompoundSteadyStateSynchronousResponseOnAShaft]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_2614.BoltCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def bolted_joints(self) -> 'List[_2615.BoltedJointCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[BoltedJointCompoundSteadyStateSynchronousResponseOnAShaft]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_2615.BoltedJointCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def clutches(self) -> 'List[_2616.ClutchCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[ClutchCompoundSteadyStateSynchronousResponseOnAShaft]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_2616.ClutchCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def concept_couplings(self) -> 'List[_2621.ConceptCouplingCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[ConceptCouplingCompoundSteadyStateSynchronousResponseOnAShaft]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_2621.ConceptCouplingCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_2626.ConceptGearSetCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[ConceptGearSetCompoundSteadyStateSynchronousResponseOnAShaft]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_2626.ConceptGearSetCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def cv_ts(self) -> 'List[_2636.CVTCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[CVTCompoundSteadyStateSynchronousResponseOnAShaft]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_2636.CVTCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_2640.CylindricalGearSetCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[CylindricalGearSetCompoundSteadyStateSynchronousResponseOnAShaft]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_2640.CylindricalGearSetCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def face_gear_sets(self) -> 'List[_2646.FaceGearSetCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[FaceGearSetCompoundSteadyStateSynchronousResponseOnAShaft]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_2646.FaceGearSetCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_2647.FlexiblePinAssemblyCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[FlexiblePinAssemblyCompoundSteadyStateSynchronousResponseOnAShaft]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_2647.FlexiblePinAssemblyCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_2654.HypoidGearSetCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[HypoidGearSetCompoundSteadyStateSynchronousResponseOnAShaft]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_2654.HypoidGearSetCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def imported_fe_components(self) -> 'List[_2655.ImportedFEComponentCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[ImportedFEComponentCompoundSteadyStateSynchronousResponseOnAShaft]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_2655.ImportedFEComponentCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_2662.KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponseOnAShaft]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_2662.KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_2665.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_2665.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def mass_discs(self) -> 'List[_2666.MassDiscCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[MassDiscCompoundSteadyStateSynchronousResponseOnAShaft]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_2666.MassDiscCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def measurement_components(self) -> 'List[_2667.MeasurementComponentCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[MeasurementComponentCompoundSteadyStateSynchronousResponseOnAShaft]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_2667.MeasurementComponentCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def oil_seals(self) -> 'List[_2669.OilSealCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[OilSealCompoundSteadyStateSynchronousResponseOnAShaft]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_2669.OilSealCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_2671.PartToPartShearCouplingCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[PartToPartShearCouplingCompoundSteadyStateSynchronousResponseOnAShaft]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_2671.PartToPartShearCouplingCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def planet_carriers(self) -> 'List[_2676.PlanetCarrierCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[PlanetCarrierCompoundSteadyStateSynchronousResponseOnAShaft]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_2676.PlanetCarrierCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def point_loads(self) -> 'List[_2677.PointLoadCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[PointLoadCompoundSteadyStateSynchronousResponseOnAShaft]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_2677.PointLoadCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def power_loads(self) -> 'List[_2678.PowerLoadCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[PowerLoadCompoundSteadyStateSynchronousResponseOnAShaft]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_2678.PowerLoadCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_2685.ShaftHubConnectionCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[ShaftHubConnectionCompoundSteadyStateSynchronousResponseOnAShaft]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_2685.ShaftHubConnectionCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_2680.RollingRingAssemblyCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[RollingRingAssemblyCompoundSteadyStateSynchronousResponseOnAShaft]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_2680.RollingRingAssemblyCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def shafts(self) -> 'List[_2684.ShaftCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[ShaftCompoundSteadyStateSynchronousResponseOnAShaft]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_2684.ShaftCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_2690.SpiralBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[SpiralBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_2690.SpiralBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def spring_dampers(self) -> 'List[_2691.SpringDamperCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[SpringDamperCompoundSteadyStateSynchronousResponseOnAShaft]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_2691.SpringDamperCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_2696.StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseOnAShaft]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_2696.StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_2699.StraightBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[StraightBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_2699.StraightBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def synchronisers(self) -> 'List[_2702.SynchroniserCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[SynchroniserCompoundSteadyStateSynchronousResponseOnAShaft]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_2702.SynchroniserCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def torque_converters(self) -> 'List[_2706.TorqueConverterCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[TorqueConverterCompoundSteadyStateSynchronousResponseOnAShaft]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_2706.TorqueConverterCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_2710.UnbalancedMassCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[UnbalancedMassCompoundSteadyStateSynchronousResponseOnAShaft]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_2710.UnbalancedMassCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_2714.WormGearSetCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[WormGearSetCompoundSteadyStateSynchronousResponseOnAShaft]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_2714.WormGearSetCompoundSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_2717.ZerolBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft]':
        '''List[ZerolBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_2717.ZerolBevelGearSetCompoundSteadyStateSynchronousResponseOnAShaft))
        return value
