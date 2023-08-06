﻿'''_4754.py

OilSealModalAnalysis
'''


from mastapy.system_model.part_model import _1985
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6130
from mastapy.system_model.analyses_and_results.system_deflections import _2268
from mastapy.system_model.analyses_and_results.modal_analyses import _4710
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'OilSealModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealModalAnalysis',)


class OilSealModalAnalysis(_4710.ConnectorModalAnalysis):
    '''OilSealModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1985.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1985.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6130.OilSealLoadCase':
        '''OilSealLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6130.OilSealLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2268.OilSealSystemDeflection':
        '''OilSealSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2268.OilSealSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
