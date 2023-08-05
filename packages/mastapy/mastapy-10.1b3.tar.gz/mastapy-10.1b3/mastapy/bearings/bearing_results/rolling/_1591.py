'''_1591.py

LoadedBallBearingDutyCycle
'''


from mastapy._internal import constructor
from mastapy.utility.property import _1329
from mastapy.bearings.bearing_results.rolling import _1594
from mastapy.bearings.bearing_results import _1559
from mastapy._internal.python_net import python_net_import

_LOADED_BALL_BEARING_DUTY_CYCLE = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedBallBearingDutyCycle')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedBallBearingDutyCycle',)


class LoadedBallBearingDutyCycle(_1559.LoadedRollingBearingDutyCycle):
    '''LoadedBallBearingDutyCycle

    This is a mastapy class.
    '''

    TYPE = _LOADED_BALL_BEARING_DUTY_CYCLE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedBallBearingDutyCycle.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def track_truncation_safety_factor(self) -> 'float':
        '''float: 'TrackTruncationSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TrackTruncationSafetyFactor

    @property
    def track_truncation_inner_summary(self) -> '_1329.DutyCyclePropertySummaryPercentage[_1594.LoadedBallBearingResults]':
        '''DutyCyclePropertySummaryPercentage[LoadedBallBearingResults]: 'TrackTruncationInnerSummary' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1329.DutyCyclePropertySummaryPercentage)[_1594.LoadedBallBearingResults](self.wrapped.TrackTruncationInnerSummary) if self.wrapped.TrackTruncationInnerSummary else None

    @property
    def track_truncation_outer_summary(self) -> '_1329.DutyCyclePropertySummaryPercentage[_1594.LoadedBallBearingResults]':
        '''DutyCyclePropertySummaryPercentage[LoadedBallBearingResults]: 'TrackTruncationOuterSummary' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1329.DutyCyclePropertySummaryPercentage)[_1594.LoadedBallBearingResults](self.wrapped.TrackTruncationOuterSummary) if self.wrapped.TrackTruncationOuterSummary else None
