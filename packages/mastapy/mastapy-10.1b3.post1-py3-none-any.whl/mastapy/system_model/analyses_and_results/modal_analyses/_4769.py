'''_4769.py

ModalAnalysis
'''


from mastapy.system_model.analyses_and_results.dynamic_analyses import _5838
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses import _4772, _4770
from mastapy.system_model.analyses_and_results.analysis_cases import _6493
from mastapy._internal.python_net import python_net_import

_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'ModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ModalAnalysis',)


class ModalAnalysis(_6493.StaticLoadAnalysisCase):
    '''ModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def modal_analysis_results(self) -> '_5838.DynamicAnalysis':
        '''DynamicAnalysis: 'ModalAnalysisResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5838.DynamicAnalysis)(self.wrapped.ModalAnalysisResults) if self.wrapped.ModalAnalysisResults else None

    @property
    def analysis_settings(self) -> '_4772.ModalAnalysisOptions':
        '''ModalAnalysisOptions: 'AnalysisSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4772.ModalAnalysisOptions)(self.wrapped.AnalysisSettings) if self.wrapped.AnalysisSettings else None

    @property
    def bar_model_export(self) -> '_4770.ModalAnalysisBarModelFEExportOptions':
        '''ModalAnalysisBarModelFEExportOptions: 'BarModelExport' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4770.ModalAnalysisBarModelFEExportOptions)(self.wrapped.BarModelExport) if self.wrapped.BarModelExport else None
