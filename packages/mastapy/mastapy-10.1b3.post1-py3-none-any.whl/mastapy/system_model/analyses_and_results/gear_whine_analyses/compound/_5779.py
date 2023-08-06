﻿'''_5779.py

WormGearSetCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2088
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5777, _5778, _5715
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5391
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'WormGearSetCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetCompoundGearWhineAnalysis',)


class WormGearSetCompoundGearWhineAnalysis(_5715.GearSetCompoundGearWhineAnalysis):
    '''WormGearSetCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2088.WormGearSet':
        '''WormGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2088.WormGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2088.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2088.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def worm_gears_compound_gear_whine_analysis(self) -> 'List[_5777.WormGearCompoundGearWhineAnalysis]':
        '''List[WormGearCompoundGearWhineAnalysis]: 'WormGearsCompoundGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsCompoundGearWhineAnalysis, constructor.new(_5777.WormGearCompoundGearWhineAnalysis))
        return value

    @property
    def worm_meshes_compound_gear_whine_analysis(self) -> 'List[_5778.WormGearMeshCompoundGearWhineAnalysis]':
        '''List[WormGearMeshCompoundGearWhineAnalysis]: 'WormMeshesCompoundGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesCompoundGearWhineAnalysis, constructor.new(_5778.WormGearMeshCompoundGearWhineAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5391.WormGearSetGearWhineAnalysis]':
        '''List[WormGearSetGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5391.WormGearSetGearWhineAnalysis))
        return value

    @property
    def assembly_gear_whine_analysis_load_cases(self) -> 'List[_5391.WormGearSetGearWhineAnalysis]':
        '''List[WormGearSetGearWhineAnalysis]: 'AssemblyGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyGearWhineAnalysisLoadCases, constructor.new(_5391.WormGearSetGearWhineAnalysis))
        return value
