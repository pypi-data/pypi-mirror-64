'''_4889.py

FaceGearCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2064
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4745
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4893
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'FaceGearCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearCompoundModalAnalysis',)


class FaceGearCompoundModalAnalysis(_4893.GearCompoundModalAnalysis):
    '''FaceGearCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2064.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2064.FaceGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4745.FaceGearModalAnalysis]':
        '''List[FaceGearModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4745.FaceGearModalAnalysis))
        return value

    @property
    def component_modal_analysis_load_cases(self) -> 'List[_4745.FaceGearModalAnalysis]':
        '''List[FaceGearModalAnalysis]: 'ComponentModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisLoadCases, constructor.new(_4745.FaceGearModalAnalysis))
        return value
