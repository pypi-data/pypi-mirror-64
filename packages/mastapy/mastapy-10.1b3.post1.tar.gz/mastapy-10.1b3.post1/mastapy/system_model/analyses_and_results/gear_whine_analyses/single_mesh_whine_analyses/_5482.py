'''_5482.py

PartToPartShearCouplingSingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model.couplings import _2119
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6155
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5442
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'PartToPartShearCouplingSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingSingleMeshWhineAnalysis',)


class PartToPartShearCouplingSingleMeshWhineAnalysis(_5442.CouplingSingleMeshWhineAnalysis):
    '''PartToPartShearCouplingSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2119.PartToPartShearCoupling':
        '''PartToPartShearCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2119.PartToPartShearCoupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6155.PartToPartShearCouplingLoadCase':
        '''PartToPartShearCouplingLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6155.PartToPartShearCouplingLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
