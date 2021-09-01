"""View classes for nautobot_bgp_models."""

from django.shortcuts import get_object_or_404
from nautobot.core.views import generic
from nautobot.dcim.models import Device, Interface
from nautobot.virtualization.models import VirtualMachine, VMInterface

from . import filters, forms, models, tables


class AutonomousSystemListView(generic.ObjectListView):
    """List/table view of AutonomousSystem records."""

    queryset = models.AutonomousSystem.objects.all()
    table = tables.AutonomousSystemTable
    filterset = filters.AutonomousSystemFilterSet
    filterset_form = forms.AutonomousSystemFilterForm
    action_buttons = ("add", "import", "export")


class AutonomousSystemView(generic.ObjectView):
    """Detail view of a single AutonomousSystem."""

    queryset = models.AutonomousSystem.objects.all()


class AutonomousSystemEditView(generic.ObjectEditView):
    """Create/edit view for an AutonomousSystem."""

    queryset = models.AutonomousSystem.objects.all()
    model_form = forms.AutonomousSystemForm


class AutonomousSystemDeleteView(generic.ObjectDeleteView):
    """Delete view for an AutonomousSystem."""

    queryset = models.AutonomousSystem.objects.all()


class AutonomousSystemBulkImportView(generic.BulkImportView):
    """Bulk-importing view for multiple AutonomousSystems."""

    queryset = models.AutonomousSystem.objects.all()
    model_form = forms.AutonomousSystemCSVForm
    table = tables.AutonomousSystemTable


class AutonomousSystemBulkEditView(generic.BulkEditView):
    """Bulk-editing view for multiple AutonomousSystems."""

    queryset = models.AutonomousSystem.objects.all()
    filterset = filters.AutonomousSystemFilterSet
    table = tables.AutonomousSystemTable
    form = forms.AutonomousSystemBulkEditForm


class AutonomousSystemBulkDeleteView(generic.BulkDeleteView):
    """Bulk-deleting view for multiple AutonomousSystems."""

    queryset = models.AutonomousSystem.objects.all()
    filterset = filters.AutonomousSystemFilterSet
    table = tables.AutonomousSystemTable


class BGPRoutingInstanceListView(generic.ObjectListView):
    """List/table view of BGPRoutingInstance records."""

    queryset = models.BGPRoutingInstance.objects.all()
    table = tables.BGPRoutingInstanceTable
    filterset = filters.BGPRoutingInstanceFilterSet
    filterset_form = forms.BGPRoutingInstanceFilterForm
    action_buttons = ("add")


class BGPRoutingInstanceView(generic.ObjectView):
    """Detail view of a single BGPRoutingInstance."""

    queryset = models.BGPRoutingInstance.objects.all()


class BGPRoutingInstanceEditView(generic.ObjectEditView):
    """Create/edit view for an BGPRoutingInstance."""

    queryset = models.BGPRoutingInstance.objects.all()
    model_form = forms.BGPRoutingInstanceForm


class BGPRoutingInstanceDeleteView(generic.ObjectDeleteView):
    """Delete view for an BGPRoutingInstance."""

    queryset = models.BGPRoutingInstance.objects.all()


class BGPRoutingInstanceBulkEditView(generic.BulkEditView):
    """Bulk-editing view for multiple BGPRoutingInstances."""

    queryset = models.BGPRoutingInstance.objects.all()
    filterset = filters.BGPRoutingInstanceFilterSet
    table = tables.BGPRoutingInstanceTable
    form = forms.BGPRoutingInstanceBulkEditForm


class BGPRoutingInstanceBulkDeleteView(generic.BulkDeleteView):
    """Bulk-deleting view for multiple BGPRoutingInstances."""

    queryset = models.BGPRoutingInstance.objects.all()
    filterset = filters.BGPRoutingInstanceFilterSet
    table = tables.BGPRoutingInstanceTable


class PeeringRoleListView(generic.ObjectListView):
    """List/table view of PeeringRole records."""

    queryset = models.PeeringRole.objects.all()
    table = tables.PeeringRoleTable
    filterset = filters.PeeringRoleFilterSet
    filterset_form = forms.PeeringRoleFilterForm
    action_buttons = ("add", "import", "export")


class PeeringRoleView(generic.ObjectView):
    """Detail view of a single PeeringRole."""

    queryset = models.PeeringRole.objects.all()


class PeeringRoleEditView(generic.ObjectEditView):
    """Create/edit view for a PeeringRole."""

    queryset = models.PeeringRole.objects.all()
    model_form = forms.PeeringRoleForm


class PeeringRoleDeleteView(generic.ObjectDeleteView):
    """Delete view for a PeeringRole."""

    queryset = models.PeeringRole.objects.all()


class PeeringRoleBulkImportView(generic.BulkImportView):
    """Bulk-importing view for multiple PeeringRoles."""

    queryset = models.PeeringRole.objects.all()
    model_form = forms.PeeringRoleCSVForm
    table = tables.PeeringRoleTable


class PeeringRoleBulkEditView(generic.BulkEditView):
    """Bulk-editing view for multiple PeeringRoles."""

    queryset = models.PeeringRole.objects.all()
    filterset = filters.PeeringRoleFilterSet
    table = tables.PeeringRoleTable
    form = forms.PeeringRoleBulkEditForm


class PeeringRoleBulkDeleteView(generic.BulkDeleteView):
    """Bulk-deleting view for multiple PeeringRoles."""

    queryset = models.PeeringRole.objects.all()
    filterset = filters.PeeringRoleFilterSet
    table = tables.PeeringRoleTable


class PeerGroupListView(generic.ObjectListView):
    """List/table view of PeerGroup records."""

    queryset = models.PeerGroup.objects.all()
    table = tables.PeerGroupTable
    filterset = filters.PeerGroupFilterSet
    filterset_form = forms.PeerGroupFilterForm
    action_buttons = ("add",)


class PeerGroupView(generic.ObjectView):
    """Detail view of a single PeerGroup."""

    queryset = models.PeerGroup.objects.all()

    def get_extra_context(self, request, instance):
        """Return any additional context data for the template."""
        return {"object_fields": instance.get_fields(include_inherited=True)}


class PeerGroupEditView(generic.ObjectEditView):
    """Create/edit view for a PeerGroup."""

    queryset = models.PeerGroup.objects.all()
    model_form = forms.PeerGroupForm


class PeerGroupDeleteView(generic.ObjectDeleteView):
    """Delete view for a PeerGroup."""

    queryset = models.PeerGroup.objects.all()


class PeerGroupBulkEditView(generic.BulkEditView):
    """Bulk-editing view for multiple PeerGroup."""

    queryset = models.PeerGroup.objects.all()
    filterset = filters.PeerGroupFilterSet
    table = tables.PeerGroupTable
    form = forms.PeerGroupBulkEditForm


class PeerGroupBulkDeleteView(generic.BulkDeleteView):
    """Bulk-deleting view for multiple PeerGroup."""

    queryset = models.PeerGroup.objects.all()
    filterset = filters.PeerGroupFilterSet
    table = tables.PeerGroupTable


class PeerGroupTemplateView(generic.ObjectView):
    """Detail view of a single PeerGroupTemplate."""

    queryset = models.PeerGroupTemplate.objects.all()

    # def get_extra_context(self, request, instance):
    #     """Return any additional context data for the template."""
    #     return {"object_fields": instance.get_fields(include_inherited=True)}


class PeerGroupTemplateListView(generic.ObjectListView):
    """List/table view of PeerGroupTemplate records."""

    queryset = models.PeerGroupTemplate.objects.all()
    table = tables.PeerGroupTemplateTable
    filterset = filters.PeerGroupTemplateFilterSet
    filterset_form = forms.PeerGroupTemplateFilterForm
    action_buttons = ("add",)


class PeerGroupTemplateEditView(generic.ObjectEditView):
    """Create/edit view for a PeerGroupTemplate."""

    queryset = models.PeerGroupTemplate.objects.all()
    model_form = forms.PeerGroupTemplateForm


class PeerGroupTemplateDeleteView(generic.ObjectDeleteView):
    """Delete view for a PeerGroup."""

    queryset = models.PeerGroupTemplate.objects.all()


class PeerGroupTemplateBulkEditView(generic.BulkEditView):
    """Bulk-editing view for multiple PeerGroupTemplate."""

    queryset = models.PeerGroupTemplate.objects.all()
    filterset = filters.PeerGroupTemplateFilterSet
    table = tables.PeerGroupTemplateTable
    form = forms.PeerGroupTemplateBulkEditForm


class PeerGroupTemplateBulkDeleteView(generic.BulkDeleteView):
    """Bulk-deleting view for multiple PeerGroupTemplate."""

    queryset = models.PeerGroupTemplate.objects.all()
    filterset = filters.PeerGroupTemplateFilterSet
    table = tables.PeerGroupTemplateTable


class PeerEndpointListView(generic.ObjectListView):
    """List/table view of PeerEndpoint records."""

    queryset = models.PeerEndpoint.objects.all()
    table = tables.PeerEndpointTable
    filterset = filters.PeerEndpointFilterSet
    # filterset_form = forms.PeerEndpointFilterForm
    action_buttons = ("add")


class PeerEndpointView(generic.ObjectView):
    """Detail view of a single PeerEndpoint."""

    queryset = models.PeerEndpoint.objects.all()

    def get_extra_context(self, request, instance):
        """Return any additional context data for the template."""
        return {"object_fields": instance.get_fields(include_inherited=True)}


class PeerEndpointEditView(generic.ObjectEditView):
    """Create/edit view for a PeerEndpoint."""

    queryset = models.PeerEndpoint.objects.all()
    model_form = forms.PeerEndpointForm

    def alter_obj(self, obj, request, url_args, url_kwargs):
        """Inject peering object into form from url args."""
        if "peering" in url_kwargs:
            obj.peering = get_object_or_404(models.Peering, pk=url_kwargs["peering"])
        return obj

    def get_return_url(self, request, obj, *args, **kwargs):
        """Return to main Peering page after edit."""
        return obj.peering.get_absolute_url()


class PeerEndpointDeleteView(generic.ObjectDeleteView):
    """Delete view for a PeerEndpoint."""

    queryset = models.PeerEndpoint.objects.all()


class PeeringListView(generic.ObjectListView):
    """List/table view of Peering records."""

    queryset = models.Peering.objects.all()
    table = tables.PeeringTable
    filterset = filters.PeeringFilterSet
    filterset_form = forms.PeeringFilterForm
    action_buttons = ("add",)


class PeeringView(generic.ObjectView):
    """Detail view of a single Peering."""

    queryset = models.Peering.objects.all()


class PeeringEditView(generic.ObjectEditView):
    """Create/edit view for a Peering."""

    queryset = models.Peering.objects.all()
    model_form = forms.PeeringForm


class PeeringDeleteView(generic.ObjectDeleteView):
    """Delete view for a Peering."""

    queryset = models.Peering.objects.all()


class PeeringBulkDeleteView(generic.BulkDeleteView):
    """Bulk-deleting view for multiple Peering."""

    queryset = models.Peering.objects.all()
    filterset = filters.PeeringFilterSet
    table = tables.PeeringTable


class AddressFamilyListView(generic.ObjectListView):
    """List/table view of AddressFamily records."""

    queryset = models.AddressFamily.objects.all()
    table = tables.AddressFamilyTable
    filterset = filters.AddressFamilyFilterSet
    filterset_form = forms.AddressFamilyFilterForm
    action_buttons = ("add",)


class AddressFamilyView(generic.ObjectView):
    """Detail view of a single AddressFamily."""

    queryset = models.AddressFamily.objects.all()


class AddressFamilyEditView(generic.ObjectEditView):
    """Create/edit view for an AddressFamily."""

    queryset = models.AddressFamily.objects.all()
    model_form = forms.AddressFamilyForm


class AddressFamilyDeleteView(generic.ObjectDeleteView):
    """Delete view for an AddressFamily."""

    queryset = models.AddressFamily.objects.all()


class AddressFamilyBulkEditView(generic.BulkEditView):
    """Bulk-editing view for multiple AddressFamily."""

    queryset = models.AddressFamily.objects.all()
    filterset = filters.AddressFamilyFilterSet
    table = tables.AddressFamilyTable
    form = forms.AddressFamilyBulkEditForm


class AddressFamilyBulkDeleteView(generic.BulkDeleteView):
    """Bulk-deleting view for multiple AddressFamily."""

    queryset = models.AddressFamily.objects.all()
    filterset = filters.AddressFamilyFilterSet
    table = tables.AddressFamilyTable
