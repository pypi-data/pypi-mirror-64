'''_6314.py

PointLoadAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2009
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6162
from mastapy.system_model.analyses_and_results.system_deflections import _2295
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6350
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'PointLoadAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadAdvancedSystemDeflection',)


class PointLoadAdvancedSystemDeflection(_6350.VirtualComponentAdvancedSystemDeflection):
    '''PointLoadAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2009.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2009.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6162.PointLoadLoadCase':
        '''PointLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6162.PointLoadLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2295.PointLoadSystemDeflection]':
        '''List[PointLoadSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2295.PointLoadSystemDeflection))
        return value
