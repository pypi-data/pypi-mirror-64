'''_5393.py

ZerolBevelGearMeshGearWhineAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _1890
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6210
from mastapy.system_model.analyses_and_results.system_deflections import _2340
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5265
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_MESH_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'ZerolBevelGearMeshGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearMeshGearWhineAnalysis',)


class ZerolBevelGearMeshGearWhineAnalysis(_5265.BevelGearMeshGearWhineAnalysis):
    '''ZerolBevelGearMeshGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_MESH_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearMeshGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1890.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1890.ZerolBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6210.ZerolBevelGearMeshLoadCase':
        '''ZerolBevelGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6210.ZerolBevelGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def system_deflection_results(self) -> '_2340.ZerolBevelGearMeshSystemDeflection':
        '''ZerolBevelGearMeshSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2340.ZerolBevelGearMeshSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
