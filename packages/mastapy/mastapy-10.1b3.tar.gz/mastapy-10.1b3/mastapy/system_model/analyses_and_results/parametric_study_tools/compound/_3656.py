'''_3656.py

PlanetCarrierCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _1987
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3535
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3648
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'PlanetCarrierCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierCompoundParametricStudyTool',)


class PlanetCarrierCompoundParametricStudyTool(_3648.MountableComponentCompoundParametricStudyTool):
    '''PlanetCarrierCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1987.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1987.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3535.PlanetCarrierParametricStudyTool]':
        '''List[PlanetCarrierParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3535.PlanetCarrierParametricStudyTool))
        return value

    @property
    def component_parametric_study_tool_load_cases(self) -> 'List[_3535.PlanetCarrierParametricStudyTool]':
        '''List[PlanetCarrierParametricStudyTool]: 'ComponentParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentParametricStudyToolLoadCases, constructor.new(_3535.PlanetCarrierParametricStudyTool))
        return value
