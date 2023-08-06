'''_5026.py

MultiBodyDynamicsAnalysis
'''


from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.mbd_analyses import _5022
from mastapy.nodal_analysis.system_solvers import (
    _1401, _1383, _1384, _1387,
    _1388, _1389, _1390, _1391,
    _1392, _1393, _1394, _1399,
    _1402
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.analysis_cases import _6474
from mastapy._internal.python_net import python_net_import

_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'MultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MultiBodyDynamicsAnalysis',)


class MultiBodyDynamicsAnalysis(_6474.TimeSeriesLoadAnalysisCase):
    '''MultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def percentage_time_spent_in_masta_solver(self) -> 'float':
        '''float: 'PercentageTimeSpentInMASTASolver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PercentageTimeSpentInMASTASolver

    @property
    def has_interface_analysis_results_available(self) -> 'bool':
        '''bool: 'HasInterfaceAnalysisResultsAvailable' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HasInterfaceAnalysisResultsAvailable

    @property
    def mbd_options(self) -> '_5022.MBDAnalysisOptions':
        '''MBDAnalysisOptions: 'MBDOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5022.MBDAnalysisOptions)(self.wrapped.MBDOptions) if self.wrapped.MBDOptions else None

    @property
    def transient_solver(self) -> '_1401.TransientSolver':
        '''TransientSolver: 'TransientSolver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1401.TransientSolver)(self.wrapped.TransientSolver) if self.wrapped.TransientSolver else None

    @property
    def transient_solver_of_type_backward_euler_acceleration_step_halving_transient_solver(self) -> '_1383.BackwardEulerAccelerationStepHalvingTransientSolver':
        '''BackwardEulerAccelerationStepHalvingTransientSolver: 'TransientSolver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1383.BackwardEulerAccelerationStepHalvingTransientSolver.TYPE not in self.wrapped.TransientSolver.__class__.__mro__:
            raise CastException('Failed to cast transient_solver to BackwardEulerAccelerationStepHalvingTransientSolver. Expected: {}.'.format(self.wrapped.TransientSolver.__class__.__qualname__))

        return constructor.new(_1383.BackwardEulerAccelerationStepHalvingTransientSolver)(self.wrapped.TransientSolver) if self.wrapped.TransientSolver else None

    @property
    def transient_solver_of_type_backward_euler_transient_solver(self) -> '_1384.BackwardEulerTransientSolver':
        '''BackwardEulerTransientSolver: 'TransientSolver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1384.BackwardEulerTransientSolver.TYPE not in self.wrapped.TransientSolver.__class__.__mro__:
            raise CastException('Failed to cast transient_solver to BackwardEulerTransientSolver. Expected: {}.'.format(self.wrapped.TransientSolver.__class__.__qualname__))

        return constructor.new(_1384.BackwardEulerTransientSolver)(self.wrapped.TransientSolver) if self.wrapped.TransientSolver else None

    @property
    def transient_solver_of_type_internal_transient_solver(self) -> '_1387.InternalTransientSolver':
        '''InternalTransientSolver: 'TransientSolver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1387.InternalTransientSolver.TYPE not in self.wrapped.TransientSolver.__class__.__mro__:
            raise CastException('Failed to cast transient_solver to InternalTransientSolver. Expected: {}.'.format(self.wrapped.TransientSolver.__class__.__qualname__))

        return constructor.new(_1387.InternalTransientSolver)(self.wrapped.TransientSolver) if self.wrapped.TransientSolver else None

    @property
    def transient_solver_of_type_lobatto_iiia_transient_solver(self) -> '_1388.LobattoIIIATransientSolver':
        '''LobattoIIIATransientSolver: 'TransientSolver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1388.LobattoIIIATransientSolver.TYPE not in self.wrapped.TransientSolver.__class__.__mro__:
            raise CastException('Failed to cast transient_solver to LobattoIIIATransientSolver. Expected: {}.'.format(self.wrapped.TransientSolver.__class__.__qualname__))

        return constructor.new(_1388.LobattoIIIATransientSolver)(self.wrapped.TransientSolver) if self.wrapped.TransientSolver else None

    @property
    def transient_solver_of_type_lobatto_iiic_transient_solver(self) -> '_1389.LobattoIIICTransientSolver':
        '''LobattoIIICTransientSolver: 'TransientSolver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1389.LobattoIIICTransientSolver.TYPE not in self.wrapped.TransientSolver.__class__.__mro__:
            raise CastException('Failed to cast transient_solver to LobattoIIICTransientSolver. Expected: {}.'.format(self.wrapped.TransientSolver.__class__.__qualname__))

        return constructor.new(_1389.LobattoIIICTransientSolver)(self.wrapped.TransientSolver) if self.wrapped.TransientSolver else None

    @property
    def transient_solver_of_type_newmark_acceleration_transient_solver(self) -> '_1390.NewmarkAccelerationTransientSolver':
        '''NewmarkAccelerationTransientSolver: 'TransientSolver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1390.NewmarkAccelerationTransientSolver.TYPE not in self.wrapped.TransientSolver.__class__.__mro__:
            raise CastException('Failed to cast transient_solver to NewmarkAccelerationTransientSolver. Expected: {}.'.format(self.wrapped.TransientSolver.__class__.__qualname__))

        return constructor.new(_1390.NewmarkAccelerationTransientSolver)(self.wrapped.TransientSolver) if self.wrapped.TransientSolver else None

    @property
    def transient_solver_of_type_newmark_transient_solver(self) -> '_1391.NewmarkTransientSolver':
        '''NewmarkTransientSolver: 'TransientSolver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1391.NewmarkTransientSolver.TYPE not in self.wrapped.TransientSolver.__class__.__mro__:
            raise CastException('Failed to cast transient_solver to NewmarkTransientSolver. Expected: {}.'.format(self.wrapped.TransientSolver.__class__.__qualname__))

        return constructor.new(_1391.NewmarkTransientSolver)(self.wrapped.TransientSolver) if self.wrapped.TransientSolver else None

    @property
    def transient_solver_of_type_semi_implicit_transient_solver(self) -> '_1392.SemiImplicitTransientSolver':
        '''SemiImplicitTransientSolver: 'TransientSolver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1392.SemiImplicitTransientSolver.TYPE not in self.wrapped.TransientSolver.__class__.__mro__:
            raise CastException('Failed to cast transient_solver to SemiImplicitTransientSolver. Expected: {}.'.format(self.wrapped.TransientSolver.__class__.__qualname__))

        return constructor.new(_1392.SemiImplicitTransientSolver)(self.wrapped.TransientSolver) if self.wrapped.TransientSolver else None

    @property
    def transient_solver_of_type_simple_acceleration_based_step_halving_transient_solver(self) -> '_1393.SimpleAccelerationBasedStepHalvingTransientSolver':
        '''SimpleAccelerationBasedStepHalvingTransientSolver: 'TransientSolver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1393.SimpleAccelerationBasedStepHalvingTransientSolver.TYPE not in self.wrapped.TransientSolver.__class__.__mro__:
            raise CastException('Failed to cast transient_solver to SimpleAccelerationBasedStepHalvingTransientSolver. Expected: {}.'.format(self.wrapped.TransientSolver.__class__.__qualname__))

        return constructor.new(_1393.SimpleAccelerationBasedStepHalvingTransientSolver)(self.wrapped.TransientSolver) if self.wrapped.TransientSolver else None

    @property
    def transient_solver_of_type_simple_velocity_based_step_halving_transient_solver(self) -> '_1394.SimpleVelocityBasedStepHalvingTransientSolver':
        '''SimpleVelocityBasedStepHalvingTransientSolver: 'TransientSolver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1394.SimpleVelocityBasedStepHalvingTransientSolver.TYPE not in self.wrapped.TransientSolver.__class__.__mro__:
            raise CastException('Failed to cast transient_solver to SimpleVelocityBasedStepHalvingTransientSolver. Expected: {}.'.format(self.wrapped.TransientSolver.__class__.__qualname__))

        return constructor.new(_1394.SimpleVelocityBasedStepHalvingTransientSolver)(self.wrapped.TransientSolver) if self.wrapped.TransientSolver else None

    @property
    def transient_solver_of_type_step_halving_transient_solver(self) -> '_1399.StepHalvingTransientSolver':
        '''StepHalvingTransientSolver: 'TransientSolver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1399.StepHalvingTransientSolver.TYPE not in self.wrapped.TransientSolver.__class__.__mro__:
            raise CastException('Failed to cast transient_solver to StepHalvingTransientSolver. Expected: {}.'.format(self.wrapped.TransientSolver.__class__.__qualname__))

        return constructor.new(_1399.StepHalvingTransientSolver)(self.wrapped.TransientSolver) if self.wrapped.TransientSolver else None

    @property
    def transient_solver_of_type_wilson_theta_transient_solver(self) -> '_1402.WilsonThetaTransientSolver':
        '''WilsonThetaTransientSolver: 'TransientSolver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1402.WilsonThetaTransientSolver.TYPE not in self.wrapped.TransientSolver.__class__.__mro__:
            raise CastException('Failed to cast transient_solver to WilsonThetaTransientSolver. Expected: {}.'.format(self.wrapped.TransientSolver.__class__.__qualname__))

        return constructor.new(_1402.WilsonThetaTransientSolver)(self.wrapped.TransientSolver) if self.wrapped.TransientSolver else None
