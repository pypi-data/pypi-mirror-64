﻿'''_5914.py

ZerolBevelGearSetDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2090
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6211
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5912, _5913, _5808
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'ZerolBevelGearSetDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetDynamicAnalysis',)


class ZerolBevelGearSetDynamicAnalysis(_5808.BevelGearSetDynamicAnalysis):
    '''ZerolBevelGearSetDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2090.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2090.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6211.ZerolBevelGearSetLoadCase':
        '''ZerolBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6211.ZerolBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def zerol_bevel_gears_dynamic_analysis(self) -> 'List[_5912.ZerolBevelGearDynamicAnalysis]':
        '''List[ZerolBevelGearDynamicAnalysis]: 'ZerolBevelGearsDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsDynamicAnalysis, constructor.new(_5912.ZerolBevelGearDynamicAnalysis))
        return value

    @property
    def zerol_bevel_meshes_dynamic_analysis(self) -> 'List[_5913.ZerolBevelGearMeshDynamicAnalysis]':
        '''List[ZerolBevelGearMeshDynamicAnalysis]: 'ZerolBevelMeshesDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesDynamicAnalysis, constructor.new(_5913.ZerolBevelGearMeshDynamicAnalysis))
        return value
