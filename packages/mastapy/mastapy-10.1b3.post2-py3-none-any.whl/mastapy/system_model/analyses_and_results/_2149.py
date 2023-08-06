'''_2149.py

SingleMeshWhineAnalysisAnalysis
'''


from mastapy.system_model.analyses_and_results.static_loads import (
    _6188, _6189, _6191, _6135,
    _6134, _6033, _6046, _6045,
    _6051, _6050, _6064, _6063,
    _6066, _6067, _6144, _6150,
    _6148, _6146, _6160, _6159,
    _6171, _6170, _6172, _6173,
    _6177, _6178, _6179, _6065,
    _6032, _6047, _6060, _6115,
    _6136, _6147, _6152, _6035,
    _6053, _6091, _6163, _6040,
    _6057, _6027, _6070, _6111,
    _6117, _6120, _6123, _6156,
    _6166, _6187, _6190, _6097,
    _6133, _6044, _6049, _6062,
    _6158, _6176, _6023, _6024,
    _6031, _6043, _6042, _6048,
    _6061, _6076, _6089, _6093,
    _6030, _6101, _6113, _6125,
    _6126, _6128, _6130, _6132,
    _6139, _6142, _6143, _6149,
    _6153, _6184, _6185, _6151,
    _6052, _6054, _6090, _6092,
    _6026, _6028, _6034, _6036,
    _6037, _6038, _6039, _6041,
    _6055, _6059, _6068, _6072,
    _6073, _6095, _6100, _6110,
    _6112, _6116, _6118, _6119,
    _6121, _6122, _6124, _6137,
    _6155, _6157, _6162, _6164,
    _6165, _6167, _6168, _6169,
    _6186
)
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import (
    _5503, _5507, _5506, _5462,
    _5461, _5393, _5406, _5405,
    _5411, _5410, _5422, _5421,
    _5425, _5424, _5468, _5473,
    _5471, _5469, _5483, _5482,
    _5494, _5492, _5493, _5495,
    _5498, _5497, _5499, _5423,
    _5392, _5407, _5418, _5444,
    _5463, _5470, _5475, _5394,
    _5412, _5432, _5484, _5399,
    _5415, _5387, _5426, _5440,
    _5445, _5448, _5451, _5478,
    _5487, _5502, _5505, _5436,
    _5460, _5404, _5409, _5420,
    _5481, _5496, _5385, _5386,
    _5391, _5403, _5402, _5408,
    _5419, _5430, _5431, _5435,
    _5390, _5439, _5443, _5454,
    _5455, _5457, _5458, _5459,
    _5465, _5466, _5467, _5472,
    _5477, _5500, _5501, _5474,
    _5414, _5413, _5434, _5433,
    _5389, _5388, _5396, _5395,
    _5397, _5398, _5401, _5400,
    _5417, _5416, _5428, _5427,
    _5429, _5438, _5437, _5442,
    _5441, _5447, _5446, _5450,
    _5449, _5453, _5452, _5464,
    _5480, _5479, _5486, _5485,
    _5489, _5488, _5490, _5491,
    _5504
)
from mastapy._internal import constructor
from mastapy.system_model.part_model.gears import (
    _2069, _2070, _2037, _2038,
    _2044, _2045, _2029, _2030,
    _2031, _2032, _2033, _2034,
    _2035, _2036, _2039, _2040,
    _2041, _2042, _2043, _2046,
    _2048, _2050, _2051, _2052,
    _2053, _2054, _2055, _2056,
    _2057, _2058, _2059, _2060,
    _2061, _2062, _2063, _2064,
    _2065, _2066, _2067, _2068
)
from mastapy.system_model.part_model.couplings import (
    _2099, _2100, _2088, _2090,
    _2091, _2093, _2094, _2095,
    _2096, _2097, _2098, _2101,
    _2109, _2107, _2108, _2110,
    _2111, _2112, _2114, _2115,
    _2116, _2117, _2118, _2120
)
from mastapy.system_model.connections_and_sockets import (
    _1815, _1810, _1811, _1814,
    _1823, _1826, _1830, _1834
)
from mastapy.system_model.connections_and_sockets.gears import (
    _1840, _1844, _1850, _1864,
    _1842, _1846, _1838, _1848,
    _1854, _1857, _1858, _1859,
    _1862, _1866, _1868, _1870,
    _1852
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _1878, _1872, _1874, _1876,
    _1880, _1882
)
from mastapy.system_model.part_model import (
    _1958, _1959, _1962, _1964,
    _1965, _1966, _1969, _1970,
    _1973, _1974, _1957, _1975,
    _1978, _1981, _1982, _1983,
    _1985, _1986, _1987, _1989,
    _1990, _1992, _1994, _1995,
    _1996
)
from mastapy.system_model.part_model.shaft_model import _1999
from mastapy.system_model.analyses_and_results import _2130
from mastapy._internal.python_net import python_net_import

_SINGLE_MESH_WHINE_ANALYSIS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'SingleMeshWhineAnalysisAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SingleMeshWhineAnalysisAnalysis',)


class SingleMeshWhineAnalysisAnalysis(_2130.SingleAnalysis):
    '''SingleMeshWhineAnalysisAnalysis

    This is a mastapy class.
    '''

    TYPE = _SINGLE_MESH_WHINE_ANALYSIS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SingleMeshWhineAnalysisAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    def results_for_worm_gear_set_load_case(self, design_entity_analysis: '_6188.WormGearSetLoadCase') -> '_5503.WormGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.WormGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5503.WormGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_zerol_bevel_gear(self, design_entity: '_2069.ZerolBevelGear') -> '_5507.ZerolBevelGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ZerolBevelGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5507.ZerolBevelGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_load_case(self, design_entity_analysis: '_6189.ZerolBevelGearLoadCase') -> '_5507.ZerolBevelGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ZerolBevelGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5507.ZerolBevelGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set(self, design_entity: '_2070.ZerolBevelGearSet') -> '_5506.ZerolBevelGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ZerolBevelGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5506.ZerolBevelGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set_load_case(self, design_entity_analysis: '_6191.ZerolBevelGearSetLoadCase') -> '_5506.ZerolBevelGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ZerolBevelGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5506.ZerolBevelGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling(self, design_entity: '_2099.PartToPartShearCoupling') -> '_5462.PartToPartShearCouplingSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.PartToPartShearCouplingSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5462.PartToPartShearCouplingSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_load_case(self, design_entity_analysis: '_6135.PartToPartShearCouplingLoadCase') -> '_5462.PartToPartShearCouplingSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.PartToPartShearCouplingSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5462.PartToPartShearCouplingSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_half(self, design_entity: '_2100.PartToPartShearCouplingHalf') -> '_5461.PartToPartShearCouplingHalfSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.PartToPartShearCouplingHalfSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5461.PartToPartShearCouplingHalfSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_half_load_case(self, design_entity_analysis: '_6134.PartToPartShearCouplingHalfLoadCase') -> '_5461.PartToPartShearCouplingHalfSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.PartToPartShearCouplingHalfSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5461.PartToPartShearCouplingHalfSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_belt_drive(self, design_entity: '_2088.BeltDrive') -> '_5393.BeltDriveSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.BeltDriveSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5393.BeltDriveSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_belt_drive_load_case(self, design_entity_analysis: '_6033.BeltDriveLoadCase') -> '_5393.BeltDriveSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltDriveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.BeltDriveSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5393.BeltDriveSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_clutch(self, design_entity: '_2090.Clutch') -> '_5406.ClutchSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ClutchSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5406.ClutchSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_clutch_load_case(self, design_entity_analysis: '_6046.ClutchLoadCase') -> '_5406.ClutchSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ClutchSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5406.ClutchSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_clutch_half(self, design_entity: '_2091.ClutchHalf') -> '_5405.ClutchHalfSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ClutchHalfSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5405.ClutchHalfSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_clutch_half_load_case(self, design_entity_analysis: '_6045.ClutchHalfLoadCase') -> '_5405.ClutchHalfSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ClutchHalfSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5405.ClutchHalfSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_concept_coupling(self, design_entity: '_2093.ConceptCoupling') -> '_5411.ConceptCouplingSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ConceptCouplingSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5411.ConceptCouplingSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_concept_coupling_load_case(self, design_entity_analysis: '_6051.ConceptCouplingLoadCase') -> '_5411.ConceptCouplingSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ConceptCouplingSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5411.ConceptCouplingSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_concept_coupling_half(self, design_entity: '_2094.ConceptCouplingHalf') -> '_5410.ConceptCouplingHalfSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ConceptCouplingHalfSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5410.ConceptCouplingHalfSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_concept_coupling_half_load_case(self, design_entity_analysis: '_6050.ConceptCouplingHalfLoadCase') -> '_5410.ConceptCouplingHalfSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ConceptCouplingHalfSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5410.ConceptCouplingHalfSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_coupling(self, design_entity: '_2095.Coupling') -> '_5422.CouplingSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.CouplingSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5422.CouplingSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_coupling_load_case(self, design_entity_analysis: '_6064.CouplingLoadCase') -> '_5422.CouplingSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.CouplingSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5422.CouplingSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_coupling_half(self, design_entity: '_2096.CouplingHalf') -> '_5421.CouplingHalfSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.CouplingHalfSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5421.CouplingHalfSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_coupling_half_load_case(self, design_entity_analysis: '_6063.CouplingHalfLoadCase') -> '_5421.CouplingHalfSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.CouplingHalfSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5421.CouplingHalfSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_cvt(self, design_entity: '_2097.CVT') -> '_5425.CVTSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.CVTSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5425.CVTSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_cvt_load_case(self, design_entity_analysis: '_6066.CVTLoadCase') -> '_5425.CVTSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.CVTSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5425.CVTSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_cvt_pulley(self, design_entity: '_2098.CVTPulley') -> '_5424.CVTPulleySingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.CVTPulleySingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5424.CVTPulleySingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_cvt_pulley_load_case(self, design_entity_analysis: '_6067.CVTPulleyLoadCase') -> '_5424.CVTPulleySingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTPulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.CVTPulleySingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5424.CVTPulleySingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_pulley(self, design_entity: '_2101.Pulley') -> '_5468.PulleySingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.PulleySingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5468.PulleySingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_pulley_load_case(self, design_entity_analysis: '_6144.PulleyLoadCase') -> '_5468.PulleySingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.PulleySingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5468.PulleySingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_shaft_hub_connection(self, design_entity: '_2109.ShaftHubConnection') -> '_5473.ShaftHubConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ShaftHubConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5473.ShaftHubConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_shaft_hub_connection_load_case(self, design_entity_analysis: '_6150.ShaftHubConnectionLoadCase') -> '_5473.ShaftHubConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ShaftHubConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5473.ShaftHubConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_rolling_ring(self, design_entity: '_2107.RollingRing') -> '_5471.RollingRingSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.RollingRingSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5471.RollingRingSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_rolling_ring_load_case(self, design_entity_analysis: '_6148.RollingRingLoadCase') -> '_5471.RollingRingSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.RollingRingSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5471.RollingRingSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_rolling_ring_assembly(self, design_entity: '_2108.RollingRingAssembly') -> '_5469.RollingRingAssemblySingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.RollingRingAssemblySingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5469.RollingRingAssemblySingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_rolling_ring_assembly_load_case(self, design_entity_analysis: '_6146.RollingRingAssemblyLoadCase') -> '_5469.RollingRingAssemblySingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.RollingRingAssemblySingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5469.RollingRingAssemblySingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_spring_damper(self, design_entity: '_2110.SpringDamper') -> '_5483.SpringDamperSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.SpringDamperSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5483.SpringDamperSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_spring_damper_load_case(self, design_entity_analysis: '_6160.SpringDamperLoadCase') -> '_5483.SpringDamperSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.SpringDamperSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5483.SpringDamperSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_spring_damper_half(self, design_entity: '_2111.SpringDamperHalf') -> '_5482.SpringDamperHalfSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.SpringDamperHalfSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5482.SpringDamperHalfSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_spring_damper_half_load_case(self, design_entity_analysis: '_6159.SpringDamperHalfLoadCase') -> '_5482.SpringDamperHalfSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.SpringDamperHalfSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5482.SpringDamperHalfSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_synchroniser(self, design_entity: '_2112.Synchroniser') -> '_5494.SynchroniserSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.SynchroniserSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5494.SynchroniserSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_synchroniser_load_case(self, design_entity_analysis: '_6171.SynchroniserLoadCase') -> '_5494.SynchroniserSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.SynchroniserSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5494.SynchroniserSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_synchroniser_half(self, design_entity: '_2114.SynchroniserHalf') -> '_5492.SynchroniserHalfSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.SynchroniserHalfSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5492.SynchroniserHalfSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_synchroniser_half_load_case(self, design_entity_analysis: '_6170.SynchroniserHalfLoadCase') -> '_5492.SynchroniserHalfSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.SynchroniserHalfSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5492.SynchroniserHalfSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_synchroniser_part(self, design_entity: '_2115.SynchroniserPart') -> '_5493.SynchroniserPartSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.SynchroniserPartSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5493.SynchroniserPartSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_synchroniser_part_load_case(self, design_entity_analysis: '_6172.SynchroniserPartLoadCase') -> '_5493.SynchroniserPartSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserPartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.SynchroniserPartSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5493.SynchroniserPartSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_synchroniser_sleeve(self, design_entity: '_2116.SynchroniserSleeve') -> '_5495.SynchroniserSleeveSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.SynchroniserSleeveSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5495.SynchroniserSleeveSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_synchroniser_sleeve_load_case(self, design_entity_analysis: '_6173.SynchroniserSleeveLoadCase') -> '_5495.SynchroniserSleeveSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserSleeveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.SynchroniserSleeveSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5495.SynchroniserSleeveSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_torque_converter(self, design_entity: '_2117.TorqueConverter') -> '_5498.TorqueConverterSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.TorqueConverterSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5498.TorqueConverterSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_torque_converter_load_case(self, design_entity_analysis: '_6177.TorqueConverterLoadCase') -> '_5498.TorqueConverterSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.TorqueConverterSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5498.TorqueConverterSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_torque_converter_pump(self, design_entity: '_2118.TorqueConverterPump') -> '_5497.TorqueConverterPumpSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.TorqueConverterPumpSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5497.TorqueConverterPumpSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_torque_converter_pump_load_case(self, design_entity_analysis: '_6178.TorqueConverterPumpLoadCase') -> '_5497.TorqueConverterPumpSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterPumpLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.TorqueConverterPumpSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5497.TorqueConverterPumpSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_torque_converter_turbine(self, design_entity: '_2120.TorqueConverterTurbine') -> '_5499.TorqueConverterTurbineSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.TorqueConverterTurbineSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5499.TorqueConverterTurbineSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_torque_converter_turbine_load_case(self, design_entity_analysis: '_6179.TorqueConverterTurbineLoadCase') -> '_5499.TorqueConverterTurbineSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterTurbineLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.TorqueConverterTurbineSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5499.TorqueConverterTurbineSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_cvt_belt_connection(self, design_entity: '_1815.CVTBeltConnection') -> '_5423.CVTBeltConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.CVTBeltConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5423.CVTBeltConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_cvt_belt_connection_load_case(self, design_entity_analysis: '_6065.CVTBeltConnectionLoadCase') -> '_5423.CVTBeltConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTBeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.CVTBeltConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5423.CVTBeltConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_belt_connection(self, design_entity: '_1810.BeltConnection') -> '_5392.BeltConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.BeltConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5392.BeltConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_belt_connection_load_case(self, design_entity_analysis: '_6032.BeltConnectionLoadCase') -> '_5392.BeltConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.BeltConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5392.BeltConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_coaxial_connection(self, design_entity: '_1811.CoaxialConnection') -> '_5407.CoaxialConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.CoaxialConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5407.CoaxialConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_coaxial_connection_load_case(self, design_entity_analysis: '_6047.CoaxialConnectionLoadCase') -> '_5407.CoaxialConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.CoaxialConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5407.CoaxialConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_connection(self, design_entity: '_1814.Connection') -> '_5418.ConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5418.ConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_connection_load_case(self, design_entity_analysis: '_6060.ConnectionLoadCase') -> '_5418.ConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5418.ConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection(self, design_entity: '_1823.InterMountableComponentConnection') -> '_5444.InterMountableComponentConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.InterMountableComponentConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5444.InterMountableComponentConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection_load_case(self, design_entity_analysis: '_6115.InterMountableComponentConnectionLoadCase') -> '_5444.InterMountableComponentConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.InterMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.InterMountableComponentConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5444.InterMountableComponentConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_planetary_connection(self, design_entity: '_1826.PlanetaryConnection') -> '_5463.PlanetaryConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.PlanetaryConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5463.PlanetaryConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_planetary_connection_load_case(self, design_entity_analysis: '_6136.PlanetaryConnectionLoadCase') -> '_5463.PlanetaryConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.PlanetaryConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5463.PlanetaryConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_rolling_ring_connection(self, design_entity: '_1830.RollingRingConnection') -> '_5470.RollingRingConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.RollingRingConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5470.RollingRingConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_rolling_ring_connection_load_case(self, design_entity_analysis: '_6147.RollingRingConnectionLoadCase') -> '_5470.RollingRingConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.RollingRingConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5470.RollingRingConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1834.ShaftToMountableComponentConnection') -> '_5475.ShaftToMountableComponentConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ShaftToMountableComponentConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5475.ShaftToMountableComponentConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection_load_case(self, design_entity_analysis: '_6152.ShaftToMountableComponentConnectionLoadCase') -> '_5475.ShaftToMountableComponentConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftToMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ShaftToMountableComponentConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5475.ShaftToMountableComponentConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1840.BevelDifferentialGearMesh') -> '_5394.BevelDifferentialGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.BevelDifferentialGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5394.BevelDifferentialGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh_load_case(self, design_entity_analysis: '_6035.BevelDifferentialGearMeshLoadCase') -> '_5394.BevelDifferentialGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.BevelDifferentialGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5394.BevelDifferentialGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_concept_gear_mesh(self, design_entity: '_1844.ConceptGearMesh') -> '_5412.ConceptGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ConceptGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5412.ConceptGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_concept_gear_mesh_load_case(self, design_entity_analysis: '_6053.ConceptGearMeshLoadCase') -> '_5412.ConceptGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ConceptGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5412.ConceptGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_face_gear_mesh(self, design_entity: '_1850.FaceGearMesh') -> '_5432.FaceGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.FaceGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5432.FaceGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_face_gear_mesh_load_case(self, design_entity_analysis: '_6091.FaceGearMeshLoadCase') -> '_5432.FaceGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.FaceGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5432.FaceGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1864.StraightBevelDiffGearMesh') -> '_5484.StraightBevelDiffGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.StraightBevelDiffGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5484.StraightBevelDiffGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh_load_case(self, design_entity_analysis: '_6163.StraightBevelDiffGearMeshLoadCase') -> '_5484.StraightBevelDiffGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.StraightBevelDiffGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5484.StraightBevelDiffGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_bevel_gear_mesh(self, design_entity: '_1842.BevelGearMesh') -> '_5399.BevelGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.BevelGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5399.BevelGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6040.BevelGearMeshLoadCase') -> '_5399.BevelGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.BevelGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5399.BevelGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_conical_gear_mesh(self, design_entity: '_1846.ConicalGearMesh') -> '_5415.ConicalGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ConicalGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5415.ConicalGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_conical_gear_mesh_load_case(self, design_entity_analysis: '_6057.ConicalGearMeshLoadCase') -> '_5415.ConicalGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ConicalGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5415.ConicalGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1838.AGMAGleasonConicalGearMesh') -> '_5387.AGMAGleasonConicalGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.AGMAGleasonConicalGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5387.AGMAGleasonConicalGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh_load_case(self, design_entity_analysis: '_6027.AGMAGleasonConicalGearMeshLoadCase') -> '_5387.AGMAGleasonConicalGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.AGMAGleasonConicalGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5387.AGMAGleasonConicalGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1848.CylindricalGearMesh') -> '_5426.CylindricalGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.CylindricalGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5426.CylindricalGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh_load_case(self, design_entity_analysis: '_6070.CylindricalGearMeshLoadCase') -> '_5426.CylindricalGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.CylindricalGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5426.CylindricalGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh(self, design_entity: '_1854.HypoidGearMesh') -> '_5440.HypoidGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.HypoidGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5440.HypoidGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_6111.HypoidGearMeshLoadCase') -> '_5440.HypoidGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.HypoidGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5440.HypoidGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1857.KlingelnbergCycloPalloidConicalGearMesh') -> '_5445.KlingelnbergCycloPalloidConicalGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.KlingelnbergCycloPalloidConicalGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5445.KlingelnbergCycloPalloidConicalGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh_load_case(self, design_entity_analysis: '_6117.KlingelnbergCycloPalloidConicalGearMeshLoadCase') -> '_5445.KlingelnbergCycloPalloidConicalGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.KlingelnbergCycloPalloidConicalGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5445.KlingelnbergCycloPalloidConicalGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1858.KlingelnbergCycloPalloidHypoidGearMesh') -> '_5448.KlingelnbergCycloPalloidHypoidGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.KlingelnbergCycloPalloidHypoidGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5448.KlingelnbergCycloPalloidHypoidGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_6120.KlingelnbergCycloPalloidHypoidGearMeshLoadCase') -> '_5448.KlingelnbergCycloPalloidHypoidGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.KlingelnbergCycloPalloidHypoidGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5448.KlingelnbergCycloPalloidHypoidGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1859.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> '_5451.KlingelnbergCycloPalloidSpiralBevelGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.KlingelnbergCycloPalloidSpiralBevelGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5451.KlingelnbergCycloPalloidSpiralBevelGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6123.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase') -> '_5451.KlingelnbergCycloPalloidSpiralBevelGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.KlingelnbergCycloPalloidSpiralBevelGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5451.KlingelnbergCycloPalloidSpiralBevelGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1862.SpiralBevelGearMesh') -> '_5478.SpiralBevelGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.SpiralBevelGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5478.SpiralBevelGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6156.SpiralBevelGearMeshLoadCase') -> '_5478.SpiralBevelGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.SpiralBevelGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5478.SpiralBevelGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1866.StraightBevelGearMesh') -> '_5487.StraightBevelGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.StraightBevelGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5487.StraightBevelGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6166.StraightBevelGearMeshLoadCase') -> '_5487.StraightBevelGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.StraightBevelGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5487.StraightBevelGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_worm_gear_mesh(self, design_entity: '_1868.WormGearMesh') -> '_5502.WormGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.WormGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5502.WormGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_worm_gear_mesh_load_case(self, design_entity_analysis: '_6187.WormGearMeshLoadCase') -> '_5502.WormGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.WormGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5502.WormGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1870.ZerolBevelGearMesh') -> '_5505.ZerolBevelGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ZerolBevelGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5505.ZerolBevelGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6190.ZerolBevelGearMeshLoadCase') -> '_5505.ZerolBevelGearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ZerolBevelGearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5505.ZerolBevelGearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_gear_mesh(self, design_entity: '_1852.GearMesh') -> '_5436.GearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.GearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5436.GearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_gear_mesh_load_case(self, design_entity_analysis: '_6097.GearMeshLoadCase') -> '_5436.GearMeshSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.GearMeshSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5436.GearMeshSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_connection(self, design_entity: '_1878.PartToPartShearCouplingConnection') -> '_5460.PartToPartShearCouplingConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.PartToPartShearCouplingConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5460.PartToPartShearCouplingConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_connection_load_case(self, design_entity_analysis: '_6133.PartToPartShearCouplingConnectionLoadCase') -> '_5460.PartToPartShearCouplingConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.PartToPartShearCouplingConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5460.PartToPartShearCouplingConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_clutch_connection(self, design_entity: '_1872.ClutchConnection') -> '_5404.ClutchConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ClutchConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5404.ClutchConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_clutch_connection_load_case(self, design_entity_analysis: '_6044.ClutchConnectionLoadCase') -> '_5404.ClutchConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ClutchConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5404.ClutchConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_concept_coupling_connection(self, design_entity: '_1874.ConceptCouplingConnection') -> '_5409.ConceptCouplingConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ConceptCouplingConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5409.ConceptCouplingConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_concept_coupling_connection_load_case(self, design_entity_analysis: '_6049.ConceptCouplingConnectionLoadCase') -> '_5409.ConceptCouplingConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ConceptCouplingConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5409.ConceptCouplingConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_coupling_connection(self, design_entity: '_1876.CouplingConnection') -> '_5420.CouplingConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.CouplingConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5420.CouplingConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_coupling_connection_load_case(self, design_entity_analysis: '_6062.CouplingConnectionLoadCase') -> '_5420.CouplingConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.CouplingConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5420.CouplingConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_spring_damper_connection(self, design_entity: '_1880.SpringDamperConnection') -> '_5481.SpringDamperConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.SpringDamperConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5481.SpringDamperConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_spring_damper_connection_load_case(self, design_entity_analysis: '_6158.SpringDamperConnectionLoadCase') -> '_5481.SpringDamperConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.SpringDamperConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5481.SpringDamperConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_torque_converter_connection(self, design_entity: '_1882.TorqueConverterConnection') -> '_5496.TorqueConverterConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.TorqueConverterConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5496.TorqueConverterConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_torque_converter_connection_load_case(self, design_entity_analysis: '_6176.TorqueConverterConnectionLoadCase') -> '_5496.TorqueConverterConnectionSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.TorqueConverterConnectionSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5496.TorqueConverterConnectionSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_abstract_assembly(self, design_entity: '_1958.AbstractAssembly') -> '_5385.AbstractAssemblySingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.AbstractAssemblySingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5385.AbstractAssemblySingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_abstract_assembly_load_case(self, design_entity_analysis: '_6023.AbstractAssemblyLoadCase') -> '_5385.AbstractAssemblySingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.AbstractAssemblySingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5385.AbstractAssemblySingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing(self, design_entity: '_1959.AbstractShaftOrHousing') -> '_5386.AbstractShaftOrHousingSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.AbstractShaftOrHousingSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5386.AbstractShaftOrHousingSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing_load_case(self, design_entity_analysis: '_6024.AbstractShaftOrHousingLoadCase') -> '_5386.AbstractShaftOrHousingSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractShaftOrHousingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.AbstractShaftOrHousingSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5386.AbstractShaftOrHousingSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_bearing(self, design_entity: '_1962.Bearing') -> '_5391.BearingSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.BearingSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5391.BearingSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_bearing_load_case(self, design_entity_analysis: '_6031.BearingLoadCase') -> '_5391.BearingSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.BearingSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5391.BearingSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_bolt(self, design_entity: '_1964.Bolt') -> '_5403.BoltSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.BoltSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5403.BoltSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_bolt_load_case(self, design_entity_analysis: '_6043.BoltLoadCase') -> '_5403.BoltSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.BoltSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5403.BoltSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_bolted_joint(self, design_entity: '_1965.BoltedJoint') -> '_5402.BoltedJointSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.BoltedJointSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5402.BoltedJointSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_bolted_joint_load_case(self, design_entity_analysis: '_6042.BoltedJointLoadCase') -> '_5402.BoltedJointSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltedJointLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.BoltedJointSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5402.BoltedJointSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_component(self, design_entity: '_1966.Component') -> '_5408.ComponentSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ComponentSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5408.ComponentSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_component_load_case(self, design_entity_analysis: '_6048.ComponentLoadCase') -> '_5408.ComponentSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ComponentSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5408.ComponentSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_connector(self, design_entity: '_1969.Connector') -> '_5419.ConnectorSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ConnectorSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5419.ConnectorSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_connector_load_case(self, design_entity_analysis: '_6061.ConnectorLoadCase') -> '_5419.ConnectorSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectorLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ConnectorSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5419.ConnectorSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_datum(self, design_entity: '_1970.Datum') -> '_5430.DatumSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.DatumSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5430.DatumSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_datum_load_case(self, design_entity_analysis: '_6076.DatumLoadCase') -> '_5430.DatumSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.DatumLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.DatumSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5430.DatumSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_external_cad_model(self, design_entity: '_1973.ExternalCADModel') -> '_5431.ExternalCADModelSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ExternalCADModelSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5431.ExternalCADModelSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_external_cad_model_load_case(self, design_entity_analysis: '_6089.ExternalCADModelLoadCase') -> '_5431.ExternalCADModelSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ExternalCADModelSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5431.ExternalCADModelSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_flexible_pin_assembly(self, design_entity: '_1974.FlexiblePinAssembly') -> '_5435.FlexiblePinAssemblySingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.FlexiblePinAssemblySingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5435.FlexiblePinAssemblySingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_flexible_pin_assembly_load_case(self, design_entity_analysis: '_6093.FlexiblePinAssemblyLoadCase') -> '_5435.FlexiblePinAssemblySingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FlexiblePinAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.FlexiblePinAssemblySingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5435.FlexiblePinAssemblySingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_assembly(self, design_entity: '_1957.Assembly') -> '_5390.AssemblySingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.AssemblySingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5390.AssemblySingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_assembly_load_case(self, design_entity_analysis: '_6030.AssemblyLoadCase') -> '_5390.AssemblySingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.AssemblySingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5390.AssemblySingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_guide_dxf_model(self, design_entity: '_1975.GuideDxfModel') -> '_5439.GuideDxfModelSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.GuideDxfModelSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5439.GuideDxfModelSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_guide_dxf_model_load_case(self, design_entity_analysis: '_6101.GuideDxfModelLoadCase') -> '_5439.GuideDxfModelSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GuideDxfModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.GuideDxfModelSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5439.GuideDxfModelSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_imported_fe_component(self, design_entity: '_1978.ImportedFEComponent') -> '_5443.ImportedFEComponentSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ImportedFEComponentSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5443.ImportedFEComponentSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_imported_fe_component_load_case(self, design_entity_analysis: '_6113.ImportedFEComponentLoadCase') -> '_5443.ImportedFEComponentSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ImportedFEComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ImportedFEComponentSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5443.ImportedFEComponentSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_mass_disc(self, design_entity: '_1981.MassDisc') -> '_5454.MassDiscSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.MassDiscSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5454.MassDiscSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_mass_disc_load_case(self, design_entity_analysis: '_6125.MassDiscLoadCase') -> '_5454.MassDiscSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MassDiscLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.MassDiscSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5454.MassDiscSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_measurement_component(self, design_entity: '_1982.MeasurementComponent') -> '_5455.MeasurementComponentSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.MeasurementComponentSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5455.MeasurementComponentSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_measurement_component_load_case(self, design_entity_analysis: '_6126.MeasurementComponentLoadCase') -> '_5455.MeasurementComponentSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MeasurementComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.MeasurementComponentSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5455.MeasurementComponentSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_mountable_component(self, design_entity: '_1983.MountableComponent') -> '_5457.MountableComponentSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.MountableComponentSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5457.MountableComponentSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_mountable_component_load_case(self, design_entity_analysis: '_6128.MountableComponentLoadCase') -> '_5457.MountableComponentSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MountableComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.MountableComponentSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5457.MountableComponentSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_oil_seal(self, design_entity: '_1985.OilSeal') -> '_5458.OilSealSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.OilSealSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5458.OilSealSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_oil_seal_load_case(self, design_entity_analysis: '_6130.OilSealLoadCase') -> '_5458.OilSealSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.OilSealSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5458.OilSealSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_part(self, design_entity: '_1986.Part') -> '_5459.PartSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.PartSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5459.PartSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_part_load_case(self, design_entity_analysis: '_6132.PartLoadCase') -> '_5459.PartSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.PartSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5459.PartSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_planet_carrier(self, design_entity: '_1987.PlanetCarrier') -> '_5465.PlanetCarrierSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.PlanetCarrierSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5465.PlanetCarrierSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_planet_carrier_load_case(self, design_entity_analysis: '_6139.PlanetCarrierLoadCase') -> '_5465.PlanetCarrierSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.PlanetCarrierSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5465.PlanetCarrierSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_point_load(self, design_entity: '_1989.PointLoad') -> '_5466.PointLoadSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.PointLoadSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5466.PointLoadSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_point_load_load_case(self, design_entity_analysis: '_6142.PointLoadLoadCase') -> '_5466.PointLoadSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.PointLoadSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5466.PointLoadSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_power_load(self, design_entity: '_1990.PowerLoad') -> '_5467.PowerLoadSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.PowerLoadSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5467.PowerLoadSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_power_load_load_case(self, design_entity_analysis: '_6143.PowerLoadLoadCase') -> '_5467.PowerLoadSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.PowerLoadSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5467.PowerLoadSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_root_assembly(self, design_entity: '_1992.RootAssembly') -> '_5472.RootAssemblySingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.RootAssemblySingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5472.RootAssemblySingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_root_assembly_load_case(self, design_entity_analysis: '_6149.RootAssemblyLoadCase') -> '_5472.RootAssemblySingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RootAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.RootAssemblySingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5472.RootAssemblySingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_specialised_assembly(self, design_entity: '_1994.SpecialisedAssembly') -> '_5477.SpecialisedAssemblySingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.SpecialisedAssemblySingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5477.SpecialisedAssemblySingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_specialised_assembly_load_case(self, design_entity_analysis: '_6153.SpecialisedAssemblyLoadCase') -> '_5477.SpecialisedAssemblySingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpecialisedAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.SpecialisedAssemblySingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5477.SpecialisedAssemblySingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_unbalanced_mass(self, design_entity: '_1995.UnbalancedMass') -> '_5500.UnbalancedMassSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.UnbalancedMassSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5500.UnbalancedMassSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_unbalanced_mass_load_case(self, design_entity_analysis: '_6184.UnbalancedMassLoadCase') -> '_5500.UnbalancedMassSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.UnbalancedMassLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.UnbalancedMassSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5500.UnbalancedMassSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_virtual_component(self, design_entity: '_1996.VirtualComponent') -> '_5501.VirtualComponentSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.VirtualComponentSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5501.VirtualComponentSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_virtual_component_load_case(self, design_entity_analysis: '_6185.VirtualComponentLoadCase') -> '_5501.VirtualComponentSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.VirtualComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.VirtualComponentSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5501.VirtualComponentSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_shaft(self, design_entity: '_1999.Shaft') -> '_5474.ShaftSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ShaftSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5474.ShaftSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_shaft_load_case(self, design_entity_analysis: '_6151.ShaftLoadCase') -> '_5474.ShaftSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ShaftSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5474.ShaftSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_concept_gear(self, design_entity: '_2037.ConceptGear') -> '_5414.ConceptGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ConceptGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5414.ConceptGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_concept_gear_load_case(self, design_entity_analysis: '_6052.ConceptGearLoadCase') -> '_5414.ConceptGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ConceptGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5414.ConceptGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_concept_gear_set(self, design_entity: '_2038.ConceptGearSet') -> '_5413.ConceptGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ConceptGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5413.ConceptGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_concept_gear_set_load_case(self, design_entity_analysis: '_6054.ConceptGearSetLoadCase') -> '_5413.ConceptGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ConceptGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5413.ConceptGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_face_gear(self, design_entity: '_2044.FaceGear') -> '_5434.FaceGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.FaceGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5434.FaceGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_face_gear_load_case(self, design_entity_analysis: '_6090.FaceGearLoadCase') -> '_5434.FaceGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.FaceGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5434.FaceGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_face_gear_set(self, design_entity: '_2045.FaceGearSet') -> '_5433.FaceGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.FaceGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5433.FaceGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_face_gear_set_load_case(self, design_entity_analysis: '_6092.FaceGearSetLoadCase') -> '_5433.FaceGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.FaceGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5433.FaceGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear(self, design_entity: '_2029.AGMAGleasonConicalGear') -> '_5389.AGMAGleasonConicalGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.AGMAGleasonConicalGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5389.AGMAGleasonConicalGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_load_case(self, design_entity_analysis: '_6026.AGMAGleasonConicalGearLoadCase') -> '_5389.AGMAGleasonConicalGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.AGMAGleasonConicalGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5389.AGMAGleasonConicalGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_2030.AGMAGleasonConicalGearSet') -> '_5388.AGMAGleasonConicalGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.AGMAGleasonConicalGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5388.AGMAGleasonConicalGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set_load_case(self, design_entity_analysis: '_6028.AGMAGleasonConicalGearSetLoadCase') -> '_5388.AGMAGleasonConicalGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.AGMAGleasonConicalGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5388.AGMAGleasonConicalGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_gear(self, design_entity: '_2031.BevelDifferentialGear') -> '_5396.BevelDifferentialGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.BevelDifferentialGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5396.BevelDifferentialGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_gear_load_case(self, design_entity_analysis: '_6034.BevelDifferentialGearLoadCase') -> '_5396.BevelDifferentialGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.BevelDifferentialGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5396.BevelDifferentialGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set(self, design_entity: '_2032.BevelDifferentialGearSet') -> '_5395.BevelDifferentialGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.BevelDifferentialGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5395.BevelDifferentialGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set_load_case(self, design_entity_analysis: '_6036.BevelDifferentialGearSetLoadCase') -> '_5395.BevelDifferentialGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.BevelDifferentialGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5395.BevelDifferentialGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2033.BevelDifferentialPlanetGear') -> '_5397.BevelDifferentialPlanetGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.BevelDifferentialPlanetGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5397.BevelDifferentialPlanetGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear_load_case(self, design_entity_analysis: '_6037.BevelDifferentialPlanetGearLoadCase') -> '_5397.BevelDifferentialPlanetGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.BevelDifferentialPlanetGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5397.BevelDifferentialPlanetGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2034.BevelDifferentialSunGear') -> '_5398.BevelDifferentialSunGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.BevelDifferentialSunGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5398.BevelDifferentialSunGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear_load_case(self, design_entity_analysis: '_6038.BevelDifferentialSunGearLoadCase') -> '_5398.BevelDifferentialSunGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.BevelDifferentialSunGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5398.BevelDifferentialSunGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_bevel_gear(self, design_entity: '_2035.BevelGear') -> '_5401.BevelGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.BevelGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5401.BevelGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_bevel_gear_load_case(self, design_entity_analysis: '_6039.BevelGearLoadCase') -> '_5401.BevelGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.BevelGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5401.BevelGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_bevel_gear_set(self, design_entity: '_2036.BevelGearSet') -> '_5400.BevelGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.BevelGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5400.BevelGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_bevel_gear_set_load_case(self, design_entity_analysis: '_6041.BevelGearSetLoadCase') -> '_5400.BevelGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.BevelGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5400.BevelGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_conical_gear(self, design_entity: '_2039.ConicalGear') -> '_5417.ConicalGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ConicalGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5417.ConicalGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_conical_gear_load_case(self, design_entity_analysis: '_6055.ConicalGearLoadCase') -> '_5417.ConicalGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ConicalGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5417.ConicalGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_conical_gear_set(self, design_entity: '_2040.ConicalGearSet') -> '_5416.ConicalGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ConicalGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5416.ConicalGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_conical_gear_set_load_case(self, design_entity_analysis: '_6059.ConicalGearSetLoadCase') -> '_5416.ConicalGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.ConicalGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5416.ConicalGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_gear(self, design_entity: '_2041.CylindricalGear') -> '_5428.CylindricalGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.CylindricalGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5428.CylindricalGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_gear_load_case(self, design_entity_analysis: '_6068.CylindricalGearLoadCase') -> '_5428.CylindricalGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.CylindricalGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5428.CylindricalGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_gear_set(self, design_entity: '_2042.CylindricalGearSet') -> '_5427.CylindricalGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.CylindricalGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5427.CylindricalGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_gear_set_load_case(self, design_entity_analysis: '_6072.CylindricalGearSetLoadCase') -> '_5427.CylindricalGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.CylindricalGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5427.CylindricalGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear(self, design_entity: '_2043.CylindricalPlanetGear') -> '_5429.CylindricalPlanetGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.CylindricalPlanetGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5429.CylindricalPlanetGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear_load_case(self, design_entity_analysis: '_6073.CylindricalPlanetGearLoadCase') -> '_5429.CylindricalPlanetGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.CylindricalPlanetGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5429.CylindricalPlanetGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_gear(self, design_entity: '_2046.Gear') -> '_5438.GearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.GearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5438.GearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_gear_load_case(self, design_entity_analysis: '_6095.GearLoadCase') -> '_5438.GearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.GearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5438.GearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_gear_set(self, design_entity: '_2048.GearSet') -> '_5437.GearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.GearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5437.GearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_gear_set_load_case(self, design_entity_analysis: '_6100.GearSetLoadCase') -> '_5437.GearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.GearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5437.GearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_hypoid_gear(self, design_entity: '_2050.HypoidGear') -> '_5442.HypoidGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.HypoidGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5442.HypoidGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_hypoid_gear_load_case(self, design_entity_analysis: '_6110.HypoidGearLoadCase') -> '_5442.HypoidGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.HypoidGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5442.HypoidGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_hypoid_gear_set(self, design_entity: '_2051.HypoidGearSet') -> '_5441.HypoidGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.HypoidGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5441.HypoidGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_hypoid_gear_set_load_case(self, design_entity_analysis: '_6112.HypoidGearSetLoadCase') -> '_5441.HypoidGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.HypoidGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5441.HypoidGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2052.KlingelnbergCycloPalloidConicalGear') -> '_5447.KlingelnbergCycloPalloidConicalGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.KlingelnbergCycloPalloidConicalGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5447.KlingelnbergCycloPalloidConicalGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_load_case(self, design_entity_analysis: '_6116.KlingelnbergCycloPalloidConicalGearLoadCase') -> '_5447.KlingelnbergCycloPalloidConicalGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.KlingelnbergCycloPalloidConicalGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5447.KlingelnbergCycloPalloidConicalGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2053.KlingelnbergCycloPalloidConicalGearSet') -> '_5446.KlingelnbergCycloPalloidConicalGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.KlingelnbergCycloPalloidConicalGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5446.KlingelnbergCycloPalloidConicalGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set_load_case(self, design_entity_analysis: '_6118.KlingelnbergCycloPalloidConicalGearSetLoadCase') -> '_5446.KlingelnbergCycloPalloidConicalGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.KlingelnbergCycloPalloidConicalGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5446.KlingelnbergCycloPalloidConicalGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2054.KlingelnbergCycloPalloidHypoidGear') -> '_5450.KlingelnbergCycloPalloidHypoidGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.KlingelnbergCycloPalloidHypoidGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5450.KlingelnbergCycloPalloidHypoidGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_load_case(self, design_entity_analysis: '_6119.KlingelnbergCycloPalloidHypoidGearLoadCase') -> '_5450.KlingelnbergCycloPalloidHypoidGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.KlingelnbergCycloPalloidHypoidGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5450.KlingelnbergCycloPalloidHypoidGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2055.KlingelnbergCycloPalloidHypoidGearSet') -> '_5449.KlingelnbergCycloPalloidHypoidGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.KlingelnbergCycloPalloidHypoidGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5449.KlingelnbergCycloPalloidHypoidGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(self, design_entity_analysis: '_6121.KlingelnbergCycloPalloidHypoidGearSetLoadCase') -> '_5449.KlingelnbergCycloPalloidHypoidGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.KlingelnbergCycloPalloidHypoidGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5449.KlingelnbergCycloPalloidHypoidGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2056.KlingelnbergCycloPalloidSpiralBevelGear') -> '_5453.KlingelnbergCycloPalloidSpiralBevelGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.KlingelnbergCycloPalloidSpiralBevelGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5453.KlingelnbergCycloPalloidSpiralBevelGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(self, design_entity_analysis: '_6122.KlingelnbergCycloPalloidSpiralBevelGearLoadCase') -> '_5453.KlingelnbergCycloPalloidSpiralBevelGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.KlingelnbergCycloPalloidSpiralBevelGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5453.KlingelnbergCycloPalloidSpiralBevelGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2057.KlingelnbergCycloPalloidSpiralBevelGearSet') -> '_5452.KlingelnbergCycloPalloidSpiralBevelGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.KlingelnbergCycloPalloidSpiralBevelGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5452.KlingelnbergCycloPalloidSpiralBevelGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_6124.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase') -> '_5452.KlingelnbergCycloPalloidSpiralBevelGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.KlingelnbergCycloPalloidSpiralBevelGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5452.KlingelnbergCycloPalloidSpiralBevelGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_planetary_gear_set(self, design_entity: '_2058.PlanetaryGearSet') -> '_5464.PlanetaryGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.PlanetaryGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5464.PlanetaryGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_planetary_gear_set_load_case(self, design_entity_analysis: '_6137.PlanetaryGearSetLoadCase') -> '_5464.PlanetaryGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.PlanetaryGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5464.PlanetaryGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_spiral_bevel_gear(self, design_entity: '_2059.SpiralBevelGear') -> '_5480.SpiralBevelGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.SpiralBevelGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5480.SpiralBevelGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_load_case(self, design_entity_analysis: '_6155.SpiralBevelGearLoadCase') -> '_5480.SpiralBevelGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.SpiralBevelGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5480.SpiralBevelGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set(self, design_entity: '_2060.SpiralBevelGearSet') -> '_5479.SpiralBevelGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.SpiralBevelGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5479.SpiralBevelGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_6157.SpiralBevelGearSetLoadCase') -> '_5479.SpiralBevelGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.SpiralBevelGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5479.SpiralBevelGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2061.StraightBevelDiffGear') -> '_5486.StraightBevelDiffGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.StraightBevelDiffGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5486.StraightBevelDiffGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_load_case(self, design_entity_analysis: '_6162.StraightBevelDiffGearLoadCase') -> '_5486.StraightBevelDiffGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.StraightBevelDiffGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5486.StraightBevelDiffGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_2062.StraightBevelDiffGearSet') -> '_5485.StraightBevelDiffGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.StraightBevelDiffGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5485.StraightBevelDiffGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set_load_case(self, design_entity_analysis: '_6164.StraightBevelDiffGearSetLoadCase') -> '_5485.StraightBevelDiffGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.StraightBevelDiffGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5485.StraightBevelDiffGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_gear(self, design_entity: '_2063.StraightBevelGear') -> '_5489.StraightBevelGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.StraightBevelGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5489.StraightBevelGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_gear_load_case(self, design_entity_analysis: '_6165.StraightBevelGearLoadCase') -> '_5489.StraightBevelGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.StraightBevelGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5489.StraightBevelGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set(self, design_entity: '_2064.StraightBevelGearSet') -> '_5488.StraightBevelGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.StraightBevelGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5488.StraightBevelGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set_load_case(self, design_entity_analysis: '_6167.StraightBevelGearSetLoadCase') -> '_5488.StraightBevelGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.StraightBevelGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5488.StraightBevelGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2065.StraightBevelPlanetGear') -> '_5490.StraightBevelPlanetGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.StraightBevelPlanetGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5490.StraightBevelPlanetGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear_load_case(self, design_entity_analysis: '_6168.StraightBevelPlanetGearLoadCase') -> '_5490.StraightBevelPlanetGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.StraightBevelPlanetGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5490.StraightBevelPlanetGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2066.StraightBevelSunGear') -> '_5491.StraightBevelSunGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.StraightBevelSunGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5491.StraightBevelSunGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear_load_case(self, design_entity_analysis: '_6169.StraightBevelSunGearLoadCase') -> '_5491.StraightBevelSunGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.StraightBevelSunGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5491.StraightBevelSunGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_worm_gear(self, design_entity: '_2067.WormGear') -> '_5504.WormGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.WormGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5504.WormGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_worm_gear_load_case(self, design_entity_analysis: '_6186.WormGearLoadCase') -> '_5504.WormGearSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.WormGearSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5504.WormGearSingleMeshWhineAnalysis)(method_result) if method_result else None

    def results_for_worm_gear_set(self, design_entity: '_2068.WormGearSet') -> '_5503.WormGearSetSingleMeshWhineAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.WormGearSetSingleMeshWhineAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5503.WormGearSetSingleMeshWhineAnalysis)(method_result) if method_result else None
