'''_3542.py

RootAssemblyParametricStudyTool
'''


from mastapy.system_model.part_model import _1992
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3525, _3445
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'RootAssemblyParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyParametricStudyTool',)


class RootAssemblyParametricStudyTool(_3445.AssemblyParametricStudyTool):
    '''RootAssemblyParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblyParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1992.RootAssembly':
        '''RootAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1992.RootAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def parametric_study_tool_inputs(self) -> '_3525.ParametricStudyTool':
        '''ParametricStudyTool: 'ParametricStudyToolInputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3525.ParametricStudyTool)(self.wrapped.ParametricStudyToolInputs) if self.wrapped.ParametricStudyToolInputs else None
