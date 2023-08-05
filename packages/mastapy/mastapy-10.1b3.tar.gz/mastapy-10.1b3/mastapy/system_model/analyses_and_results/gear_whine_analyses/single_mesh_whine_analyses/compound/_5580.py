﻿'''_5580.py

OilSealCompoundSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _1985
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5458
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import _5542
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'OilSealCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealCompoundSingleMeshWhineAnalysis',)


class OilSealCompoundSingleMeshWhineAnalysis(_5542.ConnectorCompoundSingleMeshWhineAnalysis):
    '''OilSealCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1985.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1985.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5458.OilSealSingleMeshWhineAnalysis]':
        '''List[OilSealSingleMeshWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5458.OilSealSingleMeshWhineAnalysis))
        return value

    @property
    def component_single_mesh_whine_analysis_load_cases(self) -> 'List[_5458.OilSealSingleMeshWhineAnalysis]':
        '''List[OilSealSingleMeshWhineAnalysis]: 'ComponentSingleMeshWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSingleMeshWhineAnalysisLoadCases, constructor.new(_5458.OilSealSingleMeshWhineAnalysis))
        return value
