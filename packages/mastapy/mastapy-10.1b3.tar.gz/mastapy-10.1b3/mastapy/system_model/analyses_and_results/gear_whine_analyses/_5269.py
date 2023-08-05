'''_5269.py

CVTBeltConnectionGearWhineAnalysis
'''


from mastapy.system_model.connections_and_sockets import _1815
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2224
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5237
from mastapy._internal.python_net import python_net_import

_CVT_BELT_CONNECTION_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'CVTBeltConnectionGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTBeltConnectionGearWhineAnalysis',)


class CVTBeltConnectionGearWhineAnalysis(_5237.BeltConnectionGearWhineAnalysis):
    '''CVTBeltConnectionGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_BELT_CONNECTION_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTBeltConnectionGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1815.CVTBeltConnection':
        '''CVTBeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1815.CVTBeltConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def system_deflection_results(self) -> '_2224.CVTBeltConnectionSystemDeflection':
        '''CVTBeltConnectionSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2224.CVTBeltConnectionSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
