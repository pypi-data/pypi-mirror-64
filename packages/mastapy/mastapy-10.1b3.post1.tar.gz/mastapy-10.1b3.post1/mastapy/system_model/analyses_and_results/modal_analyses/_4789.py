﻿'''_4789.py

RootAssemblyModalAnalysis
'''


from mastapy.system_model.part_model import _2012
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses import _4769, _4701
from mastapy.system_model.analyses_and_results.system_deflections import _2301
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'RootAssemblyModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyModalAnalysis',)


class RootAssemblyModalAnalysis(_4701.AssemblyModalAnalysis):
    '''RootAssemblyModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblyModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2012.RootAssembly':
        '''RootAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2012.RootAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def modal_analysis_inputs(self) -> '_4769.ModalAnalysis':
        '''ModalAnalysis: 'ModalAnalysisInputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4769.ModalAnalysis)(self.wrapped.ModalAnalysisInputs) if self.wrapped.ModalAnalysisInputs else None

    @property
    def system_deflection_results(self) -> '_2301.RootAssemblySystemDeflection':
        '''RootAssemblySystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2301.RootAssemblySystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
