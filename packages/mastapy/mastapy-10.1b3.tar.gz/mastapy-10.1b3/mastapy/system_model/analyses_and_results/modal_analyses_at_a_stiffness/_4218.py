﻿'''_4218.py

ConceptGearSetModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model.gears import _2038
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6054
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4217, _4216, _4243
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'ConceptGearSetModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetModalAnalysisAtAStiffness',)


class ConceptGearSetModalAnalysisAtAStiffness(_4243.GearSetModalAnalysisAtAStiffness):
    '''ConceptGearSetModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2038.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2038.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6054.ConceptGearSetLoadCase':
        '''ConceptGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6054.ConceptGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def concept_gears_modal_analysis_at_a_stiffness(self) -> 'List[_4217.ConceptGearModalAnalysisAtAStiffness]':
        '''List[ConceptGearModalAnalysisAtAStiffness]: 'ConceptGearsModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsModalAnalysisAtAStiffness, constructor.new(_4217.ConceptGearModalAnalysisAtAStiffness))
        return value

    @property
    def concept_meshes_modal_analysis_at_a_stiffness(self) -> 'List[_4216.ConceptGearMeshModalAnalysisAtAStiffness]':
        '''List[ConceptGearMeshModalAnalysisAtAStiffness]: 'ConceptMeshesModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesModalAnalysisAtAStiffness, constructor.new(_4216.ConceptGearMeshModalAnalysisAtAStiffness))
        return value
