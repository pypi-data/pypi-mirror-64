'''_2413.py

PowerLoadCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _1990
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2276
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2447
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'PowerLoadCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadCompoundSystemDeflection',)


class PowerLoadCompoundSystemDeflection(_2447.VirtualComponentCompoundSystemDeflection):
    '''PowerLoadCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _POWER_LOAD_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerLoadCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1990.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1990.PowerLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2276.PowerLoadSystemDeflection]':
        '''List[PowerLoadSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2276.PowerLoadSystemDeflection))
        return value

    @property
    def component_system_deflection_load_cases(self) -> 'List[_2276.PowerLoadSystemDeflection]':
        '''List[PowerLoadSystemDeflection]: 'ComponentSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionLoadCases, constructor.new(_2276.PowerLoadSystemDeflection))
        return value
