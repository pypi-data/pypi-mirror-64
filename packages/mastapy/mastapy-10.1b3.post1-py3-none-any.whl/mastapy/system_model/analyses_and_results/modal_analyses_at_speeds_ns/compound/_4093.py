'''_4093.py

AssemblyCompoundModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model import _1977
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _3968
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import (
    _4094, _4096, _4099, _4105,
    _4106, _4107, _4112, _4117,
    _4127, _4131, _4137, _4138,
    _4145, _4146, _4153, _4156,
    _4157, _4158, _4160, _4162,
    _4167, _4168, _4169, _4176,
    _4171, _4175, _4181, _4182,
    _4187, _4190, _4193, _4197,
    _4201, _4205, _4208, _4088
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'AssemblyCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundModalAnalysesAtSpeeds',)


class AssemblyCompoundModalAnalysesAtSpeeds(_4088.AbstractAssemblyCompoundModalAnalysesAtSpeeds):
    '''AssemblyCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundModalAnalysesAtSpeeds.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_3968.AssemblyModalAnalysesAtSpeeds]':
        '''List[AssemblyModalAnalysesAtSpeeds]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3968.AssemblyModalAnalysesAtSpeeds))
        return value

    @property
    def assembly_modal_analyses_at_speeds_load_cases(self) -> 'List[_3968.AssemblyModalAnalysesAtSpeeds]':
        '''List[AssemblyModalAnalysesAtSpeeds]: 'AssemblyModalAnalysesAtSpeedsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysesAtSpeedsLoadCases, constructor.new(_3968.AssemblyModalAnalysesAtSpeeds))
        return value

    @property
    def bearings(self) -> 'List[_4094.BearingCompoundModalAnalysesAtSpeeds]':
        '''List[BearingCompoundModalAnalysesAtSpeeds]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_4094.BearingCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def belt_drives(self) -> 'List[_4096.BeltDriveCompoundModalAnalysesAtSpeeds]':
        '''List[BeltDriveCompoundModalAnalysesAtSpeeds]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_4096.BeltDriveCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_4099.BevelDifferentialGearSetCompoundModalAnalysesAtSpeeds]':
        '''List[BevelDifferentialGearSetCompoundModalAnalysesAtSpeeds]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_4099.BevelDifferentialGearSetCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def bolts(self) -> 'List[_4105.BoltCompoundModalAnalysesAtSpeeds]':
        '''List[BoltCompoundModalAnalysesAtSpeeds]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_4105.BoltCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def bolted_joints(self) -> 'List[_4106.BoltedJointCompoundModalAnalysesAtSpeeds]':
        '''List[BoltedJointCompoundModalAnalysesAtSpeeds]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_4106.BoltedJointCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def clutches(self) -> 'List[_4107.ClutchCompoundModalAnalysesAtSpeeds]':
        '''List[ClutchCompoundModalAnalysesAtSpeeds]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_4107.ClutchCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def concept_couplings(self) -> 'List[_4112.ConceptCouplingCompoundModalAnalysesAtSpeeds]':
        '''List[ConceptCouplingCompoundModalAnalysesAtSpeeds]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_4112.ConceptCouplingCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_4117.ConceptGearSetCompoundModalAnalysesAtSpeeds]':
        '''List[ConceptGearSetCompoundModalAnalysesAtSpeeds]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_4117.ConceptGearSetCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def cv_ts(self) -> 'List[_4127.CVTCompoundModalAnalysesAtSpeeds]':
        '''List[CVTCompoundModalAnalysesAtSpeeds]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_4127.CVTCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_4131.CylindricalGearSetCompoundModalAnalysesAtSpeeds]':
        '''List[CylindricalGearSetCompoundModalAnalysesAtSpeeds]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_4131.CylindricalGearSetCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def face_gear_sets(self) -> 'List[_4137.FaceGearSetCompoundModalAnalysesAtSpeeds]':
        '''List[FaceGearSetCompoundModalAnalysesAtSpeeds]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_4137.FaceGearSetCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_4138.FlexiblePinAssemblyCompoundModalAnalysesAtSpeeds]':
        '''List[FlexiblePinAssemblyCompoundModalAnalysesAtSpeeds]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_4138.FlexiblePinAssemblyCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_4145.HypoidGearSetCompoundModalAnalysesAtSpeeds]':
        '''List[HypoidGearSetCompoundModalAnalysesAtSpeeds]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_4145.HypoidGearSetCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def imported_fe_components(self) -> 'List[_4146.ImportedFEComponentCompoundModalAnalysesAtSpeeds]':
        '''List[ImportedFEComponentCompoundModalAnalysesAtSpeeds]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_4146.ImportedFEComponentCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_4153.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysesAtSpeeds]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysesAtSpeeds]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_4153.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_4156.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysesAtSpeeds]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysesAtSpeeds]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_4156.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def mass_discs(self) -> 'List[_4157.MassDiscCompoundModalAnalysesAtSpeeds]':
        '''List[MassDiscCompoundModalAnalysesAtSpeeds]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_4157.MassDiscCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def measurement_components(self) -> 'List[_4158.MeasurementComponentCompoundModalAnalysesAtSpeeds]':
        '''List[MeasurementComponentCompoundModalAnalysesAtSpeeds]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_4158.MeasurementComponentCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def oil_seals(self) -> 'List[_4160.OilSealCompoundModalAnalysesAtSpeeds]':
        '''List[OilSealCompoundModalAnalysesAtSpeeds]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_4160.OilSealCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_4162.PartToPartShearCouplingCompoundModalAnalysesAtSpeeds]':
        '''List[PartToPartShearCouplingCompoundModalAnalysesAtSpeeds]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_4162.PartToPartShearCouplingCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def planet_carriers(self) -> 'List[_4167.PlanetCarrierCompoundModalAnalysesAtSpeeds]':
        '''List[PlanetCarrierCompoundModalAnalysesAtSpeeds]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_4167.PlanetCarrierCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def point_loads(self) -> 'List[_4168.PointLoadCompoundModalAnalysesAtSpeeds]':
        '''List[PointLoadCompoundModalAnalysesAtSpeeds]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_4168.PointLoadCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def power_loads(self) -> 'List[_4169.PowerLoadCompoundModalAnalysesAtSpeeds]':
        '''List[PowerLoadCompoundModalAnalysesAtSpeeds]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_4169.PowerLoadCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_4176.ShaftHubConnectionCompoundModalAnalysesAtSpeeds]':
        '''List[ShaftHubConnectionCompoundModalAnalysesAtSpeeds]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_4176.ShaftHubConnectionCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_4171.RollingRingAssemblyCompoundModalAnalysesAtSpeeds]':
        '''List[RollingRingAssemblyCompoundModalAnalysesAtSpeeds]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_4171.RollingRingAssemblyCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def shafts(self) -> 'List[_4175.ShaftCompoundModalAnalysesAtSpeeds]':
        '''List[ShaftCompoundModalAnalysesAtSpeeds]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_4175.ShaftCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_4181.SpiralBevelGearSetCompoundModalAnalysesAtSpeeds]':
        '''List[SpiralBevelGearSetCompoundModalAnalysesAtSpeeds]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_4181.SpiralBevelGearSetCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def spring_dampers(self) -> 'List[_4182.SpringDamperCompoundModalAnalysesAtSpeeds]':
        '''List[SpringDamperCompoundModalAnalysesAtSpeeds]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_4182.SpringDamperCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_4187.StraightBevelDiffGearSetCompoundModalAnalysesAtSpeeds]':
        '''List[StraightBevelDiffGearSetCompoundModalAnalysesAtSpeeds]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_4187.StraightBevelDiffGearSetCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_4190.StraightBevelGearSetCompoundModalAnalysesAtSpeeds]':
        '''List[StraightBevelGearSetCompoundModalAnalysesAtSpeeds]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_4190.StraightBevelGearSetCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def synchronisers(self) -> 'List[_4193.SynchroniserCompoundModalAnalysesAtSpeeds]':
        '''List[SynchroniserCompoundModalAnalysesAtSpeeds]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_4193.SynchroniserCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def torque_converters(self) -> 'List[_4197.TorqueConverterCompoundModalAnalysesAtSpeeds]':
        '''List[TorqueConverterCompoundModalAnalysesAtSpeeds]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_4197.TorqueConverterCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_4201.UnbalancedMassCompoundModalAnalysesAtSpeeds]':
        '''List[UnbalancedMassCompoundModalAnalysesAtSpeeds]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_4201.UnbalancedMassCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_4205.WormGearSetCompoundModalAnalysesAtSpeeds]':
        '''List[WormGearSetCompoundModalAnalysesAtSpeeds]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_4205.WormGearSetCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_4208.ZerolBevelGearSetCompoundModalAnalysesAtSpeeds]':
        '''List[ZerolBevelGearSetCompoundModalAnalysesAtSpeeds]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_4208.ZerolBevelGearSetCompoundModalAnalysesAtSpeeds))
        return value
