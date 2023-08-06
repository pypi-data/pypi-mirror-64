'''_5277.py

ConceptCouplingHalfGearWhineAnalysis
'''


from mastapy.system_model.part_model.couplings import _2114
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6070
from mastapy.system_model.analyses_and_results.system_deflections import _2230
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5288
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_HALF_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'ConceptCouplingHalfGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingHalfGearWhineAnalysis',)


class ConceptCouplingHalfGearWhineAnalysis(_5288.CouplingHalfGearWhineAnalysis):
    '''ConceptCouplingHalfGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_HALF_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingHalfGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2114.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2114.ConceptCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6070.ConceptCouplingHalfLoadCase':
        '''ConceptCouplingHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6070.ConceptCouplingHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2230.ConceptCouplingHalfSystemDeflection':
        '''ConceptCouplingHalfSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2230.ConceptCouplingHalfSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
