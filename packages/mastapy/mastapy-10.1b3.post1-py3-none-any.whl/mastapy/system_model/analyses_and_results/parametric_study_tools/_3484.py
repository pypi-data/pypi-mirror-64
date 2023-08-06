'''_3484.py

ConceptCouplingConnectionParametricStudyTool
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _1894
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6069
from mastapy.system_model.analyses_and_results.system_deflections import _2229
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3495
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_CONNECTION_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'ConceptCouplingConnectionParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingConnectionParametricStudyTool',)


class ConceptCouplingConnectionParametricStudyTool(_3495.CouplingConnectionParametricStudyTool):
    '''ConceptCouplingConnectionParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_CONNECTION_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingConnectionParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1894.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1894.ConceptCouplingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6069.ConceptCouplingConnectionLoadCase':
        '''ConceptCouplingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6069.ConceptCouplingConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def connection_system_deflection_results(self) -> 'List[_2229.ConceptCouplingConnectionSystemDeflection]':
        '''List[ConceptCouplingConnectionSystemDeflection]: 'ConnectionSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionResults, constructor.new(_2229.ConceptCouplingConnectionSystemDeflection))
        return value
