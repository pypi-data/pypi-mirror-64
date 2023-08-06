'''_3499.py

CVTParametricStudyTool
'''


from mastapy.system_model.part_model.couplings import _2117
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3468
from mastapy._internal.python_net import python_net_import

_CVT_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'CVTParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTParametricStudyTool',)


class CVTParametricStudyTool(_3468.BeltDriveParametricStudyTool):
    '''CVTParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _CVT_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2117.CVT':
        '''CVT: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2117.CVT)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None
