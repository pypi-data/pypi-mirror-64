﻿'''_6291.py

ImportedFEComponentAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _1998
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6133
from mastapy.system_model.analyses_and_results.system_deflections import _2271
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6230
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_COMPONENT_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'ImportedFEComponentAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEComponentAdvancedSystemDeflection',)


class ImportedFEComponentAdvancedSystemDeflection(_6230.AbstractShaftOrHousingAdvancedSystemDeflection):
    '''ImportedFEComponentAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_COMPONENT_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEComponentAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1998.ImportedFEComponent':
        '''ImportedFEComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1998.ImportedFEComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6133.ImportedFEComponentLoadCase':
        '''ImportedFEComponentLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6133.ImportedFEComponentLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[ImportedFEComponentAdvancedSystemDeflection]':
        '''List[ImportedFEComponentAdvancedSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ImportedFEComponentAdvancedSystemDeflection))
        return value

    @property
    def component_system_deflection_results(self) -> 'List[_2271.ImportedFEComponentSystemDeflection]':
        '''List[ImportedFEComponentSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2271.ImportedFEComponentSystemDeflection))
        return value
