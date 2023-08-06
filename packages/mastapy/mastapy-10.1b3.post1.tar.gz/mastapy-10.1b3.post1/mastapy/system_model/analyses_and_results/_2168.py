'''_2168.py

PowerFlowAnalysis
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
from mastapy.system_model.analyses_and_results.power_flows import (
    _3334, _3336, _3337, _3290,
    _3289, _3221, _3234, _3233,
    _3239, _3238, _3250, _3249,
    _3252, _3253, _3298, _3303,
    _3301, _3299, _3312, _3311,
    _3323, _3321, _3322, _3324,
    _3327, _3328, _3329, _3251,
    _3220, _3235, _3246, _3273,
    _3291, _3300, _3305, _3222,
    _3240, _3261, _3313, _3227,
    _3243, _3215, _3255, _3269,
    _3274, _3277, _3280, _3307,
    _3316, _3332, _3335, _3265,
    _3288, _3232, _3237, _3248,
    _3310, _3326, _3213, _3214,
    _3219, _3231, _3230, _3236,
    _3247, _3259, _3260, _3264,
    _3218, _3268, _3272, _3283,
    _3284, _3285, _3286, _3287,
    _3293, _3294, _3297, _3302,
    _3306, _3330, _3331, _3304,
    _3241, _3242, _3262, _3263,
    _3216, _3217, _3223, _3224,
    _3225, _3226, _3228, _3229,
    _3244, _3245, _3256, _3257,
    _3258, _3266, _3267, _3270,
    _3271, _3275, _3276, _3278,
    _3279, _3281, _3282, _3292,
    _3308, _3309, _3314, _3315,
    _3317, _3318, _3319, _3320,
    _3333
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

_POWER_FLOW_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'PowerFlowAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerFlowAnalysis',)


class PowerFlowAnalysis(_2150.SingleAnalysis):
    '''PowerFlowAnalysis

    This is a mastapy class.
    '''

    TYPE = _POWER_FLOW_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerFlowAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    def results_for_worm_gear_set_load_case(self, design_entity_analysis: '_6208.WormGearSetLoadCase') -> '_3334.WormGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.WormGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3334.WormGearSetPowerFlow)(method_result) if method_result else None

    def results_for_zerol_bevel_gear(self, design_entity: '_2089.ZerolBevelGear') -> '_3336.ZerolBevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ZerolBevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3336.ZerolBevelGearPowerFlow)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_load_case(self, design_entity_analysis: '_6209.ZerolBevelGearLoadCase') -> '_3336.ZerolBevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ZerolBevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3336.ZerolBevelGearPowerFlow)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set(self, design_entity: '_2090.ZerolBevelGearSet') -> '_3337.ZerolBevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ZerolBevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3337.ZerolBevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set_load_case(self, design_entity_analysis: '_6211.ZerolBevelGearSetLoadCase') -> '_3337.ZerolBevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ZerolBevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3337.ZerolBevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling(self, design_entity: '_2119.PartToPartShearCoupling') -> '_3290.PartToPartShearCouplingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PartToPartShearCouplingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3290.PartToPartShearCouplingPowerFlow)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_load_case(self, design_entity_analysis: '_6155.PartToPartShearCouplingLoadCase') -> '_3290.PartToPartShearCouplingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PartToPartShearCouplingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3290.PartToPartShearCouplingPowerFlow)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_half(self, design_entity: '_2120.PartToPartShearCouplingHalf') -> '_3289.PartToPartShearCouplingHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PartToPartShearCouplingHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3289.PartToPartShearCouplingHalfPowerFlow)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_half_load_case(self, design_entity_analysis: '_6154.PartToPartShearCouplingHalfLoadCase') -> '_3289.PartToPartShearCouplingHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PartToPartShearCouplingHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3289.PartToPartShearCouplingHalfPowerFlow)(method_result) if method_result else None

    def results_for_belt_drive(self, design_entity: '_2108.BeltDrive') -> '_3221.BeltDrivePowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BeltDrivePowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3221.BeltDrivePowerFlow)(method_result) if method_result else None

    def results_for_belt_drive_load_case(self, design_entity_analysis: '_6053.BeltDriveLoadCase') -> '_3221.BeltDrivePowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltDriveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BeltDrivePowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3221.BeltDrivePowerFlow)(method_result) if method_result else None

    def results_for_clutch(self, design_entity: '_2110.Clutch') -> '_3234.ClutchPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ClutchPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3234.ClutchPowerFlow)(method_result) if method_result else None

    def results_for_clutch_load_case(self, design_entity_analysis: '_6066.ClutchLoadCase') -> '_3234.ClutchPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ClutchPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3234.ClutchPowerFlow)(method_result) if method_result else None

    def results_for_clutch_half(self, design_entity: '_2111.ClutchHalf') -> '_3233.ClutchHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ClutchHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3233.ClutchHalfPowerFlow)(method_result) if method_result else None

    def results_for_clutch_half_load_case(self, design_entity_analysis: '_6065.ClutchHalfLoadCase') -> '_3233.ClutchHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ClutchHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3233.ClutchHalfPowerFlow)(method_result) if method_result else None

    def results_for_concept_coupling(self, design_entity: '_2113.ConceptCoupling') -> '_3239.ConceptCouplingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptCouplingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3239.ConceptCouplingPowerFlow)(method_result) if method_result else None

    def results_for_concept_coupling_load_case(self, design_entity_analysis: '_6071.ConceptCouplingLoadCase') -> '_3239.ConceptCouplingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptCouplingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3239.ConceptCouplingPowerFlow)(method_result) if method_result else None

    def results_for_concept_coupling_half(self, design_entity: '_2114.ConceptCouplingHalf') -> '_3238.ConceptCouplingHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptCouplingHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3238.ConceptCouplingHalfPowerFlow)(method_result) if method_result else None

    def results_for_concept_coupling_half_load_case(self, design_entity_analysis: '_6070.ConceptCouplingHalfLoadCase') -> '_3238.ConceptCouplingHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptCouplingHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3238.ConceptCouplingHalfPowerFlow)(method_result) if method_result else None

    def results_for_coupling(self, design_entity: '_2115.Coupling') -> '_3250.CouplingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CouplingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3250.CouplingPowerFlow)(method_result) if method_result else None

    def results_for_coupling_load_case(self, design_entity_analysis: '_6084.CouplingLoadCase') -> '_3250.CouplingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CouplingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3250.CouplingPowerFlow)(method_result) if method_result else None

    def results_for_coupling_half(self, design_entity: '_2116.CouplingHalf') -> '_3249.CouplingHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CouplingHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3249.CouplingHalfPowerFlow)(method_result) if method_result else None

    def results_for_coupling_half_load_case(self, design_entity_analysis: '_6083.CouplingHalfLoadCase') -> '_3249.CouplingHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CouplingHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3249.CouplingHalfPowerFlow)(method_result) if method_result else None

    def results_for_cvt(self, design_entity: '_2117.CVT') -> '_3252.CVTPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CVTPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3252.CVTPowerFlow)(method_result) if method_result else None

    def results_for_cvt_load_case(self, design_entity_analysis: '_6086.CVTLoadCase') -> '_3252.CVTPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CVTPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3252.CVTPowerFlow)(method_result) if method_result else None

    def results_for_cvt_pulley(self, design_entity: '_2118.CVTPulley') -> '_3253.CVTPulleyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CVTPulleyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3253.CVTPulleyPowerFlow)(method_result) if method_result else None

    def results_for_cvt_pulley_load_case(self, design_entity_analysis: '_6087.CVTPulleyLoadCase') -> '_3253.CVTPulleyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTPulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CVTPulleyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3253.CVTPulleyPowerFlow)(method_result) if method_result else None

    def results_for_pulley(self, design_entity: '_2121.Pulley') -> '_3298.PulleyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PulleyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3298.PulleyPowerFlow)(method_result) if method_result else None

    def results_for_pulley_load_case(self, design_entity_analysis: '_6164.PulleyLoadCase') -> '_3298.PulleyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PulleyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3298.PulleyPowerFlow)(method_result) if method_result else None

    def results_for_shaft_hub_connection(self, design_entity: '_2129.ShaftHubConnection') -> '_3303.ShaftHubConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ShaftHubConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3303.ShaftHubConnectionPowerFlow)(method_result) if method_result else None

    def results_for_shaft_hub_connection_load_case(self, design_entity_analysis: '_6170.ShaftHubConnectionLoadCase') -> '_3303.ShaftHubConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ShaftHubConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3303.ShaftHubConnectionPowerFlow)(method_result) if method_result else None

    def results_for_rolling_ring(self, design_entity: '_2127.RollingRing') -> '_3301.RollingRingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.RollingRingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3301.RollingRingPowerFlow)(method_result) if method_result else None

    def results_for_rolling_ring_load_case(self, design_entity_analysis: '_6168.RollingRingLoadCase') -> '_3301.RollingRingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.RollingRingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3301.RollingRingPowerFlow)(method_result) if method_result else None

    def results_for_rolling_ring_assembly(self, design_entity: '_2128.RollingRingAssembly') -> '_3299.RollingRingAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.RollingRingAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3299.RollingRingAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_rolling_ring_assembly_load_case(self, design_entity_analysis: '_6166.RollingRingAssemblyLoadCase') -> '_3299.RollingRingAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.RollingRingAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3299.RollingRingAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_spring_damper(self, design_entity: '_2130.SpringDamper') -> '_3312.SpringDamperPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpringDamperPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3312.SpringDamperPowerFlow)(method_result) if method_result else None

    def results_for_spring_damper_load_case(self, design_entity_analysis: '_6180.SpringDamperLoadCase') -> '_3312.SpringDamperPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpringDamperPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3312.SpringDamperPowerFlow)(method_result) if method_result else None

    def results_for_spring_damper_half(self, design_entity: '_2131.SpringDamperHalf') -> '_3311.SpringDamperHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpringDamperHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3311.SpringDamperHalfPowerFlow)(method_result) if method_result else None

    def results_for_spring_damper_half_load_case(self, design_entity_analysis: '_6179.SpringDamperHalfLoadCase') -> '_3311.SpringDamperHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpringDamperHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3311.SpringDamperHalfPowerFlow)(method_result) if method_result else None

    def results_for_synchroniser(self, design_entity: '_2132.Synchroniser') -> '_3323.SynchroniserPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SynchroniserPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3323.SynchroniserPowerFlow)(method_result) if method_result else None

    def results_for_synchroniser_load_case(self, design_entity_analysis: '_6191.SynchroniserLoadCase') -> '_3323.SynchroniserPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SynchroniserPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3323.SynchroniserPowerFlow)(method_result) if method_result else None

    def results_for_synchroniser_half(self, design_entity: '_2134.SynchroniserHalf') -> '_3321.SynchroniserHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SynchroniserHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3321.SynchroniserHalfPowerFlow)(method_result) if method_result else None

    def results_for_synchroniser_half_load_case(self, design_entity_analysis: '_6190.SynchroniserHalfLoadCase') -> '_3321.SynchroniserHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SynchroniserHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3321.SynchroniserHalfPowerFlow)(method_result) if method_result else None

    def results_for_synchroniser_part(self, design_entity: '_2135.SynchroniserPart') -> '_3322.SynchroniserPartPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SynchroniserPartPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3322.SynchroniserPartPowerFlow)(method_result) if method_result else None

    def results_for_synchroniser_part_load_case(self, design_entity_analysis: '_6192.SynchroniserPartLoadCase') -> '_3322.SynchroniserPartPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserPartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SynchroniserPartPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3322.SynchroniserPartPowerFlow)(method_result) if method_result else None

    def results_for_synchroniser_sleeve(self, design_entity: '_2136.SynchroniserSleeve') -> '_3324.SynchroniserSleevePowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SynchroniserSleevePowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3324.SynchroniserSleevePowerFlow)(method_result) if method_result else None

    def results_for_synchroniser_sleeve_load_case(self, design_entity_analysis: '_6193.SynchroniserSleeveLoadCase') -> '_3324.SynchroniserSleevePowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserSleeveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SynchroniserSleevePowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3324.SynchroniserSleevePowerFlow)(method_result) if method_result else None

    def results_for_torque_converter(self, design_entity: '_2137.TorqueConverter') -> '_3327.TorqueConverterPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.TorqueConverterPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3327.TorqueConverterPowerFlow)(method_result) if method_result else None

    def results_for_torque_converter_load_case(self, design_entity_analysis: '_6197.TorqueConverterLoadCase') -> '_3327.TorqueConverterPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.TorqueConverterPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3327.TorqueConverterPowerFlow)(method_result) if method_result else None

    def results_for_torque_converter_pump(self, design_entity: '_2138.TorqueConverterPump') -> '_3328.TorqueConverterPumpPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.TorqueConverterPumpPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3328.TorqueConverterPumpPowerFlow)(method_result) if method_result else None

    def results_for_torque_converter_pump_load_case(self, design_entity_analysis: '_6198.TorqueConverterPumpLoadCase') -> '_3328.TorqueConverterPumpPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterPumpLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.TorqueConverterPumpPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3328.TorqueConverterPumpPowerFlow)(method_result) if method_result else None

    def results_for_torque_converter_turbine(self, design_entity: '_2140.TorqueConverterTurbine') -> '_3329.TorqueConverterTurbinePowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.TorqueConverterTurbinePowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3329.TorqueConverterTurbinePowerFlow)(method_result) if method_result else None

    def results_for_torque_converter_turbine_load_case(self, design_entity_analysis: '_6199.TorqueConverterTurbineLoadCase') -> '_3329.TorqueConverterTurbinePowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterTurbineLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.TorqueConverterTurbinePowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3329.TorqueConverterTurbinePowerFlow)(method_result) if method_result else None

    def results_for_cvt_belt_connection(self, design_entity: '_1835.CVTBeltConnection') -> '_3251.CVTBeltConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CVTBeltConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3251.CVTBeltConnectionPowerFlow)(method_result) if method_result else None

    def results_for_cvt_belt_connection_load_case(self, design_entity_analysis: '_6085.CVTBeltConnectionLoadCase') -> '_3251.CVTBeltConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTBeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CVTBeltConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3251.CVTBeltConnectionPowerFlow)(method_result) if method_result else None

    def results_for_belt_connection(self, design_entity: '_1830.BeltConnection') -> '_3220.BeltConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BeltConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3220.BeltConnectionPowerFlow)(method_result) if method_result else None

    def results_for_belt_connection_load_case(self, design_entity_analysis: '_6052.BeltConnectionLoadCase') -> '_3220.BeltConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BeltConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3220.BeltConnectionPowerFlow)(method_result) if method_result else None

    def results_for_coaxial_connection(self, design_entity: '_1831.CoaxialConnection') -> '_3235.CoaxialConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CoaxialConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3235.CoaxialConnectionPowerFlow)(method_result) if method_result else None

    def results_for_coaxial_connection_load_case(self, design_entity_analysis: '_6067.CoaxialConnectionLoadCase') -> '_3235.CoaxialConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CoaxialConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3235.CoaxialConnectionPowerFlow)(method_result) if method_result else None

    def results_for_connection(self, design_entity: '_1834.Connection') -> '_3246.ConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3246.ConnectionPowerFlow)(method_result) if method_result else None

    def results_for_connection_load_case(self, design_entity_analysis: '_6080.ConnectionLoadCase') -> '_3246.ConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3246.ConnectionPowerFlow)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection(self, design_entity: '_1843.InterMountableComponentConnection') -> '_3273.InterMountableComponentConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.InterMountableComponentConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3273.InterMountableComponentConnectionPowerFlow)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection_load_case(self, design_entity_analysis: '_6135.InterMountableComponentConnectionLoadCase') -> '_3273.InterMountableComponentConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.InterMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.InterMountableComponentConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3273.InterMountableComponentConnectionPowerFlow)(method_result) if method_result else None

    def results_for_planetary_connection(self, design_entity: '_1846.PlanetaryConnection') -> '_3291.PlanetaryConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PlanetaryConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3291.PlanetaryConnectionPowerFlow)(method_result) if method_result else None

    def results_for_planetary_connection_load_case(self, design_entity_analysis: '_6156.PlanetaryConnectionLoadCase') -> '_3291.PlanetaryConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PlanetaryConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3291.PlanetaryConnectionPowerFlow)(method_result) if method_result else None

    def results_for_rolling_ring_connection(self, design_entity: '_1850.RollingRingConnection') -> '_3300.RollingRingConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.RollingRingConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3300.RollingRingConnectionPowerFlow)(method_result) if method_result else None

    def results_for_rolling_ring_connection_load_case(self, design_entity_analysis: '_6167.RollingRingConnectionLoadCase') -> '_3300.RollingRingConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.RollingRingConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3300.RollingRingConnectionPowerFlow)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1854.ShaftToMountableComponentConnection') -> '_3305.ShaftToMountableComponentConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ShaftToMountableComponentConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3305.ShaftToMountableComponentConnectionPowerFlow)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection_load_case(self, design_entity_analysis: '_6172.ShaftToMountableComponentConnectionLoadCase') -> '_3305.ShaftToMountableComponentConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftToMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ShaftToMountableComponentConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3305.ShaftToMountableComponentConnectionPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1860.BevelDifferentialGearMesh') -> '_3222.BevelDifferentialGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3222.BevelDifferentialGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh_load_case(self, design_entity_analysis: '_6055.BevelDifferentialGearMeshLoadCase') -> '_3222.BevelDifferentialGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3222.BevelDifferentialGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_concept_gear_mesh(self, design_entity: '_1864.ConceptGearMesh') -> '_3240.ConceptGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3240.ConceptGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_concept_gear_mesh_load_case(self, design_entity_analysis: '_6073.ConceptGearMeshLoadCase') -> '_3240.ConceptGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3240.ConceptGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_face_gear_mesh(self, design_entity: '_1870.FaceGearMesh') -> '_3261.FaceGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.FaceGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3261.FaceGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_face_gear_mesh_load_case(self, design_entity_analysis: '_6111.FaceGearMeshLoadCase') -> '_3261.FaceGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.FaceGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3261.FaceGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1884.StraightBevelDiffGearMesh') -> '_3313.StraightBevelDiffGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelDiffGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3313.StraightBevelDiffGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh_load_case(self, design_entity_analysis: '_6183.StraightBevelDiffGearMeshLoadCase') -> '_3313.StraightBevelDiffGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelDiffGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3313.StraightBevelDiffGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_bevel_gear_mesh(self, design_entity: '_1862.BevelGearMesh') -> '_3227.BevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3227.BevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6060.BevelGearMeshLoadCase') -> '_3227.BevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3227.BevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_conical_gear_mesh(self, design_entity: '_1866.ConicalGearMesh') -> '_3243.ConicalGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConicalGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3243.ConicalGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_conical_gear_mesh_load_case(self, design_entity_analysis: '_6077.ConicalGearMeshLoadCase') -> '_3243.ConicalGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConicalGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3243.ConicalGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1858.AGMAGleasonConicalGearMesh') -> '_3215.AGMAGleasonConicalGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AGMAGleasonConicalGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3215.AGMAGleasonConicalGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh_load_case(self, design_entity_analysis: '_6047.AGMAGleasonConicalGearMeshLoadCase') -> '_3215.AGMAGleasonConicalGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AGMAGleasonConicalGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3215.AGMAGleasonConicalGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1868.CylindricalGearMesh') -> '_3255.CylindricalGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CylindricalGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3255.CylindricalGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh_load_case(self, design_entity_analysis: '_6090.CylindricalGearMeshLoadCase') -> '_3255.CylindricalGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CylindricalGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3255.CylindricalGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh(self, design_entity: '_1874.HypoidGearMesh') -> '_3269.HypoidGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.HypoidGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3269.HypoidGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_6131.HypoidGearMeshLoadCase') -> '_3269.HypoidGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.HypoidGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3269.HypoidGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1877.KlingelnbergCycloPalloidConicalGearMesh') -> '_3274.KlingelnbergCycloPalloidConicalGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidConicalGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3274.KlingelnbergCycloPalloidConicalGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh_load_case(self, design_entity_analysis: '_6137.KlingelnbergCycloPalloidConicalGearMeshLoadCase') -> '_3274.KlingelnbergCycloPalloidConicalGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidConicalGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3274.KlingelnbergCycloPalloidConicalGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1878.KlingelnbergCycloPalloidHypoidGearMesh') -> '_3277.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3277.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_6140.KlingelnbergCycloPalloidHypoidGearMeshLoadCase') -> '_3277.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3277.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1879.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> '_3280.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3280.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6143.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase') -> '_3280.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3280.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1882.SpiralBevelGearMesh') -> '_3307.SpiralBevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpiralBevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3307.SpiralBevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6176.SpiralBevelGearMeshLoadCase') -> '_3307.SpiralBevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpiralBevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3307.SpiralBevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1886.StraightBevelGearMesh') -> '_3316.StraightBevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3316.StraightBevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6186.StraightBevelGearMeshLoadCase') -> '_3316.StraightBevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3316.StraightBevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_worm_gear_mesh(self, design_entity: '_1888.WormGearMesh') -> '_3332.WormGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.WormGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3332.WormGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_worm_gear_mesh_load_case(self, design_entity_analysis: '_6207.WormGearMeshLoadCase') -> '_3332.WormGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.WormGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3332.WormGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1890.ZerolBevelGearMesh') -> '_3335.ZerolBevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ZerolBevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3335.ZerolBevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6210.ZerolBevelGearMeshLoadCase') -> '_3335.ZerolBevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ZerolBevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3335.ZerolBevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_gear_mesh(self, design_entity: '_1872.GearMesh') -> '_3265.GearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.GearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3265.GearMeshPowerFlow)(method_result) if method_result else None

    def results_for_gear_mesh_load_case(self, design_entity_analysis: '_6117.GearMeshLoadCase') -> '_3265.GearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.GearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3265.GearMeshPowerFlow)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_connection(self, design_entity: '_1898.PartToPartShearCouplingConnection') -> '_3288.PartToPartShearCouplingConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PartToPartShearCouplingConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3288.PartToPartShearCouplingConnectionPowerFlow)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_connection_load_case(self, design_entity_analysis: '_6153.PartToPartShearCouplingConnectionLoadCase') -> '_3288.PartToPartShearCouplingConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PartToPartShearCouplingConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3288.PartToPartShearCouplingConnectionPowerFlow)(method_result) if method_result else None

    def results_for_clutch_connection(self, design_entity: '_1892.ClutchConnection') -> '_3232.ClutchConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ClutchConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3232.ClutchConnectionPowerFlow)(method_result) if method_result else None

    def results_for_clutch_connection_load_case(self, design_entity_analysis: '_6064.ClutchConnectionLoadCase') -> '_3232.ClutchConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ClutchConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3232.ClutchConnectionPowerFlow)(method_result) if method_result else None

    def results_for_concept_coupling_connection(self, design_entity: '_1894.ConceptCouplingConnection') -> '_3237.ConceptCouplingConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptCouplingConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3237.ConceptCouplingConnectionPowerFlow)(method_result) if method_result else None

    def results_for_concept_coupling_connection_load_case(self, design_entity_analysis: '_6069.ConceptCouplingConnectionLoadCase') -> '_3237.ConceptCouplingConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptCouplingConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3237.ConceptCouplingConnectionPowerFlow)(method_result) if method_result else None

    def results_for_coupling_connection(self, design_entity: '_1896.CouplingConnection') -> '_3248.CouplingConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CouplingConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3248.CouplingConnectionPowerFlow)(method_result) if method_result else None

    def results_for_coupling_connection_load_case(self, design_entity_analysis: '_6082.CouplingConnectionLoadCase') -> '_3248.CouplingConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CouplingConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3248.CouplingConnectionPowerFlow)(method_result) if method_result else None

    def results_for_spring_damper_connection(self, design_entity: '_1900.SpringDamperConnection') -> '_3310.SpringDamperConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpringDamperConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3310.SpringDamperConnectionPowerFlow)(method_result) if method_result else None

    def results_for_spring_damper_connection_load_case(self, design_entity_analysis: '_6178.SpringDamperConnectionLoadCase') -> '_3310.SpringDamperConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpringDamperConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3310.SpringDamperConnectionPowerFlow)(method_result) if method_result else None

    def results_for_torque_converter_connection(self, design_entity: '_1902.TorqueConverterConnection') -> '_3326.TorqueConverterConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.TorqueConverterConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3326.TorqueConverterConnectionPowerFlow)(method_result) if method_result else None

    def results_for_torque_converter_connection_load_case(self, design_entity_analysis: '_6196.TorqueConverterConnectionLoadCase') -> '_3326.TorqueConverterConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.TorqueConverterConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3326.TorqueConverterConnectionPowerFlow)(method_result) if method_result else None

    def results_for_abstract_assembly(self, design_entity: '_1978.AbstractAssembly') -> '_3213.AbstractAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AbstractAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3213.AbstractAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_abstract_assembly_load_case(self, design_entity_analysis: '_6043.AbstractAssemblyLoadCase') -> '_3213.AbstractAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AbstractAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3213.AbstractAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing(self, design_entity: '_1979.AbstractShaftOrHousing') -> '_3214.AbstractShaftOrHousingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AbstractShaftOrHousingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3214.AbstractShaftOrHousingPowerFlow)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing_load_case(self, design_entity_analysis: '_6044.AbstractShaftOrHousingLoadCase') -> '_3214.AbstractShaftOrHousingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractShaftOrHousingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AbstractShaftOrHousingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3214.AbstractShaftOrHousingPowerFlow)(method_result) if method_result else None

    def results_for_bearing(self, design_entity: '_1982.Bearing') -> '_3219.BearingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BearingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3219.BearingPowerFlow)(method_result) if method_result else None

    def results_for_bearing_load_case(self, design_entity_analysis: '_6051.BearingLoadCase') -> '_3219.BearingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BearingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3219.BearingPowerFlow)(method_result) if method_result else None

    def results_for_bolt(self, design_entity: '_1984.Bolt') -> '_3231.BoltPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BoltPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3231.BoltPowerFlow)(method_result) if method_result else None

    def results_for_bolt_load_case(self, design_entity_analysis: '_6063.BoltLoadCase') -> '_3231.BoltPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BoltPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3231.BoltPowerFlow)(method_result) if method_result else None

    def results_for_bolted_joint(self, design_entity: '_1985.BoltedJoint') -> '_3230.BoltedJointPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BoltedJointPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3230.BoltedJointPowerFlow)(method_result) if method_result else None

    def results_for_bolted_joint_load_case(self, design_entity_analysis: '_6062.BoltedJointLoadCase') -> '_3230.BoltedJointPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltedJointLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BoltedJointPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3230.BoltedJointPowerFlow)(method_result) if method_result else None

    def results_for_component(self, design_entity: '_1986.Component') -> '_3236.ComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3236.ComponentPowerFlow)(method_result) if method_result else None

    def results_for_component_load_case(self, design_entity_analysis: '_6068.ComponentLoadCase') -> '_3236.ComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3236.ComponentPowerFlow)(method_result) if method_result else None

    def results_for_connector(self, design_entity: '_1989.Connector') -> '_3247.ConnectorPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConnectorPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3247.ConnectorPowerFlow)(method_result) if method_result else None

    def results_for_connector_load_case(self, design_entity_analysis: '_6081.ConnectorLoadCase') -> '_3247.ConnectorPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectorLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConnectorPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3247.ConnectorPowerFlow)(method_result) if method_result else None

    def results_for_datum(self, design_entity: '_1990.Datum') -> '_3259.DatumPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.DatumPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3259.DatumPowerFlow)(method_result) if method_result else None

    def results_for_datum_load_case(self, design_entity_analysis: '_6096.DatumLoadCase') -> '_3259.DatumPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.DatumLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.DatumPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3259.DatumPowerFlow)(method_result) if method_result else None

    def results_for_external_cad_model(self, design_entity: '_1993.ExternalCADModel') -> '_3260.ExternalCADModelPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ExternalCADModelPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3260.ExternalCADModelPowerFlow)(method_result) if method_result else None

    def results_for_external_cad_model_load_case(self, design_entity_analysis: '_6109.ExternalCADModelLoadCase') -> '_3260.ExternalCADModelPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ExternalCADModelPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3260.ExternalCADModelPowerFlow)(method_result) if method_result else None

    def results_for_flexible_pin_assembly(self, design_entity: '_1994.FlexiblePinAssembly') -> '_3264.FlexiblePinAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.FlexiblePinAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3264.FlexiblePinAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_flexible_pin_assembly_load_case(self, design_entity_analysis: '_6113.FlexiblePinAssemblyLoadCase') -> '_3264.FlexiblePinAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FlexiblePinAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.FlexiblePinAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3264.FlexiblePinAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_assembly(self, design_entity: '_1977.Assembly') -> '_3218.AssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3218.AssemblyPowerFlow)(method_result) if method_result else None

    def results_for_assembly_load_case(self, design_entity_analysis: '_6050.AssemblyLoadCase') -> '_3218.AssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3218.AssemblyPowerFlow)(method_result) if method_result else None

    def results_for_guide_dxf_model(self, design_entity: '_1995.GuideDxfModel') -> '_3268.GuideDxfModelPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.GuideDxfModelPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3268.GuideDxfModelPowerFlow)(method_result) if method_result else None

    def results_for_guide_dxf_model_load_case(self, design_entity_analysis: '_6121.GuideDxfModelLoadCase') -> '_3268.GuideDxfModelPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GuideDxfModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.GuideDxfModelPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3268.GuideDxfModelPowerFlow)(method_result) if method_result else None

    def results_for_imported_fe_component(self, design_entity: '_1998.ImportedFEComponent') -> '_3272.ImportedFEComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ImportedFEComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3272.ImportedFEComponentPowerFlow)(method_result) if method_result else None

    def results_for_imported_fe_component_load_case(self, design_entity_analysis: '_6133.ImportedFEComponentLoadCase') -> '_3272.ImportedFEComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ImportedFEComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ImportedFEComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3272.ImportedFEComponentPowerFlow)(method_result) if method_result else None

    def results_for_mass_disc(self, design_entity: '_2001.MassDisc') -> '_3283.MassDiscPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.MassDiscPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3283.MassDiscPowerFlow)(method_result) if method_result else None

    def results_for_mass_disc_load_case(self, design_entity_analysis: '_6145.MassDiscLoadCase') -> '_3283.MassDiscPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MassDiscLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.MassDiscPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3283.MassDiscPowerFlow)(method_result) if method_result else None

    def results_for_measurement_component(self, design_entity: '_2002.MeasurementComponent') -> '_3284.MeasurementComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.MeasurementComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3284.MeasurementComponentPowerFlow)(method_result) if method_result else None

    def results_for_measurement_component_load_case(self, design_entity_analysis: '_6146.MeasurementComponentLoadCase') -> '_3284.MeasurementComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MeasurementComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.MeasurementComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3284.MeasurementComponentPowerFlow)(method_result) if method_result else None

    def results_for_mountable_component(self, design_entity: '_2003.MountableComponent') -> '_3285.MountableComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.MountableComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3285.MountableComponentPowerFlow)(method_result) if method_result else None

    def results_for_mountable_component_load_case(self, design_entity_analysis: '_6148.MountableComponentLoadCase') -> '_3285.MountableComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MountableComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.MountableComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3285.MountableComponentPowerFlow)(method_result) if method_result else None

    def results_for_oil_seal(self, design_entity: '_2005.OilSeal') -> '_3286.OilSealPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.OilSealPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3286.OilSealPowerFlow)(method_result) if method_result else None

    def results_for_oil_seal_load_case(self, design_entity_analysis: '_6150.OilSealLoadCase') -> '_3286.OilSealPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.OilSealPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3286.OilSealPowerFlow)(method_result) if method_result else None

    def results_for_part(self, design_entity: '_2006.Part') -> '_3287.PartPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PartPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3287.PartPowerFlow)(method_result) if method_result else None

    def results_for_part_load_case(self, design_entity_analysis: '_6152.PartLoadCase') -> '_3287.PartPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PartPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3287.PartPowerFlow)(method_result) if method_result else None

    def results_for_planet_carrier(self, design_entity: '_2007.PlanetCarrier') -> '_3293.PlanetCarrierPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PlanetCarrierPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3293.PlanetCarrierPowerFlow)(method_result) if method_result else None

    def results_for_planet_carrier_load_case(self, design_entity_analysis: '_6159.PlanetCarrierLoadCase') -> '_3293.PlanetCarrierPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PlanetCarrierPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3293.PlanetCarrierPowerFlow)(method_result) if method_result else None

    def results_for_point_load(self, design_entity: '_2009.PointLoad') -> '_3294.PointLoadPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PointLoadPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3294.PointLoadPowerFlow)(method_result) if method_result else None

    def results_for_point_load_load_case(self, design_entity_analysis: '_6162.PointLoadLoadCase') -> '_3294.PointLoadPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PointLoadPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3294.PointLoadPowerFlow)(method_result) if method_result else None

    def results_for_power_load(self, design_entity: '_2010.PowerLoad') -> '_3297.PowerLoadPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PowerLoadPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3297.PowerLoadPowerFlow)(method_result) if method_result else None

    def results_for_power_load_load_case(self, design_entity_analysis: '_6163.PowerLoadLoadCase') -> '_3297.PowerLoadPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PowerLoadPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3297.PowerLoadPowerFlow)(method_result) if method_result else None

    def results_for_root_assembly(self, design_entity: '_2012.RootAssembly') -> '_3302.RootAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.RootAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3302.RootAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_root_assembly_load_case(self, design_entity_analysis: '_6169.RootAssemblyLoadCase') -> '_3302.RootAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RootAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.RootAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3302.RootAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_specialised_assembly(self, design_entity: '_2014.SpecialisedAssembly') -> '_3306.SpecialisedAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpecialisedAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3306.SpecialisedAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_specialised_assembly_load_case(self, design_entity_analysis: '_6173.SpecialisedAssemblyLoadCase') -> '_3306.SpecialisedAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpecialisedAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpecialisedAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3306.SpecialisedAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_unbalanced_mass(self, design_entity: '_2015.UnbalancedMass') -> '_3330.UnbalancedMassPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.UnbalancedMassPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3330.UnbalancedMassPowerFlow)(method_result) if method_result else None

    def results_for_unbalanced_mass_load_case(self, design_entity_analysis: '_6204.UnbalancedMassLoadCase') -> '_3330.UnbalancedMassPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.UnbalancedMassLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.UnbalancedMassPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3330.UnbalancedMassPowerFlow)(method_result) if method_result else None

    def results_for_virtual_component(self, design_entity: '_2016.VirtualComponent') -> '_3331.VirtualComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.VirtualComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3331.VirtualComponentPowerFlow)(method_result) if method_result else None

    def results_for_virtual_component_load_case(self, design_entity_analysis: '_6205.VirtualComponentLoadCase') -> '_3331.VirtualComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.VirtualComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.VirtualComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3331.VirtualComponentPowerFlow)(method_result) if method_result else None

    def results_for_shaft(self, design_entity: '_2019.Shaft') -> '_3304.ShaftPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ShaftPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3304.ShaftPowerFlow)(method_result) if method_result else None

    def results_for_shaft_load_case(self, design_entity_analysis: '_6171.ShaftLoadCase') -> '_3304.ShaftPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ShaftPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3304.ShaftPowerFlow)(method_result) if method_result else None

    def results_for_concept_gear(self, design_entity: '_2057.ConceptGear') -> '_3241.ConceptGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3241.ConceptGearPowerFlow)(method_result) if method_result else None

    def results_for_concept_gear_load_case(self, design_entity_analysis: '_6072.ConceptGearLoadCase') -> '_3241.ConceptGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3241.ConceptGearPowerFlow)(method_result) if method_result else None

    def results_for_concept_gear_set(self, design_entity: '_2058.ConceptGearSet') -> '_3242.ConceptGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3242.ConceptGearSetPowerFlow)(method_result) if method_result else None

    def results_for_concept_gear_set_load_case(self, design_entity_analysis: '_6074.ConceptGearSetLoadCase') -> '_3242.ConceptGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3242.ConceptGearSetPowerFlow)(method_result) if method_result else None

    def results_for_face_gear(self, design_entity: '_2064.FaceGear') -> '_3262.FaceGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.FaceGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3262.FaceGearPowerFlow)(method_result) if method_result else None

    def results_for_face_gear_load_case(self, design_entity_analysis: '_6110.FaceGearLoadCase') -> '_3262.FaceGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.FaceGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3262.FaceGearPowerFlow)(method_result) if method_result else None

    def results_for_face_gear_set(self, design_entity: '_2065.FaceGearSet') -> '_3263.FaceGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.FaceGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3263.FaceGearSetPowerFlow)(method_result) if method_result else None

    def results_for_face_gear_set_load_case(self, design_entity_analysis: '_6112.FaceGearSetLoadCase') -> '_3263.FaceGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.FaceGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3263.FaceGearSetPowerFlow)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear(self, design_entity: '_2049.AGMAGleasonConicalGear') -> '_3216.AGMAGleasonConicalGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AGMAGleasonConicalGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3216.AGMAGleasonConicalGearPowerFlow)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_load_case(self, design_entity_analysis: '_6046.AGMAGleasonConicalGearLoadCase') -> '_3216.AGMAGleasonConicalGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AGMAGleasonConicalGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3216.AGMAGleasonConicalGearPowerFlow)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_2050.AGMAGleasonConicalGearSet') -> '_3217.AGMAGleasonConicalGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AGMAGleasonConicalGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3217.AGMAGleasonConicalGearSetPowerFlow)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set_load_case(self, design_entity_analysis: '_6048.AGMAGleasonConicalGearSetLoadCase') -> '_3217.AGMAGleasonConicalGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AGMAGleasonConicalGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3217.AGMAGleasonConicalGearSetPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_gear(self, design_entity: '_2051.BevelDifferentialGear') -> '_3223.BevelDifferentialGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3223.BevelDifferentialGearPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_gear_load_case(self, design_entity_analysis: '_6054.BevelDifferentialGearLoadCase') -> '_3223.BevelDifferentialGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3223.BevelDifferentialGearPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set(self, design_entity: '_2052.BevelDifferentialGearSet') -> '_3224.BevelDifferentialGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3224.BevelDifferentialGearSetPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set_load_case(self, design_entity_analysis: '_6056.BevelDifferentialGearSetLoadCase') -> '_3224.BevelDifferentialGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3224.BevelDifferentialGearSetPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2053.BevelDifferentialPlanetGear') -> '_3225.BevelDifferentialPlanetGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialPlanetGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3225.BevelDifferentialPlanetGearPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear_load_case(self, design_entity_analysis: '_6057.BevelDifferentialPlanetGearLoadCase') -> '_3225.BevelDifferentialPlanetGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialPlanetGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3225.BevelDifferentialPlanetGearPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2054.BevelDifferentialSunGear') -> '_3226.BevelDifferentialSunGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialSunGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3226.BevelDifferentialSunGearPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear_load_case(self, design_entity_analysis: '_6058.BevelDifferentialSunGearLoadCase') -> '_3226.BevelDifferentialSunGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialSunGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3226.BevelDifferentialSunGearPowerFlow)(method_result) if method_result else None

    def results_for_bevel_gear(self, design_entity: '_2055.BevelGear') -> '_3228.BevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3228.BevelGearPowerFlow)(method_result) if method_result else None

    def results_for_bevel_gear_load_case(self, design_entity_analysis: '_6059.BevelGearLoadCase') -> '_3228.BevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3228.BevelGearPowerFlow)(method_result) if method_result else None

    def results_for_bevel_gear_set(self, design_entity: '_2056.BevelGearSet') -> '_3229.BevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3229.BevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_bevel_gear_set_load_case(self, design_entity_analysis: '_6061.BevelGearSetLoadCase') -> '_3229.BevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3229.BevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_conical_gear(self, design_entity: '_2059.ConicalGear') -> '_3244.ConicalGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConicalGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3244.ConicalGearPowerFlow)(method_result) if method_result else None

    def results_for_conical_gear_load_case(self, design_entity_analysis: '_6075.ConicalGearLoadCase') -> '_3244.ConicalGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConicalGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3244.ConicalGearPowerFlow)(method_result) if method_result else None

    def results_for_conical_gear_set(self, design_entity: '_2060.ConicalGearSet') -> '_3245.ConicalGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConicalGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3245.ConicalGearSetPowerFlow)(method_result) if method_result else None

    def results_for_conical_gear_set_load_case(self, design_entity_analysis: '_6079.ConicalGearSetLoadCase') -> '_3245.ConicalGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConicalGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3245.ConicalGearSetPowerFlow)(method_result) if method_result else None

    def results_for_cylindrical_gear(self, design_entity: '_2061.CylindricalGear') -> '_3256.CylindricalGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CylindricalGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3256.CylindricalGearPowerFlow)(method_result) if method_result else None

    def results_for_cylindrical_gear_load_case(self, design_entity_analysis: '_6088.CylindricalGearLoadCase') -> '_3256.CylindricalGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CylindricalGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3256.CylindricalGearPowerFlow)(method_result) if method_result else None

    def results_for_cylindrical_gear_set(self, design_entity: '_2062.CylindricalGearSet') -> '_3257.CylindricalGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CylindricalGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3257.CylindricalGearSetPowerFlow)(method_result) if method_result else None

    def results_for_cylindrical_gear_set_load_case(self, design_entity_analysis: '_6092.CylindricalGearSetLoadCase') -> '_3257.CylindricalGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CylindricalGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3257.CylindricalGearSetPowerFlow)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear(self, design_entity: '_2063.CylindricalPlanetGear') -> '_3258.CylindricalPlanetGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CylindricalPlanetGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3258.CylindricalPlanetGearPowerFlow)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear_load_case(self, design_entity_analysis: '_6093.CylindricalPlanetGearLoadCase') -> '_3258.CylindricalPlanetGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CylindricalPlanetGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3258.CylindricalPlanetGearPowerFlow)(method_result) if method_result else None

    def results_for_gear(self, design_entity: '_2066.Gear') -> '_3266.GearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.GearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3266.GearPowerFlow)(method_result) if method_result else None

    def results_for_gear_load_case(self, design_entity_analysis: '_6115.GearLoadCase') -> '_3266.GearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.GearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3266.GearPowerFlow)(method_result) if method_result else None

    def results_for_gear_set(self, design_entity: '_2068.GearSet') -> '_3267.GearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.GearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3267.GearSetPowerFlow)(method_result) if method_result else None

    def results_for_gear_set_load_case(self, design_entity_analysis: '_6120.GearSetLoadCase') -> '_3267.GearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.GearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3267.GearSetPowerFlow)(method_result) if method_result else None

    def results_for_hypoid_gear(self, design_entity: '_2070.HypoidGear') -> '_3270.HypoidGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.HypoidGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3270.HypoidGearPowerFlow)(method_result) if method_result else None

    def results_for_hypoid_gear_load_case(self, design_entity_analysis: '_6130.HypoidGearLoadCase') -> '_3270.HypoidGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.HypoidGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3270.HypoidGearPowerFlow)(method_result) if method_result else None

    def results_for_hypoid_gear_set(self, design_entity: '_2071.HypoidGearSet') -> '_3271.HypoidGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.HypoidGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3271.HypoidGearSetPowerFlow)(method_result) if method_result else None

    def results_for_hypoid_gear_set_load_case(self, design_entity_analysis: '_6132.HypoidGearSetLoadCase') -> '_3271.HypoidGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.HypoidGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3271.HypoidGearSetPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2072.KlingelnbergCycloPalloidConicalGear') -> '_3275.KlingelnbergCycloPalloidConicalGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidConicalGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3275.KlingelnbergCycloPalloidConicalGearPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_load_case(self, design_entity_analysis: '_6136.KlingelnbergCycloPalloidConicalGearLoadCase') -> '_3275.KlingelnbergCycloPalloidConicalGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidConicalGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3275.KlingelnbergCycloPalloidConicalGearPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2073.KlingelnbergCycloPalloidConicalGearSet') -> '_3276.KlingelnbergCycloPalloidConicalGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidConicalGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3276.KlingelnbergCycloPalloidConicalGearSetPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set_load_case(self, design_entity_analysis: '_6138.KlingelnbergCycloPalloidConicalGearSetLoadCase') -> '_3276.KlingelnbergCycloPalloidConicalGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidConicalGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3276.KlingelnbergCycloPalloidConicalGearSetPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2074.KlingelnbergCycloPalloidHypoidGear') -> '_3278.KlingelnbergCycloPalloidHypoidGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidHypoidGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3278.KlingelnbergCycloPalloidHypoidGearPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_load_case(self, design_entity_analysis: '_6139.KlingelnbergCycloPalloidHypoidGearLoadCase') -> '_3278.KlingelnbergCycloPalloidHypoidGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidHypoidGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3278.KlingelnbergCycloPalloidHypoidGearPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2075.KlingelnbergCycloPalloidHypoidGearSet') -> '_3279.KlingelnbergCycloPalloidHypoidGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidHypoidGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3279.KlingelnbergCycloPalloidHypoidGearSetPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(self, design_entity_analysis: '_6141.KlingelnbergCycloPalloidHypoidGearSetLoadCase') -> '_3279.KlingelnbergCycloPalloidHypoidGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidHypoidGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3279.KlingelnbergCycloPalloidHypoidGearSetPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2076.KlingelnbergCycloPalloidSpiralBevelGear') -> '_3281.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3281.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(self, design_entity_analysis: '_6142.KlingelnbergCycloPalloidSpiralBevelGearLoadCase') -> '_3281.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3281.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2077.KlingelnbergCycloPalloidSpiralBevelGearSet') -> '_3282.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3282.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_6144.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase') -> '_3282.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3282.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_planetary_gear_set(self, design_entity: '_2078.PlanetaryGearSet') -> '_3292.PlanetaryGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PlanetaryGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3292.PlanetaryGearSetPowerFlow)(method_result) if method_result else None

    def results_for_planetary_gear_set_load_case(self, design_entity_analysis: '_6157.PlanetaryGearSetLoadCase') -> '_3292.PlanetaryGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PlanetaryGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3292.PlanetaryGearSetPowerFlow)(method_result) if method_result else None

    def results_for_spiral_bevel_gear(self, design_entity: '_2079.SpiralBevelGear') -> '_3308.SpiralBevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpiralBevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3308.SpiralBevelGearPowerFlow)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_load_case(self, design_entity_analysis: '_6175.SpiralBevelGearLoadCase') -> '_3308.SpiralBevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpiralBevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3308.SpiralBevelGearPowerFlow)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set(self, design_entity: '_2080.SpiralBevelGearSet') -> '_3309.SpiralBevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpiralBevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3309.SpiralBevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_6177.SpiralBevelGearSetLoadCase') -> '_3309.SpiralBevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpiralBevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3309.SpiralBevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2081.StraightBevelDiffGear') -> '_3314.StraightBevelDiffGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelDiffGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3314.StraightBevelDiffGearPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_load_case(self, design_entity_analysis: '_6182.StraightBevelDiffGearLoadCase') -> '_3314.StraightBevelDiffGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelDiffGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3314.StraightBevelDiffGearPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_2082.StraightBevelDiffGearSet') -> '_3315.StraightBevelDiffGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelDiffGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3315.StraightBevelDiffGearSetPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set_load_case(self, design_entity_analysis: '_6184.StraightBevelDiffGearSetLoadCase') -> '_3315.StraightBevelDiffGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelDiffGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3315.StraightBevelDiffGearSetPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_gear(self, design_entity: '_2083.StraightBevelGear') -> '_3317.StraightBevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3317.StraightBevelGearPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_gear_load_case(self, design_entity_analysis: '_6185.StraightBevelGearLoadCase') -> '_3317.StraightBevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3317.StraightBevelGearPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set(self, design_entity: '_2084.StraightBevelGearSet') -> '_3318.StraightBevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3318.StraightBevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set_load_case(self, design_entity_analysis: '_6187.StraightBevelGearSetLoadCase') -> '_3318.StraightBevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3318.StraightBevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2085.StraightBevelPlanetGear') -> '_3319.StraightBevelPlanetGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelPlanetGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3319.StraightBevelPlanetGearPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear_load_case(self, design_entity_analysis: '_6188.StraightBevelPlanetGearLoadCase') -> '_3319.StraightBevelPlanetGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelPlanetGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3319.StraightBevelPlanetGearPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2086.StraightBevelSunGear') -> '_3320.StraightBevelSunGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelSunGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3320.StraightBevelSunGearPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear_load_case(self, design_entity_analysis: '_6189.StraightBevelSunGearLoadCase') -> '_3320.StraightBevelSunGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelSunGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3320.StraightBevelSunGearPowerFlow)(method_result) if method_result else None

    def results_for_worm_gear(self, design_entity: '_2087.WormGear') -> '_3333.WormGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.WormGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3333.WormGearPowerFlow)(method_result) if method_result else None

    def results_for_worm_gear_load_case(self, design_entity_analysis: '_6206.WormGearLoadCase') -> '_3333.WormGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.WormGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3333.WormGearPowerFlow)(method_result) if method_result else None

    def results_for_worm_gear_set(self, design_entity: '_2088.WormGearSet') -> '_3334.WormGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.WormGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3334.WormGearSetPowerFlow)(method_result) if method_result else None
