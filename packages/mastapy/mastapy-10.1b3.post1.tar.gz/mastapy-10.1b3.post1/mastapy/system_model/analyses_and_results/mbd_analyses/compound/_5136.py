﻿'''_5136.py

ConceptGearMeshCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1864
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _4993
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5160
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_MESH_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'ConceptGearMeshCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearMeshCompoundMultiBodyDynamicsAnalysis',)


class ConceptGearMeshCompoundMultiBodyDynamicsAnalysis(_5160.GearMeshCompoundMultiBodyDynamicsAnalysis):
    '''ConceptGearMeshCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_MESH_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearMeshCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1864.ConceptGearMesh':
        '''ConceptGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1864.ConceptGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1864.ConceptGearMesh':
        '''ConceptGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1864.ConceptGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4993.ConceptGearMeshMultiBodyDynamicsAnalysis]':
        '''List[ConceptGearMeshMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4993.ConceptGearMeshMultiBodyDynamicsAnalysis))
        return value

    @property
    def connection_multi_body_dynamics_analysis_load_cases(self) -> 'List[_4993.ConceptGearMeshMultiBodyDynamicsAnalysis]':
        '''List[ConceptGearMeshMultiBodyDynamicsAnalysis]: 'ConnectionMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionMultiBodyDynamicsAnalysisLoadCases, constructor.new(_4993.ConceptGearMeshMultiBodyDynamicsAnalysis))
        return value
