'''_3754.py

CouplingHalfModalAnalysesAtStiffnesses
'''


from mastapy.system_model.part_model.couplings import (
    _2116, _2111, _2114, _2118,
    _2120, _2121, _2127, _2131,
    _2134, _2135, _2136, _2138,
    _2140
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3792
from mastapy._internal.python_net import python_net_import

_COUPLING_HALF_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'CouplingHalfModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingHalfModalAnalysesAtStiffnesses',)


class CouplingHalfModalAnalysesAtStiffnesses(_3792.MountableComponentModalAnalysesAtStiffnesses):
    '''CouplingHalfModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _COUPLING_HALF_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingHalfModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2116.CouplingHalf':
        '''CouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2116.CouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_clutch_half(self) -> '_2111.ClutchHalf':
        '''ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2111.ClutchHalf.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ClutchHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2111.ClutchHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_concept_coupling_half(self) -> '_2114.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2114.ConceptCouplingHalf.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2114.ConceptCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cvt_pulley(self) -> '_2118.CVTPulley':
        '''CVTPulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2118.CVTPulley.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CVTPulley. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2118.CVTPulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_part_to_part_shear_coupling_half(self) -> '_2120.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2120.PartToPartShearCouplingHalf.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2120.PartToPartShearCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_pulley(self) -> '_2121.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2121.Pulley.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Pulley. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2121.Pulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_rolling_ring(self) -> '_2127.RollingRing':
        '''RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2127.RollingRing.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to RollingRing. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2127.RollingRing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_spring_damper_half(self) -> '_2131.SpringDamperHalf':
        '''SpringDamperHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2131.SpringDamperHalf.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SpringDamperHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2131.SpringDamperHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_synchroniser_half(self) -> '_2134.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2134.SynchroniserHalf.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SynchroniserHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2134.SynchroniserHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_synchroniser_part(self) -> '_2135.SynchroniserPart':
        '''SynchroniserPart: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2135.SynchroniserPart.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SynchroniserPart. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2135.SynchroniserPart)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_synchroniser_sleeve(self) -> '_2136.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2136.SynchroniserSleeve.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2136.SynchroniserSleeve)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_torque_converter_pump(self) -> '_2138.TorqueConverterPump':
        '''TorqueConverterPump: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2138.TorqueConverterPump.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to TorqueConverterPump. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2138.TorqueConverterPump)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_torque_converter_turbine(self) -> '_2140.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2140.TorqueConverterTurbine.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2140.TorqueConverterTurbine)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
