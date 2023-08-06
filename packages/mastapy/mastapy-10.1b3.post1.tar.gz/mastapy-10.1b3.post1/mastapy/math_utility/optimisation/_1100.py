'''_1100.py

ParetoOptimisationStrategy
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.math_utility.optimisation import _1098, _1099, _1102
from mastapy.utility.databases import _1340
from mastapy._internal.python_net import python_net_import

_PARETO_OPTIMISATION_STRATEGY = python_net_import('SMT.MastaAPI.MathUtility.Optimisation', 'ParetoOptimisationStrategy')


__docformat__ = 'restructuredtext en'
__all__ = ('ParetoOptimisationStrategy',)


class ParetoOptimisationStrategy(_1340.NamedDatabaseItem):
    '''ParetoOptimisationStrategy

    This is a mastapy class.
    '''

    TYPE = _PARETO_OPTIMISATION_STRATEGY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ParetoOptimisationStrategy.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def add_chart(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'AddChart' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddChart

    @property
    def inputs(self) -> 'List[_1098.ParetoOptimisationInput]':
        '''List[ParetoOptimisationInput]: 'Inputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Inputs, constructor.new(_1098.ParetoOptimisationInput))
        return value

    @property
    def outputs(self) -> 'List[_1099.ParetoOptimisationOutput]':
        '''List[ParetoOptimisationOutput]: 'Outputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Outputs, constructor.new(_1099.ParetoOptimisationOutput))
        return value

    @property
    def charts(self) -> 'List[_1102.ParetoOptimisationStrategyChartInformation]':
        '''List[ParetoOptimisationStrategyChartInformation]: 'Charts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Charts, constructor.new(_1102.ParetoOptimisationStrategyChartInformation))
        return value
