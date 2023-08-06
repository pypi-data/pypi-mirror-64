'''_5736.py

SpringDamperCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2110
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5348
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5677
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'SpringDamperCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperCompoundGearWhineAnalysis',)


class SpringDamperCompoundGearWhineAnalysis(_5677.CouplingCompoundGearWhineAnalysis):
    '''SpringDamperCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2110.SpringDamper':
        '''SpringDamper: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2110.SpringDamper)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2110.SpringDamper':
        '''SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2110.SpringDamper)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5348.SpringDamperGearWhineAnalysis]':
        '''List[SpringDamperGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5348.SpringDamperGearWhineAnalysis))
        return value

    @property
    def assembly_gear_whine_analysis_load_cases(self) -> 'List[_5348.SpringDamperGearWhineAnalysis]':
        '''List[SpringDamperGearWhineAnalysis]: 'AssemblyGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyGearWhineAnalysisLoadCases, constructor.new(_5348.SpringDamperGearWhineAnalysis))
        return value
