﻿'''_5461.py

HypoidGearSetSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2071
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6132
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5462, _5460, _5408
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'HypoidGearSetSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetSingleMeshWhineAnalysis',)


class HypoidGearSetSingleMeshWhineAnalysis(_5408.AGMAGleasonConicalGearSetSingleMeshWhineAnalysis):
    '''HypoidGearSetSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2071.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2071.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6132.HypoidGearSetLoadCase':
        '''HypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6132.HypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def hypoid_gears_single_mesh_whine_analysis(self) -> 'List[_5462.HypoidGearSingleMeshWhineAnalysis]':
        '''List[HypoidGearSingleMeshWhineAnalysis]: 'HypoidGearsSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsSingleMeshWhineAnalysis, constructor.new(_5462.HypoidGearSingleMeshWhineAnalysis))
        return value

    @property
    def hypoid_meshes_single_mesh_whine_analysis(self) -> 'List[_5460.HypoidGearMeshSingleMeshWhineAnalysis]':
        '''List[HypoidGearMeshSingleMeshWhineAnalysis]: 'HypoidMeshesSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesSingleMeshWhineAnalysis, constructor.new(_5460.HypoidGearMeshSingleMeshWhineAnalysis))
        return value
