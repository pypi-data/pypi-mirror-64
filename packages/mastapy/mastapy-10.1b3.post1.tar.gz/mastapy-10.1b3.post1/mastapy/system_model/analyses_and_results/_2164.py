'''_2164.py

ModalAnalysisAnalysis
'''


from mastapy.system_model.analyses_and_results.static_loads import (
    _6208, _6209, _6211, _6155,
    _6154, _6053, _6066, _6065,
    _6071, _6070, _6084, _6083,
    _6086, _6087, _6164, _6170,
    _6168, _6166, _6180, _6179,
    _6191, _6190, _6192, _6193,
    _6197, _6198, _6199, _6085,
    _6052, _6067, _6080, _6135,
    _6156, _6167, _6172, _6055,
    _6073, _6111, _6183, _6060,
    _6077, _6047, _6090, _6131,
    _6137, _6140, _6143, _6176,
    _6186, _6207, _6210, _6117,
    _6153, _6064, _6069, _6082,
    _6178, _6196, _6043, _6044,
    _6051, _6063, _6062, _6068,
    _6081, _6096, _6109, _6113,
    _6050, _6121, _6133, _6145,
    _6146, _6148, _6150, _6152,
    _6159, _6162, _6163, _6169,
    _6173, _6204, _6205, _6171,
    _6072, _6074, _6110, _6112,
    _6046, _6048, _6054, _6056,
    _6057, _6058, _6059, _6061,
    _6075, _6079, _6088, _6092,
    _6093, _6115, _6120, _6130,
    _6132, _6136, _6138, _6139,
    _6141, _6142, _6144, _6157,
    _6175, _6177, _6182, _6184,
    _6185, _6187, _6188, _6189,
    _6206
)
from mastapy.system_model.analyses_and_results.modal_analyses import (
    _4826, _4828, _4829, _4779,
    _4778, _4704, _4717, _4716,
    _4722, _4721, _4734, _4733,
    _4736, _4737, _4785, _4790,
    _4788, _4786, _4800, _4799,
    _4810, _4809, _4811, _4812,
    _4814, _4815, _4816, _4735,
    _4703, _4718, _4729, _4757,
    _4780, _4787, _4793, _4705,
    _4723, _4744, _4801, _4710,
    _4726, _4698, _4738, _4753,
    _4758, _4761, _4764, _4795,
    _4804, _4824, _4827, _4749,
    _4777, _4715, _4720, _4732,
    _4798, _4813, _4696, _4697,
    _4702, _4714, _4713, _4719,
    _4730, _4742, _4743, _4747,
    _4701, _4752, _4756, _4767,
    _4768, _4773, _4774, _4776,
    _4782, _4783, _4784, _4789,
    _4794, _4817, _4818, _4791,
    _4724, _4725, _4745, _4746,
    _4699, _4700, _4706, _4707,
    _4708, _4709, _4711, _4712,
    _4727, _4728, _4739, _4740,
    _4741, _4750, _4751, _4754,
    _4755, _4759, _4760, _4762,
    _4763, _4765, _4766, _4781,
    _4796, _4797, _4802, _4803,
    _4805, _4806, _4807, _4808,
    _4825
)
from mastapy._internal import constructor
from mastapy.system_model.part_model.gears import (
    _2089, _2090, _2057, _2058,
    _2064, _2065, _2049, _2050,
    _2051, _2052, _2053, _2054,
    _2055, _2056, _2059, _2060,
    _2061, _2062, _2063, _2066,
    _2068, _2070, _2071, _2072,
    _2073, _2074, _2075, _2076,
    _2077, _2078, _2079, _2080,
    _2081, _2082, _2083, _2084,
    _2085, _2086, _2087, _2088
)
from mastapy.system_model.part_model.couplings import (
    _2119, _2120, _2108, _2110,
    _2111, _2113, _2114, _2115,
    _2116, _2117, _2118, _2121,
    _2129, _2127, _2128, _2130,
    _2131, _2132, _2134, _2135,
    _2136, _2137, _2138, _2140
)
from mastapy.system_model.connections_and_sockets import (
    _1835, _1830, _1831, _1834,
    _1843, _1846, _1850, _1854
)
from mastapy.system_model.connections_and_sockets.gears import (
    _1860, _1864, _1870, _1884,
    _1862, _1866, _1858, _1868,
    _1874, _1877, _1878, _1879,
    _1882, _1886, _1888, _1890,
    _1872
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _1898, _1892, _1894, _1896,
    _1900, _1902
)
from mastapy.system_model.part_model import (
    _1978, _1979, _1982, _1984,
    _1985, _1986, _1989, _1990,
    _1993, _1994, _1977, _1995,
    _1998, _2001, _2002, _2003,
    _2005, _2006, _2007, _2009,
    _2010, _2012, _2014, _2015,
    _2016
)
from mastapy.system_model.part_model.shaft_model import _2019
from mastapy.system_model.analyses_and_results import _2150
from mastapy._internal.python_net import python_net_import

_MODAL_ANALYSIS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'ModalAnalysisAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ModalAnalysisAnalysis',)


class ModalAnalysisAnalysis(_2150.SingleAnalysis):
    '''ModalAnalysisAnalysis

    This is a mastapy class.
    '''

    TYPE = _MODAL_ANALYSIS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ModalAnalysisAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    def results_for_worm_gear_set_load_case(self, design_entity_analysis: '_6208.WormGearSetLoadCase') -> '_4826.WormGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.WormGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4826.WormGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_zerol_bevel_gear(self, design_entity: '_2089.ZerolBevelGear') -> '_4828.ZerolBevelGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ZerolBevelGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4828.ZerolBevelGearModalAnalysis)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_load_case(self, design_entity_analysis: '_6209.ZerolBevelGearLoadCase') -> '_4828.ZerolBevelGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ZerolBevelGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4828.ZerolBevelGearModalAnalysis)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set(self, design_entity: '_2090.ZerolBevelGearSet') -> '_4829.ZerolBevelGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ZerolBevelGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4829.ZerolBevelGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set_load_case(self, design_entity_analysis: '_6211.ZerolBevelGearSetLoadCase') -> '_4829.ZerolBevelGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ZerolBevelGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4829.ZerolBevelGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling(self, design_entity: '_2119.PartToPartShearCoupling') -> '_4779.PartToPartShearCouplingModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.PartToPartShearCouplingModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4779.PartToPartShearCouplingModalAnalysis)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_load_case(self, design_entity_analysis: '_6155.PartToPartShearCouplingLoadCase') -> '_4779.PartToPartShearCouplingModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.PartToPartShearCouplingModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4779.PartToPartShearCouplingModalAnalysis)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_half(self, design_entity: '_2120.PartToPartShearCouplingHalf') -> '_4778.PartToPartShearCouplingHalfModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.PartToPartShearCouplingHalfModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4778.PartToPartShearCouplingHalfModalAnalysis)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_half_load_case(self, design_entity_analysis: '_6154.PartToPartShearCouplingHalfLoadCase') -> '_4778.PartToPartShearCouplingHalfModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.PartToPartShearCouplingHalfModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4778.PartToPartShearCouplingHalfModalAnalysis)(method_result) if method_result else None

    def results_for_belt_drive(self, design_entity: '_2108.BeltDrive') -> '_4704.BeltDriveModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.BeltDriveModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4704.BeltDriveModalAnalysis)(method_result) if method_result else None

    def results_for_belt_drive_load_case(self, design_entity_analysis: '_6053.BeltDriveLoadCase') -> '_4704.BeltDriveModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltDriveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.BeltDriveModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4704.BeltDriveModalAnalysis)(method_result) if method_result else None

    def results_for_clutch(self, design_entity: '_2110.Clutch') -> '_4717.ClutchModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ClutchModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4717.ClutchModalAnalysis)(method_result) if method_result else None

    def results_for_clutch_load_case(self, design_entity_analysis: '_6066.ClutchLoadCase') -> '_4717.ClutchModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ClutchModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4717.ClutchModalAnalysis)(method_result) if method_result else None

    def results_for_clutch_half(self, design_entity: '_2111.ClutchHalf') -> '_4716.ClutchHalfModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ClutchHalfModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4716.ClutchHalfModalAnalysis)(method_result) if method_result else None

    def results_for_clutch_half_load_case(self, design_entity_analysis: '_6065.ClutchHalfLoadCase') -> '_4716.ClutchHalfModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ClutchHalfModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4716.ClutchHalfModalAnalysis)(method_result) if method_result else None

    def results_for_concept_coupling(self, design_entity: '_2113.ConceptCoupling') -> '_4722.ConceptCouplingModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ConceptCouplingModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4722.ConceptCouplingModalAnalysis)(method_result) if method_result else None

    def results_for_concept_coupling_load_case(self, design_entity_analysis: '_6071.ConceptCouplingLoadCase') -> '_4722.ConceptCouplingModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ConceptCouplingModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4722.ConceptCouplingModalAnalysis)(method_result) if method_result else None

    def results_for_concept_coupling_half(self, design_entity: '_2114.ConceptCouplingHalf') -> '_4721.ConceptCouplingHalfModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ConceptCouplingHalfModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4721.ConceptCouplingHalfModalAnalysis)(method_result) if method_result else None

    def results_for_concept_coupling_half_load_case(self, design_entity_analysis: '_6070.ConceptCouplingHalfLoadCase') -> '_4721.ConceptCouplingHalfModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ConceptCouplingHalfModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4721.ConceptCouplingHalfModalAnalysis)(method_result) if method_result else None

    def results_for_coupling(self, design_entity: '_2115.Coupling') -> '_4734.CouplingModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.CouplingModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4734.CouplingModalAnalysis)(method_result) if method_result else None

    def results_for_coupling_load_case(self, design_entity_analysis: '_6084.CouplingLoadCase') -> '_4734.CouplingModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.CouplingModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4734.CouplingModalAnalysis)(method_result) if method_result else None

    def results_for_coupling_half(self, design_entity: '_2116.CouplingHalf') -> '_4733.CouplingHalfModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.CouplingHalfModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4733.CouplingHalfModalAnalysis)(method_result) if method_result else None

    def results_for_coupling_half_load_case(self, design_entity_analysis: '_6083.CouplingHalfLoadCase') -> '_4733.CouplingHalfModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.CouplingHalfModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4733.CouplingHalfModalAnalysis)(method_result) if method_result else None

    def results_for_cvt(self, design_entity: '_2117.CVT') -> '_4736.CVTModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.CVTModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4736.CVTModalAnalysis)(method_result) if method_result else None

    def results_for_cvt_load_case(self, design_entity_analysis: '_6086.CVTLoadCase') -> '_4736.CVTModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.CVTModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4736.CVTModalAnalysis)(method_result) if method_result else None

    def results_for_cvt_pulley(self, design_entity: '_2118.CVTPulley') -> '_4737.CVTPulleyModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.CVTPulleyModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4737.CVTPulleyModalAnalysis)(method_result) if method_result else None

    def results_for_cvt_pulley_load_case(self, design_entity_analysis: '_6087.CVTPulleyLoadCase') -> '_4737.CVTPulleyModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTPulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.CVTPulleyModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4737.CVTPulleyModalAnalysis)(method_result) if method_result else None

    def results_for_pulley(self, design_entity: '_2121.Pulley') -> '_4785.PulleyModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.PulleyModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4785.PulleyModalAnalysis)(method_result) if method_result else None

    def results_for_pulley_load_case(self, design_entity_analysis: '_6164.PulleyLoadCase') -> '_4785.PulleyModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.PulleyModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4785.PulleyModalAnalysis)(method_result) if method_result else None

    def results_for_shaft_hub_connection(self, design_entity: '_2129.ShaftHubConnection') -> '_4790.ShaftHubConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ShaftHubConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4790.ShaftHubConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_shaft_hub_connection_load_case(self, design_entity_analysis: '_6170.ShaftHubConnectionLoadCase') -> '_4790.ShaftHubConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ShaftHubConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4790.ShaftHubConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_rolling_ring(self, design_entity: '_2127.RollingRing') -> '_4788.RollingRingModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.RollingRingModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4788.RollingRingModalAnalysis)(method_result) if method_result else None

    def results_for_rolling_ring_load_case(self, design_entity_analysis: '_6168.RollingRingLoadCase') -> '_4788.RollingRingModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.RollingRingModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4788.RollingRingModalAnalysis)(method_result) if method_result else None

    def results_for_rolling_ring_assembly(self, design_entity: '_2128.RollingRingAssembly') -> '_4786.RollingRingAssemblyModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.RollingRingAssemblyModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4786.RollingRingAssemblyModalAnalysis)(method_result) if method_result else None

    def results_for_rolling_ring_assembly_load_case(self, design_entity_analysis: '_6166.RollingRingAssemblyLoadCase') -> '_4786.RollingRingAssemblyModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.RollingRingAssemblyModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4786.RollingRingAssemblyModalAnalysis)(method_result) if method_result else None

    def results_for_spring_damper(self, design_entity: '_2130.SpringDamper') -> '_4800.SpringDamperModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.SpringDamperModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4800.SpringDamperModalAnalysis)(method_result) if method_result else None

    def results_for_spring_damper_load_case(self, design_entity_analysis: '_6180.SpringDamperLoadCase') -> '_4800.SpringDamperModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.SpringDamperModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4800.SpringDamperModalAnalysis)(method_result) if method_result else None

    def results_for_spring_damper_half(self, design_entity: '_2131.SpringDamperHalf') -> '_4799.SpringDamperHalfModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.SpringDamperHalfModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4799.SpringDamperHalfModalAnalysis)(method_result) if method_result else None

    def results_for_spring_damper_half_load_case(self, design_entity_analysis: '_6179.SpringDamperHalfLoadCase') -> '_4799.SpringDamperHalfModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.SpringDamperHalfModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4799.SpringDamperHalfModalAnalysis)(method_result) if method_result else None

    def results_for_synchroniser(self, design_entity: '_2132.Synchroniser') -> '_4810.SynchroniserModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.SynchroniserModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4810.SynchroniserModalAnalysis)(method_result) if method_result else None

    def results_for_synchroniser_load_case(self, design_entity_analysis: '_6191.SynchroniserLoadCase') -> '_4810.SynchroniserModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.SynchroniserModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4810.SynchroniserModalAnalysis)(method_result) if method_result else None

    def results_for_synchroniser_half(self, design_entity: '_2134.SynchroniserHalf') -> '_4809.SynchroniserHalfModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.SynchroniserHalfModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4809.SynchroniserHalfModalAnalysis)(method_result) if method_result else None

    def results_for_synchroniser_half_load_case(self, design_entity_analysis: '_6190.SynchroniserHalfLoadCase') -> '_4809.SynchroniserHalfModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.SynchroniserHalfModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4809.SynchroniserHalfModalAnalysis)(method_result) if method_result else None

    def results_for_synchroniser_part(self, design_entity: '_2135.SynchroniserPart') -> '_4811.SynchroniserPartModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.SynchroniserPartModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4811.SynchroniserPartModalAnalysis)(method_result) if method_result else None

    def results_for_synchroniser_part_load_case(self, design_entity_analysis: '_6192.SynchroniserPartLoadCase') -> '_4811.SynchroniserPartModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserPartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.SynchroniserPartModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4811.SynchroniserPartModalAnalysis)(method_result) if method_result else None

    def results_for_synchroniser_sleeve(self, design_entity: '_2136.SynchroniserSleeve') -> '_4812.SynchroniserSleeveModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.SynchroniserSleeveModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4812.SynchroniserSleeveModalAnalysis)(method_result) if method_result else None

    def results_for_synchroniser_sleeve_load_case(self, design_entity_analysis: '_6193.SynchroniserSleeveLoadCase') -> '_4812.SynchroniserSleeveModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserSleeveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.SynchroniserSleeveModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4812.SynchroniserSleeveModalAnalysis)(method_result) if method_result else None

    def results_for_torque_converter(self, design_entity: '_2137.TorqueConverter') -> '_4814.TorqueConverterModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.TorqueConverterModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4814.TorqueConverterModalAnalysis)(method_result) if method_result else None

    def results_for_torque_converter_load_case(self, design_entity_analysis: '_6197.TorqueConverterLoadCase') -> '_4814.TorqueConverterModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.TorqueConverterModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4814.TorqueConverterModalAnalysis)(method_result) if method_result else None

    def results_for_torque_converter_pump(self, design_entity: '_2138.TorqueConverterPump') -> '_4815.TorqueConverterPumpModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.TorqueConverterPumpModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4815.TorqueConverterPumpModalAnalysis)(method_result) if method_result else None

    def results_for_torque_converter_pump_load_case(self, design_entity_analysis: '_6198.TorqueConverterPumpLoadCase') -> '_4815.TorqueConverterPumpModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterPumpLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.TorqueConverterPumpModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4815.TorqueConverterPumpModalAnalysis)(method_result) if method_result else None

    def results_for_torque_converter_turbine(self, design_entity: '_2140.TorqueConverterTurbine') -> '_4816.TorqueConverterTurbineModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.TorqueConverterTurbineModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4816.TorqueConverterTurbineModalAnalysis)(method_result) if method_result else None

    def results_for_torque_converter_turbine_load_case(self, design_entity_analysis: '_6199.TorqueConverterTurbineLoadCase') -> '_4816.TorqueConverterTurbineModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterTurbineLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.TorqueConverterTurbineModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4816.TorqueConverterTurbineModalAnalysis)(method_result) if method_result else None

    def results_for_cvt_belt_connection(self, design_entity: '_1835.CVTBeltConnection') -> '_4735.CVTBeltConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.CVTBeltConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4735.CVTBeltConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_cvt_belt_connection_load_case(self, design_entity_analysis: '_6085.CVTBeltConnectionLoadCase') -> '_4735.CVTBeltConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTBeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.CVTBeltConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4735.CVTBeltConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_belt_connection(self, design_entity: '_1830.BeltConnection') -> '_4703.BeltConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.BeltConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4703.BeltConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_belt_connection_load_case(self, design_entity_analysis: '_6052.BeltConnectionLoadCase') -> '_4703.BeltConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.BeltConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4703.BeltConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_coaxial_connection(self, design_entity: '_1831.CoaxialConnection') -> '_4718.CoaxialConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.CoaxialConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4718.CoaxialConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_coaxial_connection_load_case(self, design_entity_analysis: '_6067.CoaxialConnectionLoadCase') -> '_4718.CoaxialConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.CoaxialConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4718.CoaxialConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_connection(self, design_entity: '_1834.Connection') -> '_4729.ConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4729.ConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_connection_load_case(self, design_entity_analysis: '_6080.ConnectionLoadCase') -> '_4729.ConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4729.ConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection(self, design_entity: '_1843.InterMountableComponentConnection') -> '_4757.InterMountableComponentConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.InterMountableComponentConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4757.InterMountableComponentConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection_load_case(self, design_entity_analysis: '_6135.InterMountableComponentConnectionLoadCase') -> '_4757.InterMountableComponentConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.InterMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.InterMountableComponentConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4757.InterMountableComponentConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_planetary_connection(self, design_entity: '_1846.PlanetaryConnection') -> '_4780.PlanetaryConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.PlanetaryConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4780.PlanetaryConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_planetary_connection_load_case(self, design_entity_analysis: '_6156.PlanetaryConnectionLoadCase') -> '_4780.PlanetaryConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.PlanetaryConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4780.PlanetaryConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_rolling_ring_connection(self, design_entity: '_1850.RollingRingConnection') -> '_4787.RollingRingConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.RollingRingConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4787.RollingRingConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_rolling_ring_connection_load_case(self, design_entity_analysis: '_6167.RollingRingConnectionLoadCase') -> '_4787.RollingRingConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.RollingRingConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4787.RollingRingConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1854.ShaftToMountableComponentConnection') -> '_4793.ShaftToMountableComponentConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ShaftToMountableComponentConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4793.ShaftToMountableComponentConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection_load_case(self, design_entity_analysis: '_6172.ShaftToMountableComponentConnectionLoadCase') -> '_4793.ShaftToMountableComponentConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftToMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ShaftToMountableComponentConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4793.ShaftToMountableComponentConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1860.BevelDifferentialGearMesh') -> '_4705.BevelDifferentialGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.BevelDifferentialGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4705.BevelDifferentialGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh_load_case(self, design_entity_analysis: '_6055.BevelDifferentialGearMeshLoadCase') -> '_4705.BevelDifferentialGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.BevelDifferentialGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4705.BevelDifferentialGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_concept_gear_mesh(self, design_entity: '_1864.ConceptGearMesh') -> '_4723.ConceptGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ConceptGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4723.ConceptGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_concept_gear_mesh_load_case(self, design_entity_analysis: '_6073.ConceptGearMeshLoadCase') -> '_4723.ConceptGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ConceptGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4723.ConceptGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_face_gear_mesh(self, design_entity: '_1870.FaceGearMesh') -> '_4744.FaceGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.FaceGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4744.FaceGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_face_gear_mesh_load_case(self, design_entity_analysis: '_6111.FaceGearMeshLoadCase') -> '_4744.FaceGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.FaceGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4744.FaceGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1884.StraightBevelDiffGearMesh') -> '_4801.StraightBevelDiffGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelDiffGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4801.StraightBevelDiffGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh_load_case(self, design_entity_analysis: '_6183.StraightBevelDiffGearMeshLoadCase') -> '_4801.StraightBevelDiffGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelDiffGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4801.StraightBevelDiffGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_bevel_gear_mesh(self, design_entity: '_1862.BevelGearMesh') -> '_4710.BevelGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.BevelGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4710.BevelGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6060.BevelGearMeshLoadCase') -> '_4710.BevelGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.BevelGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4710.BevelGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_conical_gear_mesh(self, design_entity: '_1866.ConicalGearMesh') -> '_4726.ConicalGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ConicalGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4726.ConicalGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_conical_gear_mesh_load_case(self, design_entity_analysis: '_6077.ConicalGearMeshLoadCase') -> '_4726.ConicalGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ConicalGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4726.ConicalGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1858.AGMAGleasonConicalGearMesh') -> '_4698.AGMAGleasonConicalGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.AGMAGleasonConicalGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4698.AGMAGleasonConicalGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh_load_case(self, design_entity_analysis: '_6047.AGMAGleasonConicalGearMeshLoadCase') -> '_4698.AGMAGleasonConicalGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.AGMAGleasonConicalGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4698.AGMAGleasonConicalGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1868.CylindricalGearMesh') -> '_4738.CylindricalGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.CylindricalGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4738.CylindricalGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh_load_case(self, design_entity_analysis: '_6090.CylindricalGearMeshLoadCase') -> '_4738.CylindricalGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.CylindricalGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4738.CylindricalGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh(self, design_entity: '_1874.HypoidGearMesh') -> '_4753.HypoidGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.HypoidGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4753.HypoidGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_6131.HypoidGearMeshLoadCase') -> '_4753.HypoidGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.HypoidGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4753.HypoidGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1877.KlingelnbergCycloPalloidConicalGearMesh') -> '_4758.KlingelnbergCycloPalloidConicalGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidConicalGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4758.KlingelnbergCycloPalloidConicalGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh_load_case(self, design_entity_analysis: '_6137.KlingelnbergCycloPalloidConicalGearMeshLoadCase') -> '_4758.KlingelnbergCycloPalloidConicalGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidConicalGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4758.KlingelnbergCycloPalloidConicalGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1878.KlingelnbergCycloPalloidHypoidGearMesh') -> '_4761.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4761.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_6140.KlingelnbergCycloPalloidHypoidGearMeshLoadCase') -> '_4761.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4761.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1879.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> '_4764.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4764.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6143.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase') -> '_4764.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4764.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1882.SpiralBevelGearMesh') -> '_4795.SpiralBevelGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.SpiralBevelGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4795.SpiralBevelGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6176.SpiralBevelGearMeshLoadCase') -> '_4795.SpiralBevelGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.SpiralBevelGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4795.SpiralBevelGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1886.StraightBevelGearMesh') -> '_4804.StraightBevelGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4804.StraightBevelGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6186.StraightBevelGearMeshLoadCase') -> '_4804.StraightBevelGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4804.StraightBevelGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_worm_gear_mesh(self, design_entity: '_1888.WormGearMesh') -> '_4824.WormGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.WormGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4824.WormGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_worm_gear_mesh_load_case(self, design_entity_analysis: '_6207.WormGearMeshLoadCase') -> '_4824.WormGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.WormGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4824.WormGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1890.ZerolBevelGearMesh') -> '_4827.ZerolBevelGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ZerolBevelGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4827.ZerolBevelGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6210.ZerolBevelGearMeshLoadCase') -> '_4827.ZerolBevelGearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ZerolBevelGearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4827.ZerolBevelGearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_gear_mesh(self, design_entity: '_1872.GearMesh') -> '_4749.GearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.GearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4749.GearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_gear_mesh_load_case(self, design_entity_analysis: '_6117.GearMeshLoadCase') -> '_4749.GearMeshModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.GearMeshModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4749.GearMeshModalAnalysis)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_connection(self, design_entity: '_1898.PartToPartShearCouplingConnection') -> '_4777.PartToPartShearCouplingConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.PartToPartShearCouplingConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4777.PartToPartShearCouplingConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_connection_load_case(self, design_entity_analysis: '_6153.PartToPartShearCouplingConnectionLoadCase') -> '_4777.PartToPartShearCouplingConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.PartToPartShearCouplingConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4777.PartToPartShearCouplingConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_clutch_connection(self, design_entity: '_1892.ClutchConnection') -> '_4715.ClutchConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ClutchConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4715.ClutchConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_clutch_connection_load_case(self, design_entity_analysis: '_6064.ClutchConnectionLoadCase') -> '_4715.ClutchConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ClutchConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4715.ClutchConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_concept_coupling_connection(self, design_entity: '_1894.ConceptCouplingConnection') -> '_4720.ConceptCouplingConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ConceptCouplingConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4720.ConceptCouplingConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_concept_coupling_connection_load_case(self, design_entity_analysis: '_6069.ConceptCouplingConnectionLoadCase') -> '_4720.ConceptCouplingConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ConceptCouplingConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4720.ConceptCouplingConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_coupling_connection(self, design_entity: '_1896.CouplingConnection') -> '_4732.CouplingConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.CouplingConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4732.CouplingConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_coupling_connection_load_case(self, design_entity_analysis: '_6082.CouplingConnectionLoadCase') -> '_4732.CouplingConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.CouplingConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4732.CouplingConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_spring_damper_connection(self, design_entity: '_1900.SpringDamperConnection') -> '_4798.SpringDamperConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.SpringDamperConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4798.SpringDamperConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_spring_damper_connection_load_case(self, design_entity_analysis: '_6178.SpringDamperConnectionLoadCase') -> '_4798.SpringDamperConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.SpringDamperConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4798.SpringDamperConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_torque_converter_connection(self, design_entity: '_1902.TorqueConverterConnection') -> '_4813.TorqueConverterConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.TorqueConverterConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4813.TorqueConverterConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_torque_converter_connection_load_case(self, design_entity_analysis: '_6196.TorqueConverterConnectionLoadCase') -> '_4813.TorqueConverterConnectionModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.TorqueConverterConnectionModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4813.TorqueConverterConnectionModalAnalysis)(method_result) if method_result else None

    def results_for_abstract_assembly(self, design_entity: '_1978.AbstractAssembly') -> '_4696.AbstractAssemblyModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.AbstractAssemblyModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4696.AbstractAssemblyModalAnalysis)(method_result) if method_result else None

    def results_for_abstract_assembly_load_case(self, design_entity_analysis: '_6043.AbstractAssemblyLoadCase') -> '_4696.AbstractAssemblyModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.AbstractAssemblyModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4696.AbstractAssemblyModalAnalysis)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing(self, design_entity: '_1979.AbstractShaftOrHousing') -> '_4697.AbstractShaftOrHousingModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.AbstractShaftOrHousingModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4697.AbstractShaftOrHousingModalAnalysis)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing_load_case(self, design_entity_analysis: '_6044.AbstractShaftOrHousingLoadCase') -> '_4697.AbstractShaftOrHousingModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractShaftOrHousingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.AbstractShaftOrHousingModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4697.AbstractShaftOrHousingModalAnalysis)(method_result) if method_result else None

    def results_for_bearing(self, design_entity: '_1982.Bearing') -> '_4702.BearingModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.BearingModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4702.BearingModalAnalysis)(method_result) if method_result else None

    def results_for_bearing_load_case(self, design_entity_analysis: '_6051.BearingLoadCase') -> '_4702.BearingModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.BearingModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4702.BearingModalAnalysis)(method_result) if method_result else None

    def results_for_bolt(self, design_entity: '_1984.Bolt') -> '_4714.BoltModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.BoltModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4714.BoltModalAnalysis)(method_result) if method_result else None

    def results_for_bolt_load_case(self, design_entity_analysis: '_6063.BoltLoadCase') -> '_4714.BoltModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.BoltModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4714.BoltModalAnalysis)(method_result) if method_result else None

    def results_for_bolted_joint(self, design_entity: '_1985.BoltedJoint') -> '_4713.BoltedJointModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.BoltedJointModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4713.BoltedJointModalAnalysis)(method_result) if method_result else None

    def results_for_bolted_joint_load_case(self, design_entity_analysis: '_6062.BoltedJointLoadCase') -> '_4713.BoltedJointModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltedJointLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.BoltedJointModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4713.BoltedJointModalAnalysis)(method_result) if method_result else None

    def results_for_component(self, design_entity: '_1986.Component') -> '_4719.ComponentModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ComponentModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4719.ComponentModalAnalysis)(method_result) if method_result else None

    def results_for_component_load_case(self, design_entity_analysis: '_6068.ComponentLoadCase') -> '_4719.ComponentModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ComponentModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4719.ComponentModalAnalysis)(method_result) if method_result else None

    def results_for_connector(self, design_entity: '_1989.Connector') -> '_4730.ConnectorModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ConnectorModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4730.ConnectorModalAnalysis)(method_result) if method_result else None

    def results_for_connector_load_case(self, design_entity_analysis: '_6081.ConnectorLoadCase') -> '_4730.ConnectorModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectorLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ConnectorModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4730.ConnectorModalAnalysis)(method_result) if method_result else None

    def results_for_datum(self, design_entity: '_1990.Datum') -> '_4742.DatumModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.DatumModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4742.DatumModalAnalysis)(method_result) if method_result else None

    def results_for_datum_load_case(self, design_entity_analysis: '_6096.DatumLoadCase') -> '_4742.DatumModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.DatumLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.DatumModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4742.DatumModalAnalysis)(method_result) if method_result else None

    def results_for_external_cad_model(self, design_entity: '_1993.ExternalCADModel') -> '_4743.ExternalCADModelModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ExternalCADModelModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4743.ExternalCADModelModalAnalysis)(method_result) if method_result else None

    def results_for_external_cad_model_load_case(self, design_entity_analysis: '_6109.ExternalCADModelLoadCase') -> '_4743.ExternalCADModelModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ExternalCADModelModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4743.ExternalCADModelModalAnalysis)(method_result) if method_result else None

    def results_for_flexible_pin_assembly(self, design_entity: '_1994.FlexiblePinAssembly') -> '_4747.FlexiblePinAssemblyModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.FlexiblePinAssemblyModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4747.FlexiblePinAssemblyModalAnalysis)(method_result) if method_result else None

    def results_for_flexible_pin_assembly_load_case(self, design_entity_analysis: '_6113.FlexiblePinAssemblyLoadCase') -> '_4747.FlexiblePinAssemblyModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FlexiblePinAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.FlexiblePinAssemblyModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4747.FlexiblePinAssemblyModalAnalysis)(method_result) if method_result else None

    def results_for_assembly(self, design_entity: '_1977.Assembly') -> '_4701.AssemblyModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.AssemblyModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4701.AssemblyModalAnalysis)(method_result) if method_result else None

    def results_for_assembly_load_case(self, design_entity_analysis: '_6050.AssemblyLoadCase') -> '_4701.AssemblyModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.AssemblyModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4701.AssemblyModalAnalysis)(method_result) if method_result else None

    def results_for_guide_dxf_model(self, design_entity: '_1995.GuideDxfModel') -> '_4752.GuideDxfModelModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.GuideDxfModelModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4752.GuideDxfModelModalAnalysis)(method_result) if method_result else None

    def results_for_guide_dxf_model_load_case(self, design_entity_analysis: '_6121.GuideDxfModelLoadCase') -> '_4752.GuideDxfModelModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GuideDxfModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.GuideDxfModelModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4752.GuideDxfModelModalAnalysis)(method_result) if method_result else None

    def results_for_imported_fe_component(self, design_entity: '_1998.ImportedFEComponent') -> '_4756.ImportedFEComponentModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ImportedFEComponentModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4756.ImportedFEComponentModalAnalysis)(method_result) if method_result else None

    def results_for_imported_fe_component_load_case(self, design_entity_analysis: '_6133.ImportedFEComponentLoadCase') -> '_4756.ImportedFEComponentModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ImportedFEComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ImportedFEComponentModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4756.ImportedFEComponentModalAnalysis)(method_result) if method_result else None

    def results_for_mass_disc(self, design_entity: '_2001.MassDisc') -> '_4767.MassDiscModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.MassDiscModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4767.MassDiscModalAnalysis)(method_result) if method_result else None

    def results_for_mass_disc_load_case(self, design_entity_analysis: '_6145.MassDiscLoadCase') -> '_4767.MassDiscModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MassDiscLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.MassDiscModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4767.MassDiscModalAnalysis)(method_result) if method_result else None

    def results_for_measurement_component(self, design_entity: '_2002.MeasurementComponent') -> '_4768.MeasurementComponentModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.MeasurementComponentModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4768.MeasurementComponentModalAnalysis)(method_result) if method_result else None

    def results_for_measurement_component_load_case(self, design_entity_analysis: '_6146.MeasurementComponentLoadCase') -> '_4768.MeasurementComponentModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MeasurementComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.MeasurementComponentModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4768.MeasurementComponentModalAnalysis)(method_result) if method_result else None

    def results_for_mountable_component(self, design_entity: '_2003.MountableComponent') -> '_4773.MountableComponentModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.MountableComponentModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4773.MountableComponentModalAnalysis)(method_result) if method_result else None

    def results_for_mountable_component_load_case(self, design_entity_analysis: '_6148.MountableComponentLoadCase') -> '_4773.MountableComponentModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MountableComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.MountableComponentModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4773.MountableComponentModalAnalysis)(method_result) if method_result else None

    def results_for_oil_seal(self, design_entity: '_2005.OilSeal') -> '_4774.OilSealModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.OilSealModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4774.OilSealModalAnalysis)(method_result) if method_result else None

    def results_for_oil_seal_load_case(self, design_entity_analysis: '_6150.OilSealLoadCase') -> '_4774.OilSealModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.OilSealModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4774.OilSealModalAnalysis)(method_result) if method_result else None

    def results_for_part(self, design_entity: '_2006.Part') -> '_4776.PartModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.PartModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4776.PartModalAnalysis)(method_result) if method_result else None

    def results_for_part_load_case(self, design_entity_analysis: '_6152.PartLoadCase') -> '_4776.PartModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.PartModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4776.PartModalAnalysis)(method_result) if method_result else None

    def results_for_planet_carrier(self, design_entity: '_2007.PlanetCarrier') -> '_4782.PlanetCarrierModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.PlanetCarrierModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4782.PlanetCarrierModalAnalysis)(method_result) if method_result else None

    def results_for_planet_carrier_load_case(self, design_entity_analysis: '_6159.PlanetCarrierLoadCase') -> '_4782.PlanetCarrierModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.PlanetCarrierModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4782.PlanetCarrierModalAnalysis)(method_result) if method_result else None

    def results_for_point_load(self, design_entity: '_2009.PointLoad') -> '_4783.PointLoadModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.PointLoadModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4783.PointLoadModalAnalysis)(method_result) if method_result else None

    def results_for_point_load_load_case(self, design_entity_analysis: '_6162.PointLoadLoadCase') -> '_4783.PointLoadModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.PointLoadModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4783.PointLoadModalAnalysis)(method_result) if method_result else None

    def results_for_power_load(self, design_entity: '_2010.PowerLoad') -> '_4784.PowerLoadModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.PowerLoadModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4784.PowerLoadModalAnalysis)(method_result) if method_result else None

    def results_for_power_load_load_case(self, design_entity_analysis: '_6163.PowerLoadLoadCase') -> '_4784.PowerLoadModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.PowerLoadModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4784.PowerLoadModalAnalysis)(method_result) if method_result else None

    def results_for_root_assembly(self, design_entity: '_2012.RootAssembly') -> '_4789.RootAssemblyModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.RootAssemblyModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4789.RootAssemblyModalAnalysis)(method_result) if method_result else None

    def results_for_root_assembly_load_case(self, design_entity_analysis: '_6169.RootAssemblyLoadCase') -> '_4789.RootAssemblyModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RootAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.RootAssemblyModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4789.RootAssemblyModalAnalysis)(method_result) if method_result else None

    def results_for_specialised_assembly(self, design_entity: '_2014.SpecialisedAssembly') -> '_4794.SpecialisedAssemblyModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.SpecialisedAssemblyModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4794.SpecialisedAssemblyModalAnalysis)(method_result) if method_result else None

    def results_for_specialised_assembly_load_case(self, design_entity_analysis: '_6173.SpecialisedAssemblyLoadCase') -> '_4794.SpecialisedAssemblyModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpecialisedAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.SpecialisedAssemblyModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4794.SpecialisedAssemblyModalAnalysis)(method_result) if method_result else None

    def results_for_unbalanced_mass(self, design_entity: '_2015.UnbalancedMass') -> '_4817.UnbalancedMassModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.UnbalancedMassModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4817.UnbalancedMassModalAnalysis)(method_result) if method_result else None

    def results_for_unbalanced_mass_load_case(self, design_entity_analysis: '_6204.UnbalancedMassLoadCase') -> '_4817.UnbalancedMassModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.UnbalancedMassLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.UnbalancedMassModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4817.UnbalancedMassModalAnalysis)(method_result) if method_result else None

    def results_for_virtual_component(self, design_entity: '_2016.VirtualComponent') -> '_4818.VirtualComponentModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.VirtualComponentModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4818.VirtualComponentModalAnalysis)(method_result) if method_result else None

    def results_for_virtual_component_load_case(self, design_entity_analysis: '_6205.VirtualComponentLoadCase') -> '_4818.VirtualComponentModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.VirtualComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.VirtualComponentModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4818.VirtualComponentModalAnalysis)(method_result) if method_result else None

    def results_for_shaft(self, design_entity: '_2019.Shaft') -> '_4791.ShaftModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ShaftModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4791.ShaftModalAnalysis)(method_result) if method_result else None

    def results_for_shaft_load_case(self, design_entity_analysis: '_6171.ShaftLoadCase') -> '_4791.ShaftModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ShaftModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4791.ShaftModalAnalysis)(method_result) if method_result else None

    def results_for_concept_gear(self, design_entity: '_2057.ConceptGear') -> '_4724.ConceptGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ConceptGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4724.ConceptGearModalAnalysis)(method_result) if method_result else None

    def results_for_concept_gear_load_case(self, design_entity_analysis: '_6072.ConceptGearLoadCase') -> '_4724.ConceptGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ConceptGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4724.ConceptGearModalAnalysis)(method_result) if method_result else None

    def results_for_concept_gear_set(self, design_entity: '_2058.ConceptGearSet') -> '_4725.ConceptGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ConceptGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4725.ConceptGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_concept_gear_set_load_case(self, design_entity_analysis: '_6074.ConceptGearSetLoadCase') -> '_4725.ConceptGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ConceptGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4725.ConceptGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_face_gear(self, design_entity: '_2064.FaceGear') -> '_4745.FaceGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.FaceGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4745.FaceGearModalAnalysis)(method_result) if method_result else None

    def results_for_face_gear_load_case(self, design_entity_analysis: '_6110.FaceGearLoadCase') -> '_4745.FaceGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.FaceGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4745.FaceGearModalAnalysis)(method_result) if method_result else None

    def results_for_face_gear_set(self, design_entity: '_2065.FaceGearSet') -> '_4746.FaceGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.FaceGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4746.FaceGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_face_gear_set_load_case(self, design_entity_analysis: '_6112.FaceGearSetLoadCase') -> '_4746.FaceGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.FaceGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4746.FaceGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear(self, design_entity: '_2049.AGMAGleasonConicalGear') -> '_4699.AGMAGleasonConicalGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.AGMAGleasonConicalGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4699.AGMAGleasonConicalGearModalAnalysis)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_load_case(self, design_entity_analysis: '_6046.AGMAGleasonConicalGearLoadCase') -> '_4699.AGMAGleasonConicalGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.AGMAGleasonConicalGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4699.AGMAGleasonConicalGearModalAnalysis)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_2050.AGMAGleasonConicalGearSet') -> '_4700.AGMAGleasonConicalGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.AGMAGleasonConicalGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4700.AGMAGleasonConicalGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set_load_case(self, design_entity_analysis: '_6048.AGMAGleasonConicalGearSetLoadCase') -> '_4700.AGMAGleasonConicalGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.AGMAGleasonConicalGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4700.AGMAGleasonConicalGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_gear(self, design_entity: '_2051.BevelDifferentialGear') -> '_4706.BevelDifferentialGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.BevelDifferentialGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4706.BevelDifferentialGearModalAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_gear_load_case(self, design_entity_analysis: '_6054.BevelDifferentialGearLoadCase') -> '_4706.BevelDifferentialGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.BevelDifferentialGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4706.BevelDifferentialGearModalAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set(self, design_entity: '_2052.BevelDifferentialGearSet') -> '_4707.BevelDifferentialGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.BevelDifferentialGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4707.BevelDifferentialGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set_load_case(self, design_entity_analysis: '_6056.BevelDifferentialGearSetLoadCase') -> '_4707.BevelDifferentialGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.BevelDifferentialGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4707.BevelDifferentialGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2053.BevelDifferentialPlanetGear') -> '_4708.BevelDifferentialPlanetGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.BevelDifferentialPlanetGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4708.BevelDifferentialPlanetGearModalAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear_load_case(self, design_entity_analysis: '_6057.BevelDifferentialPlanetGearLoadCase') -> '_4708.BevelDifferentialPlanetGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.BevelDifferentialPlanetGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4708.BevelDifferentialPlanetGearModalAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2054.BevelDifferentialSunGear') -> '_4709.BevelDifferentialSunGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.BevelDifferentialSunGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4709.BevelDifferentialSunGearModalAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear_load_case(self, design_entity_analysis: '_6058.BevelDifferentialSunGearLoadCase') -> '_4709.BevelDifferentialSunGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.BevelDifferentialSunGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4709.BevelDifferentialSunGearModalAnalysis)(method_result) if method_result else None

    def results_for_bevel_gear(self, design_entity: '_2055.BevelGear') -> '_4711.BevelGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.BevelGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4711.BevelGearModalAnalysis)(method_result) if method_result else None

    def results_for_bevel_gear_load_case(self, design_entity_analysis: '_6059.BevelGearLoadCase') -> '_4711.BevelGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.BevelGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4711.BevelGearModalAnalysis)(method_result) if method_result else None

    def results_for_bevel_gear_set(self, design_entity: '_2056.BevelGearSet') -> '_4712.BevelGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.BevelGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4712.BevelGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_bevel_gear_set_load_case(self, design_entity_analysis: '_6061.BevelGearSetLoadCase') -> '_4712.BevelGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.BevelGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4712.BevelGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_conical_gear(self, design_entity: '_2059.ConicalGear') -> '_4727.ConicalGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ConicalGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4727.ConicalGearModalAnalysis)(method_result) if method_result else None

    def results_for_conical_gear_load_case(self, design_entity_analysis: '_6075.ConicalGearLoadCase') -> '_4727.ConicalGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ConicalGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4727.ConicalGearModalAnalysis)(method_result) if method_result else None

    def results_for_conical_gear_set(self, design_entity: '_2060.ConicalGearSet') -> '_4728.ConicalGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ConicalGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4728.ConicalGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_conical_gear_set_load_case(self, design_entity_analysis: '_6079.ConicalGearSetLoadCase') -> '_4728.ConicalGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.ConicalGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4728.ConicalGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_gear(self, design_entity: '_2061.CylindricalGear') -> '_4739.CylindricalGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.CylindricalGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4739.CylindricalGearModalAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_gear_load_case(self, design_entity_analysis: '_6088.CylindricalGearLoadCase') -> '_4739.CylindricalGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.CylindricalGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4739.CylindricalGearModalAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_gear_set(self, design_entity: '_2062.CylindricalGearSet') -> '_4740.CylindricalGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.CylindricalGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4740.CylindricalGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_gear_set_load_case(self, design_entity_analysis: '_6092.CylindricalGearSetLoadCase') -> '_4740.CylindricalGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.CylindricalGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4740.CylindricalGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear(self, design_entity: '_2063.CylindricalPlanetGear') -> '_4741.CylindricalPlanetGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.CylindricalPlanetGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4741.CylindricalPlanetGearModalAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear_load_case(self, design_entity_analysis: '_6093.CylindricalPlanetGearLoadCase') -> '_4741.CylindricalPlanetGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.CylindricalPlanetGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4741.CylindricalPlanetGearModalAnalysis)(method_result) if method_result else None

    def results_for_gear(self, design_entity: '_2066.Gear') -> '_4750.GearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.GearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4750.GearModalAnalysis)(method_result) if method_result else None

    def results_for_gear_load_case(self, design_entity_analysis: '_6115.GearLoadCase') -> '_4750.GearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.GearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4750.GearModalAnalysis)(method_result) if method_result else None

    def results_for_gear_set(self, design_entity: '_2068.GearSet') -> '_4751.GearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.GearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4751.GearSetModalAnalysis)(method_result) if method_result else None

    def results_for_gear_set_load_case(self, design_entity_analysis: '_6120.GearSetLoadCase') -> '_4751.GearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.GearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4751.GearSetModalAnalysis)(method_result) if method_result else None

    def results_for_hypoid_gear(self, design_entity: '_2070.HypoidGear') -> '_4754.HypoidGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.HypoidGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4754.HypoidGearModalAnalysis)(method_result) if method_result else None

    def results_for_hypoid_gear_load_case(self, design_entity_analysis: '_6130.HypoidGearLoadCase') -> '_4754.HypoidGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.HypoidGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4754.HypoidGearModalAnalysis)(method_result) if method_result else None

    def results_for_hypoid_gear_set(self, design_entity: '_2071.HypoidGearSet') -> '_4755.HypoidGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.HypoidGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4755.HypoidGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_hypoid_gear_set_load_case(self, design_entity_analysis: '_6132.HypoidGearSetLoadCase') -> '_4755.HypoidGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.HypoidGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4755.HypoidGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2072.KlingelnbergCycloPalloidConicalGear') -> '_4759.KlingelnbergCycloPalloidConicalGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidConicalGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4759.KlingelnbergCycloPalloidConicalGearModalAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_load_case(self, design_entity_analysis: '_6136.KlingelnbergCycloPalloidConicalGearLoadCase') -> '_4759.KlingelnbergCycloPalloidConicalGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidConicalGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4759.KlingelnbergCycloPalloidConicalGearModalAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2073.KlingelnbergCycloPalloidConicalGearSet') -> '_4760.KlingelnbergCycloPalloidConicalGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidConicalGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4760.KlingelnbergCycloPalloidConicalGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set_load_case(self, design_entity_analysis: '_6138.KlingelnbergCycloPalloidConicalGearSetLoadCase') -> '_4760.KlingelnbergCycloPalloidConicalGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidConicalGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4760.KlingelnbergCycloPalloidConicalGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2074.KlingelnbergCycloPalloidHypoidGear') -> '_4762.KlingelnbergCycloPalloidHypoidGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidHypoidGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4762.KlingelnbergCycloPalloidHypoidGearModalAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_load_case(self, design_entity_analysis: '_6139.KlingelnbergCycloPalloidHypoidGearLoadCase') -> '_4762.KlingelnbergCycloPalloidHypoidGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidHypoidGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4762.KlingelnbergCycloPalloidHypoidGearModalAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2075.KlingelnbergCycloPalloidHypoidGearSet') -> '_4763.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4763.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(self, design_entity_analysis: '_6141.KlingelnbergCycloPalloidHypoidGearSetLoadCase') -> '_4763.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4763.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2076.KlingelnbergCycloPalloidSpiralBevelGear') -> '_4765.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4765.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(self, design_entity_analysis: '_6142.KlingelnbergCycloPalloidSpiralBevelGearLoadCase') -> '_4765.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4765.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2077.KlingelnbergCycloPalloidSpiralBevelGearSet') -> '_4766.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4766.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_6144.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase') -> '_4766.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4766.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_planetary_gear_set(self, design_entity: '_2078.PlanetaryGearSet') -> '_4781.PlanetaryGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.PlanetaryGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4781.PlanetaryGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_planetary_gear_set_load_case(self, design_entity_analysis: '_6157.PlanetaryGearSetLoadCase') -> '_4781.PlanetaryGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.PlanetaryGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4781.PlanetaryGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_spiral_bevel_gear(self, design_entity: '_2079.SpiralBevelGear') -> '_4796.SpiralBevelGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.SpiralBevelGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4796.SpiralBevelGearModalAnalysis)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_load_case(self, design_entity_analysis: '_6175.SpiralBevelGearLoadCase') -> '_4796.SpiralBevelGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.SpiralBevelGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4796.SpiralBevelGearModalAnalysis)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set(self, design_entity: '_2080.SpiralBevelGearSet') -> '_4797.SpiralBevelGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.SpiralBevelGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4797.SpiralBevelGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_6177.SpiralBevelGearSetLoadCase') -> '_4797.SpiralBevelGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.SpiralBevelGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4797.SpiralBevelGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2081.StraightBevelDiffGear') -> '_4802.StraightBevelDiffGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelDiffGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4802.StraightBevelDiffGearModalAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_load_case(self, design_entity_analysis: '_6182.StraightBevelDiffGearLoadCase') -> '_4802.StraightBevelDiffGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelDiffGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4802.StraightBevelDiffGearModalAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_2082.StraightBevelDiffGearSet') -> '_4803.StraightBevelDiffGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelDiffGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4803.StraightBevelDiffGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set_load_case(self, design_entity_analysis: '_6184.StraightBevelDiffGearSetLoadCase') -> '_4803.StraightBevelDiffGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelDiffGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4803.StraightBevelDiffGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_gear(self, design_entity: '_2083.StraightBevelGear') -> '_4805.StraightBevelGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4805.StraightBevelGearModalAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_gear_load_case(self, design_entity_analysis: '_6185.StraightBevelGearLoadCase') -> '_4805.StraightBevelGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4805.StraightBevelGearModalAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set(self, design_entity: '_2084.StraightBevelGearSet') -> '_4806.StraightBevelGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4806.StraightBevelGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set_load_case(self, design_entity_analysis: '_6187.StraightBevelGearSetLoadCase') -> '_4806.StraightBevelGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4806.StraightBevelGearSetModalAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2085.StraightBevelPlanetGear') -> '_4807.StraightBevelPlanetGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelPlanetGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4807.StraightBevelPlanetGearModalAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear_load_case(self, design_entity_analysis: '_6188.StraightBevelPlanetGearLoadCase') -> '_4807.StraightBevelPlanetGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelPlanetGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4807.StraightBevelPlanetGearModalAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2086.StraightBevelSunGear') -> '_4808.StraightBevelSunGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelSunGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4808.StraightBevelSunGearModalAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear_load_case(self, design_entity_analysis: '_6189.StraightBevelSunGearLoadCase') -> '_4808.StraightBevelSunGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.StraightBevelSunGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4808.StraightBevelSunGearModalAnalysis)(method_result) if method_result else None

    def results_for_worm_gear(self, design_entity: '_2087.WormGear') -> '_4825.WormGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.WormGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4825.WormGearModalAnalysis)(method_result) if method_result else None

    def results_for_worm_gear_load_case(self, design_entity_analysis: '_6206.WormGearLoadCase') -> '_4825.WormGearModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.WormGearModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4825.WormGearModalAnalysis)(method_result) if method_result else None

    def results_for_worm_gear_set(self, design_entity: '_2088.WormGearSet') -> '_4826.WormGearSetModalAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.modal_analyses.WormGearSetModalAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4826.WormGearSetModalAnalysis)(method_result) if method_result else None
