'''_5252.py

CoaxialConnectionGearWhineAnalysis
'''


from mastapy.system_model.connections_and_sockets import _1811
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6047
from mastapy.system_model.analyses_and_results.system_deflections import _2206
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5340
from mastapy._internal.python_net import python_net_import

_COAXIAL_CONNECTION_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'CoaxialConnectionGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CoaxialConnectionGearWhineAnalysis',)


class CoaxialConnectionGearWhineAnalysis(_5340.ShaftToMountableComponentConnectionGearWhineAnalysis):
    '''CoaxialConnectionGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _COAXIAL_CONNECTION_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CoaxialConnectionGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1811.CoaxialConnection':
        '''CoaxialConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1811.CoaxialConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6047.CoaxialConnectionLoadCase':
        '''CoaxialConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6047.CoaxialConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def system_deflection_results(self) -> '_2206.CoaxialConnectionSystemDeflection':
        '''CoaxialConnectionSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2206.CoaxialConnectionSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
