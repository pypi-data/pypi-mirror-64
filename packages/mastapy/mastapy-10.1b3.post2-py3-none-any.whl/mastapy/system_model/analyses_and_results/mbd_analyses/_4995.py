'''_4995.py

FaceGearSetMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2045
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6092
from mastapy.system_model.analyses_and_results.mbd_analyses import _4994, _4993, _5000
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'FaceGearSetMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetMultiBodyDynamicsAnalysis',)


class FaceGearSetMultiBodyDynamicsAnalysis(_5000.GearSetMultiBodyDynamicsAnalysis):
    '''FaceGearSetMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2045.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2045.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6092.FaceGearSetLoadCase':
        '''FaceGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6092.FaceGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def gears(self) -> 'List[_4994.FaceGearMultiBodyDynamicsAnalysis]':
        '''List[FaceGearMultiBodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_4994.FaceGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def face_gears_multi_body_dynamics_analysis(self) -> 'List[_4994.FaceGearMultiBodyDynamicsAnalysis]':
        '''List[FaceGearMultiBodyDynamicsAnalysis]: 'FaceGearsMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsMultiBodyDynamicsAnalysis, constructor.new(_4994.FaceGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def face_meshes_multi_body_dynamics_analysis(self) -> 'List[_4993.FaceGearMeshMultiBodyDynamicsAnalysis]':
        '''List[FaceGearMeshMultiBodyDynamicsAnalysis]: 'FaceMeshesMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesMultiBodyDynamicsAnalysis, constructor.new(_4993.FaceGearMeshMultiBodyDynamicsAnalysis))
        return value
