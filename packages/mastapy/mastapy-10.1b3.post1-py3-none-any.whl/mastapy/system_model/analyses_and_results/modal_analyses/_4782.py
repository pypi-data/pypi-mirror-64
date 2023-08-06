﻿'''_4782.py

PlanetCarrierModalAnalysis
'''


from mastapy.system_model.part_model import _2007
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6159
from mastapy.system_model.analyses_and_results.system_deflections import _2294
from mastapy.system_model.analyses_and_results.modal_analyses import _4773
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'PlanetCarrierModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierModalAnalysis',)


class PlanetCarrierModalAnalysis(_4773.MountableComponentModalAnalysis):
    '''PlanetCarrierModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2007.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2007.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6159.PlanetCarrierLoadCase':
        '''PlanetCarrierLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6159.PlanetCarrierLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2294.PlanetCarrierSystemDeflection':
        '''PlanetCarrierSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2294.PlanetCarrierSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
