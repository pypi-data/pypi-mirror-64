﻿'''_2432.py

StraightBevelDiffGearSetCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2062
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2430, _2431, _2348
from mastapy.system_model.analyses_and_results.system_deflections import _2295
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'StraightBevelDiffGearSetCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetCompoundSystemDeflection',)


class StraightBevelDiffGearSetCompoundSystemDeflection(_2348.BevelGearSetCompoundSystemDeflection):
    '''StraightBevelDiffGearSetCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2062.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2062.StraightBevelDiffGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2062.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2062.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def straight_bevel_diff_gears_compound_system_deflection(self) -> 'List[_2430.StraightBevelDiffGearCompoundSystemDeflection]':
        '''List[StraightBevelDiffGearCompoundSystemDeflection]: 'StraightBevelDiffGearsCompoundSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsCompoundSystemDeflection, constructor.new(_2430.StraightBevelDiffGearCompoundSystemDeflection))
        return value

    @property
    def straight_bevel_diff_meshes_compound_system_deflection(self) -> 'List[_2431.StraightBevelDiffGearMeshCompoundSystemDeflection]':
        '''List[StraightBevelDiffGearMeshCompoundSystemDeflection]: 'StraightBevelDiffMeshesCompoundSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesCompoundSystemDeflection, constructor.new(_2431.StraightBevelDiffGearMeshCompoundSystemDeflection))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_2295.StraightBevelDiffGearSetSystemDeflection]':
        '''List[StraightBevelDiffGearSetSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2295.StraightBevelDiffGearSetSystemDeflection))
        return value

    @property
    def assembly_system_deflection_load_cases(self) -> 'List[_2295.StraightBevelDiffGearSetSystemDeflection]':
        '''List[StraightBevelDiffGearSetSystemDeflection]: 'AssemblySystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionLoadCases, constructor.new(_2295.StraightBevelDiffGearSetSystemDeflection))
        return value
