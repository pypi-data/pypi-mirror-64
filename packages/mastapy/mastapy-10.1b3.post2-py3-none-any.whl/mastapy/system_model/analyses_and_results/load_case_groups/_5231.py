'''_5231.py

AbstractStaticLoadCaseGroup
'''


from typing import Callable, List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.system_model.analyses_and_results.load_case_groups import (
    _5242, _5241, _5229, _5240,
    _5230
)
from mastapy.system_model.analyses_and_results.static_loads import (
    _6181, _6051, _6163, _6162,
    _6088, _6090, _6092, _6133
)
from mastapy.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import _5244, _5247, _5248
from mastapy.system_model.part_model import (
    _1982, _2010, _2009, _1998
)
from mastapy.system_model.part_model.gears import _2062, _2061
from mastapy.system_model.connections_and_sockets.gears import _1868
from mastapy.system_model.analyses_and_results.power_flows.compound import _3382
from mastapy._internal.python_net import python_net_import

_ABSTRACT_STATIC_LOAD_CASE_GROUP = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups', 'AbstractStaticLoadCaseGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractStaticLoadCaseGroup',)


class AbstractStaticLoadCaseGroup(_5230.AbstractLoadCaseGroup):
    '''AbstractStaticLoadCaseGroup

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_STATIC_LOAD_CASE_GROUP

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractStaticLoadCaseGroup.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def max_number_of_load_cases_to_display(self) -> 'int':
        '''int: 'MaxNumberOfLoadCasesToDisplay' is the original name of this property.'''

        return self.wrapped.MaxNumberOfLoadCasesToDisplay

    @max_number_of_load_cases_to_display.setter
    def max_number_of_load_cases_to_display(self, value: 'int'):
        self.wrapped.MaxNumberOfLoadCasesToDisplay = int(value) if value else 0

    @property
    def clear_user_specified_excitation_data_for_all_load_cases(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ClearUserSpecifiedExcitationDataForAllLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ClearUserSpecifiedExcitationDataForAllLoadCases

    @property
    def run_power_flow(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'RunPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RunPowerFlow

    @property
    def set_face_widths_for_specified_safety_factors_from_power_flow(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'SetFaceWidthsForSpecifiedSafetyFactorsFromPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SetFaceWidthsForSpecifiedSafetyFactorsFromPowerFlow

    @property
    def calculate_candidates(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'CalculateCandidates' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateCandidates

    @property
    def number_of_possible_system_designs(self) -> 'int':
        '''int: 'NumberOfPossibleSystemDesigns' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfPossibleSystemDesigns

    @property
    def perform_system_optimisation(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'PerformSystemOptimisation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PerformSystemOptimisation

    @property
    def create_designs(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'CreateDesigns' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CreateDesigns

    @property
    def optimise_gear_sets_quick(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'OptimiseGearSetsQuick' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OptimiseGearSetsQuick

    @property
    def system_optimiser_log(self) -> 'str':
        '''str: 'SystemOptimiserLog' is the original name of this property.'''

        return self.wrapped.SystemOptimiserLog

    @system_optimiser_log.setter
    def system_optimiser_log(self, value: 'str'):
        self.wrapped.SystemOptimiserLog = str(value) if value else None

    @property
    def optimum_tooth_numbers_target(self) -> '_5242.SystemOptimiserTargets':
        '''SystemOptimiserTargets: 'OptimumToothNumbersTarget' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.OptimumToothNumbersTarget)
        return constructor.new(_5242.SystemOptimiserTargets)(value) if value else None

    @optimum_tooth_numbers_target.setter
    def optimum_tooth_numbers_target(self, value: '_5242.SystemOptimiserTargets'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.OptimumToothNumbersTarget = value

    @property
    def gear_set_optimisation(self) -> '_5241.SystemOptimiserGearSetOptimisation':
        '''SystemOptimiserGearSetOptimisation: 'GearSetOptimisation' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.GearSetOptimisation)
        return constructor.new(_5241.SystemOptimiserGearSetOptimisation)(value) if value else None

    @gear_set_optimisation.setter
    def gear_set_optimisation(self, value: '_5241.SystemOptimiserGearSetOptimisation'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.GearSetOptimisation = value

    @property
    def number_of_configurations_to_create(self) -> 'int':
        '''int: 'NumberOfConfigurationsToCreate' is the original name of this property.'''

        return self.wrapped.NumberOfConfigurationsToCreate

    @number_of_configurations_to_create.setter
    def number_of_configurations_to_create(self, value: 'int'):
        self.wrapped.NumberOfConfigurationsToCreate = int(value) if value else 0

    @property
    def static_loads(self) -> 'List[_6181.StaticLoadCase]':
        '''List[StaticLoadCase]: 'StaticLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StaticLoads, constructor.new(_6181.StaticLoadCase))
        return value

    @property
    def static_loads_limited_by_max_number_of_load_cases_to_display(self) -> 'List[_6181.StaticLoadCase]':
        '''List[StaticLoadCase]: 'StaticLoadsLimitedByMaxNumberOfLoadCasesToDisplay' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StaticLoadsLimitedByMaxNumberOfLoadCasesToDisplay, constructor.new(_6181.StaticLoadCase))
        return value

    @property
    def bearings(self) -> 'List[_5244.ComponentStaticLoadCaseGroup[_1982.Bearing, _6051.BearingLoadCase]]':
        '''List[ComponentStaticLoadCaseGroup[Bearing, BearingLoadCase]]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_5244.ComponentStaticLoadCaseGroup)[_1982.Bearing, _6051.BearingLoadCase])
        return value

    @property
    def power_loads(self) -> 'List[_5244.ComponentStaticLoadCaseGroup[_2010.PowerLoad, _6163.PowerLoadLoadCase]]':
        '''List[ComponentStaticLoadCaseGroup[PowerLoad, PowerLoadLoadCase]]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_5244.ComponentStaticLoadCaseGroup)[_2010.PowerLoad, _6163.PowerLoadLoadCase])
        return value

    @property
    def point_loads(self) -> 'List[_5244.ComponentStaticLoadCaseGroup[_2009.PointLoad, _6162.PointLoadLoadCase]]':
        '''List[ComponentStaticLoadCaseGroup[PointLoad, PointLoadLoadCase]]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_5244.ComponentStaticLoadCaseGroup)[_2009.PointLoad, _6162.PointLoadLoadCase])
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_5247.GearSetStaticLoadCaseGroup[_2062.CylindricalGearSet, _2061.CylindricalGear, _6088.CylindricalGearLoadCase, _1868.CylindricalGearMesh, _6090.CylindricalGearMeshLoadCase, _6092.CylindricalGearSetLoadCase]]':
        '''List[GearSetStaticLoadCaseGroup[CylindricalGearSet, CylindricalGear, CylindricalGearLoadCase, CylindricalGearMesh, CylindricalGearMeshLoadCase, CylindricalGearSetLoadCase]]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_5247.GearSetStaticLoadCaseGroup)[_2062.CylindricalGearSet, _2061.CylindricalGear, _6088.CylindricalGearLoadCase, _1868.CylindricalGearMesh, _6090.CylindricalGearMeshLoadCase, _6092.CylindricalGearSetLoadCase])
        return value

    @property
    def parts_with_excitations(self) -> 'List[_5248.PartStaticLoadCaseGroup]':
        '''List[PartStaticLoadCaseGroup]: 'PartsWithExcitations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartsWithExcitations, constructor.new(_5248.PartStaticLoadCaseGroup))
        return value

    @property
    def fe_components(self) -> 'List[_5244.ComponentStaticLoadCaseGroup[_1998.ImportedFEComponent, _6133.ImportedFEComponentLoadCase]]':
        '''List[ComponentStaticLoadCaseGroup[ImportedFEComponent, ImportedFEComponentLoadCase]]: 'FEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEComponents, constructor.new(_5244.ComponentStaticLoadCaseGroup)[_1998.ImportedFEComponent, _6133.ImportedFEComponentLoadCase])
        return value

    @property
    def design_states(self) -> 'List[_5229.AbstractDesignStateLoadCaseGroup]':
        '''List[AbstractDesignStateLoadCaseGroup]: 'DesignStates' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.DesignStates, constructor.new(_5229.AbstractDesignStateLoadCaseGroup))
        return value

    @property
    def loaded_gear_sets(self) -> 'List[_3382.CylindricalGearSetCompoundPowerFlow]':
        '''List[CylindricalGearSetCompoundPowerFlow]: 'LoadedGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadedGearSets, constructor.new(_3382.CylindricalGearSetCompoundPowerFlow))
        return value

    @property
    def system_optimisation_gear_sets(self) -> 'List[_5240.SystemOptimisationGearSet]':
        '''List[SystemOptimisationGearSet]: 'SystemOptimisationGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SystemOptimisationGearSets, constructor.new(_5240.SystemOptimisationGearSet))
        return value
