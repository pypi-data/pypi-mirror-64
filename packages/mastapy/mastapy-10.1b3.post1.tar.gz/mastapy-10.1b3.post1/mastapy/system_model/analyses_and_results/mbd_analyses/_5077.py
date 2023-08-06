'''_5077.py

StraightBevelDiffGearSetMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2082
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6184
from mastapy.system_model.analyses_and_results.mbd_analyses import _5076, _5075, _4981
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'StraightBevelDiffGearSetMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetMultiBodyDynamicsAnalysis',)


class StraightBevelDiffGearSetMultiBodyDynamicsAnalysis(_4981.BevelGearSetMultiBodyDynamicsAnalysis):
    '''StraightBevelDiffGearSetMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2082.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2082.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6184.StraightBevelDiffGearSetLoadCase':
        '''StraightBevelDiffGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6184.StraightBevelDiffGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def gears(self) -> 'List[_5076.StraightBevelDiffGearMultiBodyDynamicsAnalysis]':
        '''List[StraightBevelDiffGearMultiBodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_5076.StraightBevelDiffGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def straight_bevel_diff_gears_multi_body_dynamics_analysis(self) -> 'List[_5076.StraightBevelDiffGearMultiBodyDynamicsAnalysis]':
        '''List[StraightBevelDiffGearMultiBodyDynamicsAnalysis]: 'StraightBevelDiffGearsMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsMultiBodyDynamicsAnalysis, constructor.new(_5076.StraightBevelDiffGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def straight_bevel_diff_meshes_multi_body_dynamics_analysis(self) -> 'List[_5075.StraightBevelDiffGearMeshMultiBodyDynamicsAnalysis]':
        '''List[StraightBevelDiffGearMeshMultiBodyDynamicsAnalysis]: 'StraightBevelDiffMeshesMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesMultiBodyDynamicsAnalysis, constructor.new(_5075.StraightBevelDiffGearMeshMultiBodyDynamicsAnalysis))
        return value
