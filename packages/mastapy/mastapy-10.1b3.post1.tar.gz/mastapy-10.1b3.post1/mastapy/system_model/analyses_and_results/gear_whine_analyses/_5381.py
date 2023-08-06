'''_5381.py

SynchroniserSleeveGearWhineAnalysis
'''


from mastapy.system_model.part_model.couplings import _2136
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6193
from mastapy.system_model.analyses_and_results.system_deflections import _2324
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5380
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_SLEEVE_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'SynchroniserSleeveGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserSleeveGearWhineAnalysis',)


class SynchroniserSleeveGearWhineAnalysis(_5380.SynchroniserPartGearWhineAnalysis):
    '''SynchroniserSleeveGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_SLEEVE_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserSleeveGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2136.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2136.SynchroniserSleeve)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6193.SynchroniserSleeveLoadCase':
        '''SynchroniserSleeveLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6193.SynchroniserSleeveLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2324.SynchroniserSleeveSystemDeflection':
        '''SynchroniserSleeveSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2324.SynchroniserSleeveSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
