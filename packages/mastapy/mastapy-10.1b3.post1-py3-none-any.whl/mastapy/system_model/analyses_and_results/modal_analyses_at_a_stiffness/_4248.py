'''_4248.py

CVTModalAnalysisAtAStiffness
'''


from mastapy.system_model.part_model.couplings import _2117
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4217
from mastapy._internal.python_net import python_net_import

_CVT_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'CVTModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTModalAnalysisAtAStiffness',)


class CVTModalAnalysisAtAStiffness(_4217.BeltDriveModalAnalysisAtAStiffness):
    '''CVTModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _CVT_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2117.CVT':
        '''CVT: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2117.CVT)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None
