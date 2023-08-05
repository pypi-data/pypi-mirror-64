﻿'''_5407.py

CoaxialConnectionSingleMeshWhineAnalysis
'''


from mastapy.system_model.connections_and_sockets import _1811
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6047
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5475
from mastapy._internal.python_net import python_net_import

_COAXIAL_CONNECTION_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'CoaxialConnectionSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CoaxialConnectionSingleMeshWhineAnalysis',)


class CoaxialConnectionSingleMeshWhineAnalysis(_5475.ShaftToMountableComponentConnectionSingleMeshWhineAnalysis):
    '''CoaxialConnectionSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _COAXIAL_CONNECTION_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CoaxialConnectionSingleMeshWhineAnalysis.TYPE'):
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
