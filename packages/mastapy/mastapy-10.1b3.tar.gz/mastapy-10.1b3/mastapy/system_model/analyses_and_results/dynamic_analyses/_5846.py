﻿'''_5846.py

OilSealDynamicAnalysis
'''


from mastapy.system_model.part_model import _1985
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6130
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5806
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'OilSealDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealDynamicAnalysis',)


class OilSealDynamicAnalysis(_5806.ConnectorDynamicAnalysis):
    '''OilSealDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealDynamicAnalysis.TYPE'):
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
