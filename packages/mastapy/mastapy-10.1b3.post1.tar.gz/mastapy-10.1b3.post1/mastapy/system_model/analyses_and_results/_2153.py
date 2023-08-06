'''_2153.py

CompoundParametricStudyToolAnalysis
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
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
    _3714, _3715, _3717, _3671,
    _3673, _3605, _3616, _3618,
    _3621, _3623, _3632, _3634,
    _3636, _3637, _3679, _3685,
    _3681, _3680, _3691, _3693,
    _3702, _3703, _3704, _3705,
    _3706, _3708, _3709, _3635,
    _3604, _3619, _3630, _3656,
    _3674, _3682, _3686, _3607,
    _3625, _3645, _3695, _3612,
    _3628, _3600, _3639, _3653,
    _3658, _3661, _3664, _3689,
    _3698, _3713, _3716, _3649,
    _3672, _3617, _3622, _3633,
    _3692, _3707, _3597, _3598,
    _3603, _3614, _3615, _3620,
    _3631, _3642, _3643, _3647,
    _3602, _3651, _3655, _3666,
    _3667, _3668, _3669, _3670,
    _3676, _3677, _3678, _3683,
    _3687, _3710, _3711, _3684,
    _3624, _3626, _3644, _3646,
    _3599, _3601, _3606, _3608,
    _3609, _3610, _3611, _3613,
    _3627, _3629, _3638, _3640,
    _3641, _3648, _3650, _3652,
    _3654, _3657, _3659, _3660,
    _3662, _3663, _3665, _3675,
    _3688, _3690, _3694, _3696,
    _3697, _3699, _3700, _3701,
    _3712
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

_COMPOUND_PARAMETRIC_STUDY_TOOL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundParametricStudyToolAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundParametricStudyToolAnalysis',)


class CompoundParametricStudyToolAnalysis(_2150.SingleAnalysis):
    '''CompoundParametricStudyToolAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_PARAMETRIC_STUDY_TOOL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundParametricStudyToolAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    def results_for_worm_gear_set_load_case(self, design_entity_analysis: '_6208.WormGearSetLoadCase') -> '_3714.WormGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.WormGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3714.WormGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_zerol_bevel_gear(self, design_entity: '_2089.ZerolBevelGear') -> '_3715.ZerolBevelGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ZerolBevelGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3715.ZerolBevelGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_load_case(self, design_entity_analysis: '_6209.ZerolBevelGearLoadCase') -> '_3715.ZerolBevelGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ZerolBevelGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3715.ZerolBevelGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set(self, design_entity: '_2090.ZerolBevelGearSet') -> '_3717.ZerolBevelGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ZerolBevelGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3717.ZerolBevelGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set_load_case(self, design_entity_analysis: '_6211.ZerolBevelGearSetLoadCase') -> '_3717.ZerolBevelGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ZerolBevelGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3717.ZerolBevelGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling(self, design_entity: '_2119.PartToPartShearCoupling') -> '_3671.PartToPartShearCouplingCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PartToPartShearCouplingCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3671.PartToPartShearCouplingCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_load_case(self, design_entity_analysis: '_6155.PartToPartShearCouplingLoadCase') -> '_3671.PartToPartShearCouplingCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PartToPartShearCouplingCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3671.PartToPartShearCouplingCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_half(self, design_entity: '_2120.PartToPartShearCouplingHalf') -> '_3673.PartToPartShearCouplingHalfCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PartToPartShearCouplingHalfCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3673.PartToPartShearCouplingHalfCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_half_load_case(self, design_entity_analysis: '_6154.PartToPartShearCouplingHalfLoadCase') -> '_3673.PartToPartShearCouplingHalfCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PartToPartShearCouplingHalfCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3673.PartToPartShearCouplingHalfCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_belt_drive(self, design_entity: '_2108.BeltDrive') -> '_3605.BeltDriveCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BeltDriveCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3605.BeltDriveCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_belt_drive_load_case(self, design_entity_analysis: '_6053.BeltDriveLoadCase') -> '_3605.BeltDriveCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltDriveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BeltDriveCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3605.BeltDriveCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_clutch(self, design_entity: '_2110.Clutch') -> '_3616.ClutchCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ClutchCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3616.ClutchCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_clutch_load_case(self, design_entity_analysis: '_6066.ClutchLoadCase') -> '_3616.ClutchCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ClutchCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3616.ClutchCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_clutch_half(self, design_entity: '_2111.ClutchHalf') -> '_3618.ClutchHalfCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ClutchHalfCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3618.ClutchHalfCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_clutch_half_load_case(self, design_entity_analysis: '_6065.ClutchHalfLoadCase') -> '_3618.ClutchHalfCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ClutchHalfCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3618.ClutchHalfCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_coupling(self, design_entity: '_2113.ConceptCoupling') -> '_3621.ConceptCouplingCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConceptCouplingCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3621.ConceptCouplingCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_coupling_load_case(self, design_entity_analysis: '_6071.ConceptCouplingLoadCase') -> '_3621.ConceptCouplingCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConceptCouplingCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3621.ConceptCouplingCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_coupling_half(self, design_entity: '_2114.ConceptCouplingHalf') -> '_3623.ConceptCouplingHalfCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConceptCouplingHalfCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3623.ConceptCouplingHalfCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_coupling_half_load_case(self, design_entity_analysis: '_6070.ConceptCouplingHalfLoadCase') -> '_3623.ConceptCouplingHalfCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConceptCouplingHalfCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3623.ConceptCouplingHalfCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_coupling(self, design_entity: '_2115.Coupling') -> '_3632.CouplingCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CouplingCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3632.CouplingCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_coupling_load_case(self, design_entity_analysis: '_6084.CouplingLoadCase') -> '_3632.CouplingCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CouplingCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3632.CouplingCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_coupling_half(self, design_entity: '_2116.CouplingHalf') -> '_3634.CouplingHalfCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CouplingHalfCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3634.CouplingHalfCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_coupling_half_load_case(self, design_entity_analysis: '_6083.CouplingHalfLoadCase') -> '_3634.CouplingHalfCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CouplingHalfCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3634.CouplingHalfCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_cvt(self, design_entity: '_2117.CVT') -> '_3636.CVTCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CVTCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3636.CVTCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_cvt_load_case(self, design_entity_analysis: '_6086.CVTLoadCase') -> '_3636.CVTCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CVTCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3636.CVTCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_cvt_pulley(self, design_entity: '_2118.CVTPulley') -> '_3637.CVTPulleyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CVTPulleyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3637.CVTPulleyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_cvt_pulley_load_case(self, design_entity_analysis: '_6087.CVTPulleyLoadCase') -> '_3637.CVTPulleyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTPulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CVTPulleyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3637.CVTPulleyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_pulley(self, design_entity: '_2121.Pulley') -> '_3679.PulleyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PulleyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3679.PulleyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_pulley_load_case(self, design_entity_analysis: '_6164.PulleyLoadCase') -> '_3679.PulleyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PulleyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3679.PulleyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_shaft_hub_connection(self, design_entity: '_2129.ShaftHubConnection') -> '_3685.ShaftHubConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ShaftHubConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3685.ShaftHubConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_shaft_hub_connection_load_case(self, design_entity_analysis: '_6170.ShaftHubConnectionLoadCase') -> '_3685.ShaftHubConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ShaftHubConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3685.ShaftHubConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_rolling_ring(self, design_entity: '_2127.RollingRing') -> '_3681.RollingRingCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.RollingRingCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3681.RollingRingCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_rolling_ring_load_case(self, design_entity_analysis: '_6168.RollingRingLoadCase') -> '_3681.RollingRingCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.RollingRingCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3681.RollingRingCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_rolling_ring_assembly(self, design_entity: '_2128.RollingRingAssembly') -> '_3680.RollingRingAssemblyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.RollingRingAssemblyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3680.RollingRingAssemblyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_rolling_ring_assembly_load_case(self, design_entity_analysis: '_6166.RollingRingAssemblyLoadCase') -> '_3680.RollingRingAssemblyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.RollingRingAssemblyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3680.RollingRingAssemblyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_spring_damper(self, design_entity: '_2130.SpringDamper') -> '_3691.SpringDamperCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SpringDamperCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3691.SpringDamperCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_spring_damper_load_case(self, design_entity_analysis: '_6180.SpringDamperLoadCase') -> '_3691.SpringDamperCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SpringDamperCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3691.SpringDamperCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_spring_damper_half(self, design_entity: '_2131.SpringDamperHalf') -> '_3693.SpringDamperHalfCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SpringDamperHalfCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3693.SpringDamperHalfCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_spring_damper_half_load_case(self, design_entity_analysis: '_6179.SpringDamperHalfLoadCase') -> '_3693.SpringDamperHalfCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SpringDamperHalfCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3693.SpringDamperHalfCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser(self, design_entity: '_2132.Synchroniser') -> '_3702.SynchroniserCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SynchroniserCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3702.SynchroniserCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser_load_case(self, design_entity_analysis: '_6191.SynchroniserLoadCase') -> '_3702.SynchroniserCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SynchroniserCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3702.SynchroniserCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser_half(self, design_entity: '_2134.SynchroniserHalf') -> '_3703.SynchroniserHalfCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SynchroniserHalfCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3703.SynchroniserHalfCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser_half_load_case(self, design_entity_analysis: '_6190.SynchroniserHalfLoadCase') -> '_3703.SynchroniserHalfCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SynchroniserHalfCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3703.SynchroniserHalfCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser_part(self, design_entity: '_2135.SynchroniserPart') -> '_3704.SynchroniserPartCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SynchroniserPartCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3704.SynchroniserPartCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser_part_load_case(self, design_entity_analysis: '_6192.SynchroniserPartLoadCase') -> '_3704.SynchroniserPartCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserPartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SynchroniserPartCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3704.SynchroniserPartCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser_sleeve(self, design_entity: '_2136.SynchroniserSleeve') -> '_3705.SynchroniserSleeveCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SynchroniserSleeveCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3705.SynchroniserSleeveCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser_sleeve_load_case(self, design_entity_analysis: '_6193.SynchroniserSleeveLoadCase') -> '_3705.SynchroniserSleeveCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserSleeveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SynchroniserSleeveCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3705.SynchroniserSleeveCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter(self, design_entity: '_2137.TorqueConverter') -> '_3706.TorqueConverterCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.TorqueConverterCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3706.TorqueConverterCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter_load_case(self, design_entity_analysis: '_6197.TorqueConverterLoadCase') -> '_3706.TorqueConverterCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.TorqueConverterCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3706.TorqueConverterCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter_pump(self, design_entity: '_2138.TorqueConverterPump') -> '_3708.TorqueConverterPumpCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.TorqueConverterPumpCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3708.TorqueConverterPumpCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter_pump_load_case(self, design_entity_analysis: '_6198.TorqueConverterPumpLoadCase') -> '_3708.TorqueConverterPumpCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterPumpLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.TorqueConverterPumpCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3708.TorqueConverterPumpCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter_turbine(self, design_entity: '_2140.TorqueConverterTurbine') -> '_3709.TorqueConverterTurbineCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.TorqueConverterTurbineCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3709.TorqueConverterTurbineCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter_turbine_load_case(self, design_entity_analysis: '_6199.TorqueConverterTurbineLoadCase') -> '_3709.TorqueConverterTurbineCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterTurbineLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.TorqueConverterTurbineCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3709.TorqueConverterTurbineCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_cvt_belt_connection(self, design_entity: '_1835.CVTBeltConnection') -> '_3635.CVTBeltConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CVTBeltConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3635.CVTBeltConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_cvt_belt_connection_load_case(self, design_entity_analysis: '_6085.CVTBeltConnectionLoadCase') -> '_3635.CVTBeltConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTBeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CVTBeltConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3635.CVTBeltConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_belt_connection(self, design_entity: '_1830.BeltConnection') -> '_3604.BeltConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BeltConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3604.BeltConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_belt_connection_load_case(self, design_entity_analysis: '_6052.BeltConnectionLoadCase') -> '_3604.BeltConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BeltConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3604.BeltConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_coaxial_connection(self, design_entity: '_1831.CoaxialConnection') -> '_3619.CoaxialConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CoaxialConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3619.CoaxialConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_coaxial_connection_load_case(self, design_entity_analysis: '_6067.CoaxialConnectionLoadCase') -> '_3619.CoaxialConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CoaxialConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3619.CoaxialConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_connection(self, design_entity: '_1834.Connection') -> '_3630.ConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3630.ConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_connection_load_case(self, design_entity_analysis: '_6080.ConnectionLoadCase') -> '_3630.ConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3630.ConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection(self, design_entity: '_1843.InterMountableComponentConnection') -> '_3656.InterMountableComponentConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.InterMountableComponentConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3656.InterMountableComponentConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection_load_case(self, design_entity_analysis: '_6135.InterMountableComponentConnectionLoadCase') -> '_3656.InterMountableComponentConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.InterMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.InterMountableComponentConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3656.InterMountableComponentConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_planetary_connection(self, design_entity: '_1846.PlanetaryConnection') -> '_3674.PlanetaryConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PlanetaryConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3674.PlanetaryConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_planetary_connection_load_case(self, design_entity_analysis: '_6156.PlanetaryConnectionLoadCase') -> '_3674.PlanetaryConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PlanetaryConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3674.PlanetaryConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_rolling_ring_connection(self, design_entity: '_1850.RollingRingConnection') -> '_3682.RollingRingConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.RollingRingConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3682.RollingRingConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_rolling_ring_connection_load_case(self, design_entity_analysis: '_6167.RollingRingConnectionLoadCase') -> '_3682.RollingRingConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.RollingRingConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3682.RollingRingConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1854.ShaftToMountableComponentConnection') -> '_3686.ShaftToMountableComponentConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ShaftToMountableComponentConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3686.ShaftToMountableComponentConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection_load_case(self, design_entity_analysis: '_6172.ShaftToMountableComponentConnectionLoadCase') -> '_3686.ShaftToMountableComponentConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftToMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ShaftToMountableComponentConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3686.ShaftToMountableComponentConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1860.BevelDifferentialGearMesh') -> '_3607.BevelDifferentialGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelDifferentialGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3607.BevelDifferentialGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh_load_case(self, design_entity_analysis: '_6055.BevelDifferentialGearMeshLoadCase') -> '_3607.BevelDifferentialGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelDifferentialGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3607.BevelDifferentialGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_gear_mesh(self, design_entity: '_1864.ConceptGearMesh') -> '_3625.ConceptGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConceptGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3625.ConceptGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_gear_mesh_load_case(self, design_entity_analysis: '_6073.ConceptGearMeshLoadCase') -> '_3625.ConceptGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConceptGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3625.ConceptGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_face_gear_mesh(self, design_entity: '_1870.FaceGearMesh') -> '_3645.FaceGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.FaceGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3645.FaceGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_face_gear_mesh_load_case(self, design_entity_analysis: '_6111.FaceGearMeshLoadCase') -> '_3645.FaceGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.FaceGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3645.FaceGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1884.StraightBevelDiffGearMesh') -> '_3695.StraightBevelDiffGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelDiffGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3695.StraightBevelDiffGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh_load_case(self, design_entity_analysis: '_6183.StraightBevelDiffGearMeshLoadCase') -> '_3695.StraightBevelDiffGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelDiffGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3695.StraightBevelDiffGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_gear_mesh(self, design_entity: '_1862.BevelGearMesh') -> '_3612.BevelGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3612.BevelGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6060.BevelGearMeshLoadCase') -> '_3612.BevelGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3612.BevelGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_conical_gear_mesh(self, design_entity: '_1866.ConicalGearMesh') -> '_3628.ConicalGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConicalGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3628.ConicalGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_conical_gear_mesh_load_case(self, design_entity_analysis: '_6077.ConicalGearMeshLoadCase') -> '_3628.ConicalGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConicalGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3628.ConicalGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1858.AGMAGleasonConicalGearMesh') -> '_3600.AGMAGleasonConicalGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.AGMAGleasonConicalGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3600.AGMAGleasonConicalGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh_load_case(self, design_entity_analysis: '_6047.AGMAGleasonConicalGearMeshLoadCase') -> '_3600.AGMAGleasonConicalGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.AGMAGleasonConicalGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3600.AGMAGleasonConicalGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1868.CylindricalGearMesh') -> '_3639.CylindricalGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CylindricalGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3639.CylindricalGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh_load_case(self, design_entity_analysis: '_6090.CylindricalGearMeshLoadCase') -> '_3639.CylindricalGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CylindricalGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3639.CylindricalGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh(self, design_entity: '_1874.HypoidGearMesh') -> '_3653.HypoidGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.HypoidGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3653.HypoidGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_6131.HypoidGearMeshLoadCase') -> '_3653.HypoidGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.HypoidGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3653.HypoidGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1877.KlingelnbergCycloPalloidConicalGearMesh') -> '_3658.KlingelnbergCycloPalloidConicalGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidConicalGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3658.KlingelnbergCycloPalloidConicalGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh_load_case(self, design_entity_analysis: '_6137.KlingelnbergCycloPalloidConicalGearMeshLoadCase') -> '_3658.KlingelnbergCycloPalloidConicalGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidConicalGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3658.KlingelnbergCycloPalloidConicalGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1878.KlingelnbergCycloPalloidHypoidGearMesh') -> '_3661.KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3661.KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_6140.KlingelnbergCycloPalloidHypoidGearMeshLoadCase') -> '_3661.KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3661.KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1879.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> '_3664.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3664.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6143.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase') -> '_3664.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3664.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1882.SpiralBevelGearMesh') -> '_3689.SpiralBevelGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SpiralBevelGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3689.SpiralBevelGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6176.SpiralBevelGearMeshLoadCase') -> '_3689.SpiralBevelGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SpiralBevelGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3689.SpiralBevelGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1886.StraightBevelGearMesh') -> '_3698.StraightBevelGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3698.StraightBevelGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6186.StraightBevelGearMeshLoadCase') -> '_3698.StraightBevelGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3698.StraightBevelGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_worm_gear_mesh(self, design_entity: '_1888.WormGearMesh') -> '_3713.WormGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.WormGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3713.WormGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_worm_gear_mesh_load_case(self, design_entity_analysis: '_6207.WormGearMeshLoadCase') -> '_3713.WormGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.WormGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3713.WormGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1890.ZerolBevelGearMesh') -> '_3716.ZerolBevelGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ZerolBevelGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3716.ZerolBevelGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6210.ZerolBevelGearMeshLoadCase') -> '_3716.ZerolBevelGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ZerolBevelGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3716.ZerolBevelGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_gear_mesh(self, design_entity: '_1872.GearMesh') -> '_3649.GearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.GearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3649.GearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_gear_mesh_load_case(self, design_entity_analysis: '_6117.GearMeshLoadCase') -> '_3649.GearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.GearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3649.GearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_connection(self, design_entity: '_1898.PartToPartShearCouplingConnection') -> '_3672.PartToPartShearCouplingConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PartToPartShearCouplingConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3672.PartToPartShearCouplingConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_connection_load_case(self, design_entity_analysis: '_6153.PartToPartShearCouplingConnectionLoadCase') -> '_3672.PartToPartShearCouplingConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PartToPartShearCouplingConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3672.PartToPartShearCouplingConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_clutch_connection(self, design_entity: '_1892.ClutchConnection') -> '_3617.ClutchConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ClutchConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3617.ClutchConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_clutch_connection_load_case(self, design_entity_analysis: '_6064.ClutchConnectionLoadCase') -> '_3617.ClutchConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ClutchConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3617.ClutchConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_coupling_connection(self, design_entity: '_1894.ConceptCouplingConnection') -> '_3622.ConceptCouplingConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConceptCouplingConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3622.ConceptCouplingConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_coupling_connection_load_case(self, design_entity_analysis: '_6069.ConceptCouplingConnectionLoadCase') -> '_3622.ConceptCouplingConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConceptCouplingConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3622.ConceptCouplingConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_coupling_connection(self, design_entity: '_1896.CouplingConnection') -> '_3633.CouplingConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CouplingConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3633.CouplingConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_coupling_connection_load_case(self, design_entity_analysis: '_6082.CouplingConnectionLoadCase') -> '_3633.CouplingConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CouplingConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3633.CouplingConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_spring_damper_connection(self, design_entity: '_1900.SpringDamperConnection') -> '_3692.SpringDamperConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SpringDamperConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3692.SpringDamperConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_spring_damper_connection_load_case(self, design_entity_analysis: '_6178.SpringDamperConnectionLoadCase') -> '_3692.SpringDamperConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SpringDamperConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3692.SpringDamperConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter_connection(self, design_entity: '_1902.TorqueConverterConnection') -> '_3707.TorqueConverterConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.TorqueConverterConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3707.TorqueConverterConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter_connection_load_case(self, design_entity_analysis: '_6196.TorqueConverterConnectionLoadCase') -> '_3707.TorqueConverterConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.TorqueConverterConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3707.TorqueConverterConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_abstract_assembly(self, design_entity: '_1978.AbstractAssembly') -> '_3597.AbstractAssemblyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.AbstractAssemblyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3597.AbstractAssemblyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_abstract_assembly_load_case(self, design_entity_analysis: '_6043.AbstractAssemblyLoadCase') -> '_3597.AbstractAssemblyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.AbstractAssemblyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3597.AbstractAssemblyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing(self, design_entity: '_1979.AbstractShaftOrHousing') -> '_3598.AbstractShaftOrHousingCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.AbstractShaftOrHousingCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3598.AbstractShaftOrHousingCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing_load_case(self, design_entity_analysis: '_6044.AbstractShaftOrHousingLoadCase') -> '_3598.AbstractShaftOrHousingCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractShaftOrHousingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.AbstractShaftOrHousingCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3598.AbstractShaftOrHousingCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bearing(self, design_entity: '_1982.Bearing') -> '_3603.BearingCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BearingCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3603.BearingCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bearing_load_case(self, design_entity_analysis: '_6051.BearingLoadCase') -> '_3603.BearingCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BearingCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3603.BearingCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bolt(self, design_entity: '_1984.Bolt') -> '_3614.BoltCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BoltCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3614.BoltCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bolt_load_case(self, design_entity_analysis: '_6063.BoltLoadCase') -> '_3614.BoltCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BoltCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3614.BoltCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bolted_joint(self, design_entity: '_1985.BoltedJoint') -> '_3615.BoltedJointCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BoltedJointCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3615.BoltedJointCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bolted_joint_load_case(self, design_entity_analysis: '_6062.BoltedJointLoadCase') -> '_3615.BoltedJointCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltedJointLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BoltedJointCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3615.BoltedJointCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_component(self, design_entity: '_1986.Component') -> '_3620.ComponentCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ComponentCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3620.ComponentCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_component_load_case(self, design_entity_analysis: '_6068.ComponentLoadCase') -> '_3620.ComponentCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ComponentCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3620.ComponentCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_connector(self, design_entity: '_1989.Connector') -> '_3631.ConnectorCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConnectorCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3631.ConnectorCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_connector_load_case(self, design_entity_analysis: '_6081.ConnectorLoadCase') -> '_3631.ConnectorCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectorLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConnectorCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3631.ConnectorCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_datum(self, design_entity: '_1990.Datum') -> '_3642.DatumCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.DatumCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3642.DatumCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_datum_load_case(self, design_entity_analysis: '_6096.DatumLoadCase') -> '_3642.DatumCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.DatumLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.DatumCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3642.DatumCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_external_cad_model(self, design_entity: '_1993.ExternalCADModel') -> '_3643.ExternalCADModelCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ExternalCADModelCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3643.ExternalCADModelCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_external_cad_model_load_case(self, design_entity_analysis: '_6109.ExternalCADModelLoadCase') -> '_3643.ExternalCADModelCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ExternalCADModelCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3643.ExternalCADModelCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_flexible_pin_assembly(self, design_entity: '_1994.FlexiblePinAssembly') -> '_3647.FlexiblePinAssemblyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.FlexiblePinAssemblyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3647.FlexiblePinAssemblyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_flexible_pin_assembly_load_case(self, design_entity_analysis: '_6113.FlexiblePinAssemblyLoadCase') -> '_3647.FlexiblePinAssemblyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FlexiblePinAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.FlexiblePinAssemblyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3647.FlexiblePinAssemblyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_assembly(self, design_entity: '_1977.Assembly') -> '_3602.AssemblyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.AssemblyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3602.AssemblyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_assembly_load_case(self, design_entity_analysis: '_6050.AssemblyLoadCase') -> '_3602.AssemblyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.AssemblyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3602.AssemblyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_guide_dxf_model(self, design_entity: '_1995.GuideDxfModel') -> '_3651.GuideDxfModelCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.GuideDxfModelCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3651.GuideDxfModelCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_guide_dxf_model_load_case(self, design_entity_analysis: '_6121.GuideDxfModelLoadCase') -> '_3651.GuideDxfModelCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GuideDxfModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.GuideDxfModelCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3651.GuideDxfModelCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_imported_fe_component(self, design_entity: '_1998.ImportedFEComponent') -> '_3655.ImportedFEComponentCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ImportedFEComponentCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3655.ImportedFEComponentCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_imported_fe_component_load_case(self, design_entity_analysis: '_6133.ImportedFEComponentLoadCase') -> '_3655.ImportedFEComponentCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ImportedFEComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ImportedFEComponentCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3655.ImportedFEComponentCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_mass_disc(self, design_entity: '_2001.MassDisc') -> '_3666.MassDiscCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.MassDiscCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3666.MassDiscCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_mass_disc_load_case(self, design_entity_analysis: '_6145.MassDiscLoadCase') -> '_3666.MassDiscCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MassDiscLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.MassDiscCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3666.MassDiscCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_measurement_component(self, design_entity: '_2002.MeasurementComponent') -> '_3667.MeasurementComponentCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.MeasurementComponentCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3667.MeasurementComponentCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_measurement_component_load_case(self, design_entity_analysis: '_6146.MeasurementComponentLoadCase') -> '_3667.MeasurementComponentCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MeasurementComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.MeasurementComponentCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3667.MeasurementComponentCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_mountable_component(self, design_entity: '_2003.MountableComponent') -> '_3668.MountableComponentCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.MountableComponentCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3668.MountableComponentCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_mountable_component_load_case(self, design_entity_analysis: '_6148.MountableComponentLoadCase') -> '_3668.MountableComponentCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MountableComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.MountableComponentCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3668.MountableComponentCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_oil_seal(self, design_entity: '_2005.OilSeal') -> '_3669.OilSealCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.OilSealCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3669.OilSealCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_oil_seal_load_case(self, design_entity_analysis: '_6150.OilSealLoadCase') -> '_3669.OilSealCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.OilSealCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3669.OilSealCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_part(self, design_entity: '_2006.Part') -> '_3670.PartCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PartCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3670.PartCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_part_load_case(self, design_entity_analysis: '_6152.PartLoadCase') -> '_3670.PartCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PartCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3670.PartCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_planet_carrier(self, design_entity: '_2007.PlanetCarrier') -> '_3676.PlanetCarrierCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PlanetCarrierCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3676.PlanetCarrierCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_planet_carrier_load_case(self, design_entity_analysis: '_6159.PlanetCarrierLoadCase') -> '_3676.PlanetCarrierCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PlanetCarrierCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3676.PlanetCarrierCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_point_load(self, design_entity: '_2009.PointLoad') -> '_3677.PointLoadCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PointLoadCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3677.PointLoadCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_point_load_load_case(self, design_entity_analysis: '_6162.PointLoadLoadCase') -> '_3677.PointLoadCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PointLoadCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3677.PointLoadCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_power_load(self, design_entity: '_2010.PowerLoad') -> '_3678.PowerLoadCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PowerLoadCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3678.PowerLoadCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_power_load_load_case(self, design_entity_analysis: '_6163.PowerLoadLoadCase') -> '_3678.PowerLoadCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PowerLoadCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3678.PowerLoadCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_root_assembly(self, design_entity: '_2012.RootAssembly') -> '_3683.RootAssemblyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.RootAssemblyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3683.RootAssemblyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_root_assembly_load_case(self, design_entity_analysis: '_6169.RootAssemblyLoadCase') -> '_3683.RootAssemblyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RootAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.RootAssemblyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3683.RootAssemblyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_specialised_assembly(self, design_entity: '_2014.SpecialisedAssembly') -> '_3687.SpecialisedAssemblyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SpecialisedAssemblyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3687.SpecialisedAssemblyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_specialised_assembly_load_case(self, design_entity_analysis: '_6173.SpecialisedAssemblyLoadCase') -> '_3687.SpecialisedAssemblyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpecialisedAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SpecialisedAssemblyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3687.SpecialisedAssemblyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_unbalanced_mass(self, design_entity: '_2015.UnbalancedMass') -> '_3710.UnbalancedMassCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.UnbalancedMassCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3710.UnbalancedMassCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_unbalanced_mass_load_case(self, design_entity_analysis: '_6204.UnbalancedMassLoadCase') -> '_3710.UnbalancedMassCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.UnbalancedMassLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.UnbalancedMassCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3710.UnbalancedMassCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_virtual_component(self, design_entity: '_2016.VirtualComponent') -> '_3711.VirtualComponentCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.VirtualComponentCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3711.VirtualComponentCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_virtual_component_load_case(self, design_entity_analysis: '_6205.VirtualComponentLoadCase') -> '_3711.VirtualComponentCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.VirtualComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.VirtualComponentCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3711.VirtualComponentCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_shaft(self, design_entity: '_2019.Shaft') -> '_3684.ShaftCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ShaftCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3684.ShaftCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_shaft_load_case(self, design_entity_analysis: '_6171.ShaftLoadCase') -> '_3684.ShaftCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ShaftCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3684.ShaftCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_gear(self, design_entity: '_2057.ConceptGear') -> '_3624.ConceptGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConceptGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3624.ConceptGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_gear_load_case(self, design_entity_analysis: '_6072.ConceptGearLoadCase') -> '_3624.ConceptGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConceptGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3624.ConceptGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_gear_set(self, design_entity: '_2058.ConceptGearSet') -> '_3626.ConceptGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConceptGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3626.ConceptGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_gear_set_load_case(self, design_entity_analysis: '_6074.ConceptGearSetLoadCase') -> '_3626.ConceptGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConceptGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3626.ConceptGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_face_gear(self, design_entity: '_2064.FaceGear') -> '_3644.FaceGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.FaceGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3644.FaceGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_face_gear_load_case(self, design_entity_analysis: '_6110.FaceGearLoadCase') -> '_3644.FaceGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.FaceGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3644.FaceGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_face_gear_set(self, design_entity: '_2065.FaceGearSet') -> '_3646.FaceGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.FaceGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3646.FaceGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_face_gear_set_load_case(self, design_entity_analysis: '_6112.FaceGearSetLoadCase') -> '_3646.FaceGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.FaceGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3646.FaceGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear(self, design_entity: '_2049.AGMAGleasonConicalGear') -> '_3599.AGMAGleasonConicalGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.AGMAGleasonConicalGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3599.AGMAGleasonConicalGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_load_case(self, design_entity_analysis: '_6046.AGMAGleasonConicalGearLoadCase') -> '_3599.AGMAGleasonConicalGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.AGMAGleasonConicalGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3599.AGMAGleasonConicalGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_2050.AGMAGleasonConicalGearSet') -> '_3601.AGMAGleasonConicalGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.AGMAGleasonConicalGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3601.AGMAGleasonConicalGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set_load_case(self, design_entity_analysis: '_6048.AGMAGleasonConicalGearSetLoadCase') -> '_3601.AGMAGleasonConicalGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.AGMAGleasonConicalGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3601.AGMAGleasonConicalGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_gear(self, design_entity: '_2051.BevelDifferentialGear') -> '_3606.BevelDifferentialGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelDifferentialGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3606.BevelDifferentialGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_gear_load_case(self, design_entity_analysis: '_6054.BevelDifferentialGearLoadCase') -> '_3606.BevelDifferentialGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelDifferentialGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3606.BevelDifferentialGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set(self, design_entity: '_2052.BevelDifferentialGearSet') -> '_3608.BevelDifferentialGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelDifferentialGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3608.BevelDifferentialGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set_load_case(self, design_entity_analysis: '_6056.BevelDifferentialGearSetLoadCase') -> '_3608.BevelDifferentialGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelDifferentialGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3608.BevelDifferentialGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2053.BevelDifferentialPlanetGear') -> '_3609.BevelDifferentialPlanetGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelDifferentialPlanetGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3609.BevelDifferentialPlanetGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear_load_case(self, design_entity_analysis: '_6057.BevelDifferentialPlanetGearLoadCase') -> '_3609.BevelDifferentialPlanetGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelDifferentialPlanetGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3609.BevelDifferentialPlanetGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2054.BevelDifferentialSunGear') -> '_3610.BevelDifferentialSunGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelDifferentialSunGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3610.BevelDifferentialSunGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear_load_case(self, design_entity_analysis: '_6058.BevelDifferentialSunGearLoadCase') -> '_3610.BevelDifferentialSunGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelDifferentialSunGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3610.BevelDifferentialSunGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_gear(self, design_entity: '_2055.BevelGear') -> '_3611.BevelGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3611.BevelGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_gear_load_case(self, design_entity_analysis: '_6059.BevelGearLoadCase') -> '_3611.BevelGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3611.BevelGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_gear_set(self, design_entity: '_2056.BevelGearSet') -> '_3613.BevelGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3613.BevelGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_gear_set_load_case(self, design_entity_analysis: '_6061.BevelGearSetLoadCase') -> '_3613.BevelGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3613.BevelGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_conical_gear(self, design_entity: '_2059.ConicalGear') -> '_3627.ConicalGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConicalGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3627.ConicalGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_conical_gear_load_case(self, design_entity_analysis: '_6075.ConicalGearLoadCase') -> '_3627.ConicalGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConicalGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3627.ConicalGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_conical_gear_set(self, design_entity: '_2060.ConicalGearSet') -> '_3629.ConicalGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConicalGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3629.ConicalGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_conical_gear_set_load_case(self, design_entity_analysis: '_6079.ConicalGearSetLoadCase') -> '_3629.ConicalGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConicalGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3629.ConicalGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_gear(self, design_entity: '_2061.CylindricalGear') -> '_3638.CylindricalGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CylindricalGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3638.CylindricalGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_gear_load_case(self, design_entity_analysis: '_6088.CylindricalGearLoadCase') -> '_3638.CylindricalGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CylindricalGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3638.CylindricalGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_gear_set(self, design_entity: '_2062.CylindricalGearSet') -> '_3640.CylindricalGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CylindricalGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3640.CylindricalGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_gear_set_load_case(self, design_entity_analysis: '_6092.CylindricalGearSetLoadCase') -> '_3640.CylindricalGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CylindricalGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3640.CylindricalGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear(self, design_entity: '_2063.CylindricalPlanetGear') -> '_3641.CylindricalPlanetGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CylindricalPlanetGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3641.CylindricalPlanetGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear_load_case(self, design_entity_analysis: '_6093.CylindricalPlanetGearLoadCase') -> '_3641.CylindricalPlanetGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CylindricalPlanetGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3641.CylindricalPlanetGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_gear(self, design_entity: '_2066.Gear') -> '_3648.GearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.GearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3648.GearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_gear_load_case(self, design_entity_analysis: '_6115.GearLoadCase') -> '_3648.GearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.GearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3648.GearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_gear_set(self, design_entity: '_2068.GearSet') -> '_3650.GearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.GearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3650.GearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_gear_set_load_case(self, design_entity_analysis: '_6120.GearSetLoadCase') -> '_3650.GearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.GearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3650.GearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_hypoid_gear(self, design_entity: '_2070.HypoidGear') -> '_3652.HypoidGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.HypoidGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3652.HypoidGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_hypoid_gear_load_case(self, design_entity_analysis: '_6130.HypoidGearLoadCase') -> '_3652.HypoidGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.HypoidGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3652.HypoidGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_hypoid_gear_set(self, design_entity: '_2071.HypoidGearSet') -> '_3654.HypoidGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.HypoidGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3654.HypoidGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_hypoid_gear_set_load_case(self, design_entity_analysis: '_6132.HypoidGearSetLoadCase') -> '_3654.HypoidGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.HypoidGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3654.HypoidGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2072.KlingelnbergCycloPalloidConicalGear') -> '_3657.KlingelnbergCycloPalloidConicalGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidConicalGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3657.KlingelnbergCycloPalloidConicalGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_load_case(self, design_entity_analysis: '_6136.KlingelnbergCycloPalloidConicalGearLoadCase') -> '_3657.KlingelnbergCycloPalloidConicalGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidConicalGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3657.KlingelnbergCycloPalloidConicalGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2073.KlingelnbergCycloPalloidConicalGearSet') -> '_3659.KlingelnbergCycloPalloidConicalGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidConicalGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3659.KlingelnbergCycloPalloidConicalGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set_load_case(self, design_entity_analysis: '_6138.KlingelnbergCycloPalloidConicalGearSetLoadCase') -> '_3659.KlingelnbergCycloPalloidConicalGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidConicalGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3659.KlingelnbergCycloPalloidConicalGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2074.KlingelnbergCycloPalloidHypoidGear') -> '_3660.KlingelnbergCycloPalloidHypoidGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidHypoidGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3660.KlingelnbergCycloPalloidHypoidGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_load_case(self, design_entity_analysis: '_6139.KlingelnbergCycloPalloidHypoidGearLoadCase') -> '_3660.KlingelnbergCycloPalloidHypoidGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidHypoidGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3660.KlingelnbergCycloPalloidHypoidGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2075.KlingelnbergCycloPalloidHypoidGearSet') -> '_3662.KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3662.KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(self, design_entity_analysis: '_6141.KlingelnbergCycloPalloidHypoidGearSetLoadCase') -> '_3662.KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3662.KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2076.KlingelnbergCycloPalloidSpiralBevelGear') -> '_3663.KlingelnbergCycloPalloidSpiralBevelGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidSpiralBevelGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3663.KlingelnbergCycloPalloidSpiralBevelGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(self, design_entity_analysis: '_6142.KlingelnbergCycloPalloidSpiralBevelGearLoadCase') -> '_3663.KlingelnbergCycloPalloidSpiralBevelGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidSpiralBevelGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3663.KlingelnbergCycloPalloidSpiralBevelGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2077.KlingelnbergCycloPalloidSpiralBevelGearSet') -> '_3665.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3665.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_6144.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase') -> '_3665.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3665.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_planetary_gear_set(self, design_entity: '_2078.PlanetaryGearSet') -> '_3675.PlanetaryGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PlanetaryGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3675.PlanetaryGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_planetary_gear_set_load_case(self, design_entity_analysis: '_6157.PlanetaryGearSetLoadCase') -> '_3675.PlanetaryGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PlanetaryGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3675.PlanetaryGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_spiral_bevel_gear(self, design_entity: '_2079.SpiralBevelGear') -> '_3688.SpiralBevelGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SpiralBevelGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3688.SpiralBevelGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_load_case(self, design_entity_analysis: '_6175.SpiralBevelGearLoadCase') -> '_3688.SpiralBevelGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SpiralBevelGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3688.SpiralBevelGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set(self, design_entity: '_2080.SpiralBevelGearSet') -> '_3690.SpiralBevelGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SpiralBevelGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3690.SpiralBevelGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_6177.SpiralBevelGearSetLoadCase') -> '_3690.SpiralBevelGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SpiralBevelGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3690.SpiralBevelGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2081.StraightBevelDiffGear') -> '_3694.StraightBevelDiffGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelDiffGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3694.StraightBevelDiffGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_load_case(self, design_entity_analysis: '_6182.StraightBevelDiffGearLoadCase') -> '_3694.StraightBevelDiffGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelDiffGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3694.StraightBevelDiffGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_2082.StraightBevelDiffGearSet') -> '_3696.StraightBevelDiffGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelDiffGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3696.StraightBevelDiffGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set_load_case(self, design_entity_analysis: '_6184.StraightBevelDiffGearSetLoadCase') -> '_3696.StraightBevelDiffGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelDiffGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3696.StraightBevelDiffGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_gear(self, design_entity: '_2083.StraightBevelGear') -> '_3697.StraightBevelGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3697.StraightBevelGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_gear_load_case(self, design_entity_analysis: '_6185.StraightBevelGearLoadCase') -> '_3697.StraightBevelGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3697.StraightBevelGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set(self, design_entity: '_2084.StraightBevelGearSet') -> '_3699.StraightBevelGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3699.StraightBevelGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set_load_case(self, design_entity_analysis: '_6187.StraightBevelGearSetLoadCase') -> '_3699.StraightBevelGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3699.StraightBevelGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2085.StraightBevelPlanetGear') -> '_3700.StraightBevelPlanetGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelPlanetGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3700.StraightBevelPlanetGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear_load_case(self, design_entity_analysis: '_6188.StraightBevelPlanetGearLoadCase') -> '_3700.StraightBevelPlanetGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelPlanetGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3700.StraightBevelPlanetGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2086.StraightBevelSunGear') -> '_3701.StraightBevelSunGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelSunGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3701.StraightBevelSunGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear_load_case(self, design_entity_analysis: '_6189.StraightBevelSunGearLoadCase') -> '_3701.StraightBevelSunGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelSunGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3701.StraightBevelSunGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_worm_gear(self, design_entity: '_2087.WormGear') -> '_3712.WormGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.WormGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3712.WormGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_worm_gear_load_case(self, design_entity_analysis: '_6206.WormGearLoadCase') -> '_3712.WormGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.WormGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3712.WormGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_worm_gear_set(self, design_entity: '_2088.WormGearSet') -> '_3714.WormGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.WormGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3714.WormGearSetCompoundParametricStudyTool)(method_result) if method_result else None
