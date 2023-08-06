'''_683.py

MicroGeometryDesignSpaceSearchCandidate
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy.gears.ltca.cylindrical import _631
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _849
from mastapy.gears.gear_set_pareto_optimiser import _673
from mastapy._internal.python_net import python_net_import

_MICRO_GEOMETRY_DESIGN_SPACE_SEARCH_CANDIDATE = python_net_import('SMT.MastaAPI.Gears.GearSetParetoOptimiser', 'MicroGeometryDesignSpaceSearchCandidate')


__docformat__ = 'restructuredtext en'
__all__ = ('MicroGeometryDesignSpaceSearchCandidate',)


class MicroGeometryDesignSpaceSearchCandidate(_673.DesignSpaceSearchCandidateBase['_631.CylindricalGearSetLoadDistributionAnalysis', 'MicroGeometryDesignSpaceSearchCandidate']):
    '''MicroGeometryDesignSpaceSearchCandidate

    This is a mastapy class.
    '''

    TYPE = _MICRO_GEOMETRY_DESIGN_SPACE_SEARCH_CANDIDATE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MicroGeometryDesignSpaceSearchCandidate.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def add_design(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'AddDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddDesign

    @property
    def candidate(self) -> '_631.CylindricalGearSetLoadDistributionAnalysis':
        '''CylindricalGearSetLoadDistributionAnalysis: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_631.CylindricalGearSetLoadDistributionAnalysis)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_for_slider(self) -> '_849.CylindricalGearSetMicroGeometry':
        '''CylindricalGearSetMicroGeometry: 'CandidateForSlider' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_849.CylindricalGearSetMicroGeometry)(self.wrapped.CandidateForSlider) if self.wrapped.CandidateForSlider else None
