'''_1372.py

FEStiffnessTester
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.nodal_analysis import _1370
from mastapy.gears.ltca import _609, _611, _619
from mastapy._internal.cast_exception import CastException
from mastapy.gears.ltca.cylindrical import _622, _624
from mastapy.gears.ltca.conical import _634, _636
from mastapy.system_model.imported_fes import _1932
from mastapy.math_utility.measured_vectors import _1111
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_FE_STIFFNESS_TESTER = python_net_import('SMT.MastaAPI.NodalAnalysis', 'FEStiffnessTester')


__docformat__ = 'restructuredtext en'
__all__ = ('FEStiffnessTester',)


class FEStiffnessTester(_0.APIBase):
    '''FEStiffnessTester

    This is a mastapy class.
    '''

    TYPE = _FE_STIFFNESS_TESTER

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEStiffnessTester.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def force_scaling_factor(self) -> 'float':
        '''float: 'ForceScalingFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ForceScalingFactor

    @property
    def displacement_scaling_factor(self) -> 'float':
        '''float: 'DisplacementScalingFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DisplacementScalingFactor

    @property
    def fe_stiffness(self) -> '_1370.FEStiffness':
        '''FEStiffness: 'FEStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1370.FEStiffness)(self.wrapped.FEStiffness) if self.wrapped.FEStiffness else None

    @property
    def fe_stiffness_of_type_gear_bending_stiffness(self) -> '_609.GearBendingStiffness':
        '''GearBendingStiffness: 'FEStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _609.GearBendingStiffness.TYPE not in self.wrapped.FEStiffness.__class__.__mro__:
            raise CastException('Failed to cast fe_stiffness to GearBendingStiffness. Expected: {}.'.format(self.wrapped.FEStiffness.__class__.__qualname__))

        return constructor.new(_609.GearBendingStiffness)(self.wrapped.FEStiffness) if self.wrapped.FEStiffness else None

    @property
    def fe_stiffness_of_type_gear_contact_stiffness(self) -> '_611.GearContactStiffness':
        '''GearContactStiffness: 'FEStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _611.GearContactStiffness.TYPE not in self.wrapped.FEStiffness.__class__.__mro__:
            raise CastException('Failed to cast fe_stiffness to GearContactStiffness. Expected: {}.'.format(self.wrapped.FEStiffness.__class__.__qualname__))

        return constructor.new(_611.GearContactStiffness)(self.wrapped.FEStiffness) if self.wrapped.FEStiffness else None

    @property
    def fe_stiffness_of_type_gear_stiffness(self) -> '_619.GearStiffness':
        '''GearStiffness: 'FEStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _619.GearStiffness.TYPE not in self.wrapped.FEStiffness.__class__.__mro__:
            raise CastException('Failed to cast fe_stiffness to GearStiffness. Expected: {}.'.format(self.wrapped.FEStiffness.__class__.__qualname__))

        return constructor.new(_619.GearStiffness)(self.wrapped.FEStiffness) if self.wrapped.FEStiffness else None

    @property
    def fe_stiffness_of_type_cylindrical_gear_bending_stiffness(self) -> '_622.CylindricalGearBendingStiffness':
        '''CylindricalGearBendingStiffness: 'FEStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _622.CylindricalGearBendingStiffness.TYPE not in self.wrapped.FEStiffness.__class__.__mro__:
            raise CastException('Failed to cast fe_stiffness to CylindricalGearBendingStiffness. Expected: {}.'.format(self.wrapped.FEStiffness.__class__.__qualname__))

        return constructor.new(_622.CylindricalGearBendingStiffness)(self.wrapped.FEStiffness) if self.wrapped.FEStiffness else None

    @property
    def fe_stiffness_of_type_cylindrical_gear_contact_stiffness(self) -> '_624.CylindricalGearContactStiffness':
        '''CylindricalGearContactStiffness: 'FEStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _624.CylindricalGearContactStiffness.TYPE not in self.wrapped.FEStiffness.__class__.__mro__:
            raise CastException('Failed to cast fe_stiffness to CylindricalGearContactStiffness. Expected: {}.'.format(self.wrapped.FEStiffness.__class__.__qualname__))

        return constructor.new(_624.CylindricalGearContactStiffness)(self.wrapped.FEStiffness) if self.wrapped.FEStiffness else None

    @property
    def fe_stiffness_of_type_conical_gear_bending_stiffness(self) -> '_634.ConicalGearBendingStiffness':
        '''ConicalGearBendingStiffness: 'FEStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _634.ConicalGearBendingStiffness.TYPE not in self.wrapped.FEStiffness.__class__.__mro__:
            raise CastException('Failed to cast fe_stiffness to ConicalGearBendingStiffness. Expected: {}.'.format(self.wrapped.FEStiffness.__class__.__qualname__))

        return constructor.new(_634.ConicalGearBendingStiffness)(self.wrapped.FEStiffness) if self.wrapped.FEStiffness else None

    @property
    def fe_stiffness_of_type_conical_gear_contact_stiffness(self) -> '_636.ConicalGearContactStiffness':
        '''ConicalGearContactStiffness: 'FEStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _636.ConicalGearContactStiffness.TYPE not in self.wrapped.FEStiffness.__class__.__mro__:
            raise CastException('Failed to cast fe_stiffness to ConicalGearContactStiffness. Expected: {}.'.format(self.wrapped.FEStiffness.__class__.__qualname__))

        return constructor.new(_636.ConicalGearContactStiffness)(self.wrapped.FEStiffness) if self.wrapped.FEStiffness else None

    @property
    def fe_stiffness_of_type_imported_fe(self) -> '_1932.ImportedFE':
        '''ImportedFE: 'FEStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1932.ImportedFE.TYPE not in self.wrapped.FEStiffness.__class__.__mro__:
            raise CastException('Failed to cast fe_stiffness to ImportedFE. Expected: {}.'.format(self.wrapped.FEStiffness.__class__.__qualname__))

        return constructor.new(_1932.ImportedFE)(self.wrapped.FEStiffness) if self.wrapped.FEStiffness else None

    @property
    def force_and_displacement_results(self) -> 'List[_1111.ForceAndDisplacementResults]':
        '''List[ForceAndDisplacementResults]: 'ForceAndDisplacementResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ForceAndDisplacementResults, constructor.new(_1111.ForceAndDisplacementResults))
        return value

    @property
    def report_names(self) -> 'List[str]':
        '''List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReportNames

    def output_default_report_to(self, file_path: 'str'):
        ''' 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else None)

    def get_default_report_with_encoded_images(self) -> 'str':
        ''' 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        ''' 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else None)

    def output_active_report_as_text_to(self, file_path: 'str'):
        ''' 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else None)

    def get_active_report_with_encoded_images(self) -> 'str':
        ''' 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else None, file_path if file_path else None)

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        ''' 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        '''

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else None)
        return method_result
