﻿'''_5879.py

SynchroniserDynamicAnalysis
'''


from mastapy.system_model.part_model.couplings import _2112
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6171
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5864
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'SynchroniserDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserDynamicAnalysis',)


class SynchroniserDynamicAnalysis(_5864.SpecialisedAssemblyDynamicAnalysis):
    '''SynchroniserDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2112.Synchroniser':
        '''Synchroniser: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2112.Synchroniser)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6171.SynchroniserLoadCase':
        '''SynchroniserLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6171.SynchroniserLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
