'''_2305.py

SynchroniserSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2112
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6171
from mastapy.system_model.analyses_and_results.power_flows import _3303
from mastapy.system_model.analyses_and_results.system_deflections import _2302, _2287
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'SynchroniserSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserSystemDeflection',)


class SynchroniserSystemDeflection(_2287.SpecialisedAssemblySystemDeflection):
    '''SynchroniserSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserSystemDeflection.TYPE'):
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

    @property
    def power_flow_results(self) -> '_3303.SynchroniserPowerFlow':
        '''SynchroniserPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3303.SynchroniserPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def cones(self) -> 'List[_2302.SynchroniserHalfSystemDeflection]':
        '''List[SynchroniserHalfSystemDeflection]: 'Cones' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Cones, constructor.new(_2302.SynchroniserHalfSystemDeflection))
        return value
