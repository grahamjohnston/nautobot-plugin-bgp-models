"""Forms and FilterForms for nautobot_bgp_models."""
from django import forms

import nautobot.utilities.forms as utilities_forms
from nautobot.apps.forms import (
    CSVModelChoiceField,
    CSVModelForm,
    DynamicModelMultipleChoiceField,
    DynamicModelChoiceField,
    NautobotModelForm,
    NautobotBulkEditForm,
    StatusModelCSVFormMixin,
    TagFilterField,
    TagsBulkEditFormMixin,
)
from nautobot.circuits.models import Provider
from nautobot.dcim.models import Device, Interface
from nautobot.extras.forms import NautobotFilterForm
from nautobot.extras.models import Tag, Secret
from nautobot.ipam.models import VRF, IPAddress

from . import choices, models


class AutonomousSystemForm(NautobotModelForm):
    """Form for creating/updating AutonomousSystem records."""

    tags = DynamicModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)
    provider = DynamicModelChoiceField(queryset=Provider.objects.all(), required=False)

    class Meta:
        model = models.AutonomousSystem
        fields = ("asn", "description", "provider", "status", "tags")


class AutonomousSystemFilterForm(NautobotFilterForm):
    """Form for filtering AutonomousSystem records in combination with AutonomousSystemFilterSet."""

    model = models.AutonomousSystem
    field_order = ["status", "tag"]
    tag = TagFilterField(model)


class AutonomousSystemCSVForm(StatusModelCSVFormMixin, CSVModelForm):
    """Form for importing AutonomousSystems from CSV data."""

    provider = CSVModelChoiceField(
        queryset=Provider.objects.all(),
        to_field_name="name",
        help_text="Provider name",
        required=False,
    )

    class Meta:
        model = models.AutonomousSystem
        fields = models.AutonomousSystem.csv_headers


class AutonomousSystemBulkEditForm(TagsBulkEditFormMixin, NautobotBulkEditForm):
    """Form for bulk-editing multiple AutonomousSystem records."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.AutonomousSystem.objects.all(), widget=forms.MultipleHiddenInput()
    )
    description = forms.CharField(max_length=200, required=False)

    class Meta:
        nullable_fields = [
            "description",
        ]


class BGPRoutingInstanceForm(NautobotModelForm):
    """Form for creating/updating BGPRoutingInstance records."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)

        if self.initial.get("device"):
            self.fields["device"].disabled = True
            self.fields.pop("template")

    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
    )

    autonomous_system = DynamicModelChoiceField(
        queryset=models.AutonomousSystem.objects.all(),
    )

    router_id = DynamicModelChoiceField(
        queryset=IPAddress.objects.all(),
        label="Router ID",
        required=False,
        query_params={"device_id": "$device"},
    )

    tags = DynamicModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)

    template = DynamicModelMultipleChoiceField(
        queryset=models.PeerGroupTemplate.objects.all(),
        required=False,
        label="Peer Group Templates",
        help_text="Automatically create references to the global peer group templates",
        display_field="name",
    )

    def save(self, commit=True):
        """Save."""
        obj = super().save(commit)

        if commit:
            # Initiate local templates as indicated in the creation form.
            # Templates are only created during object creation.
            for t in self.cleaned_data.get("template", []):  # pylint: disable=invalid-name
                models.PeerGroup.objects.create(
                    name=t.name,
                    template=t,
                    routing_instance=obj,
                )

        return obj

    class Meta:
        model = models.BGPRoutingInstance
        fields = ("device", "autonomous_system", "description", "router_id", "template", "tags", "extra_attributes")


class BGPRoutingInstanceFilterForm(NautobotFilterForm):
    """Form for filtering BGPRoutingInstance records in combination with BGPRoutingInstanceFilterSet."""

    q = forms.CharField(required=False, label="Search")

    model = models.BGPRoutingInstance

    device = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        to_field_name="name",
    )

    autonomous_system = DynamicModelMultipleChoiceField(
        queryset=models.AutonomousSystem.objects.all(),
        required=False,
        to_field_name="asn",
    )

    tag = TagFilterField(model)

    field_order = [
        "q",
        "device",
        "router_id",
        "autonomous_system",
        "tag",
    ]


class BGPRoutingInstanceBulkEditForm(NautobotBulkEditForm):
    """Form for bulk-editing multiple BGPRoutingInstance records."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.BGPRoutingInstance.objects.all(), widget=forms.MultipleHiddenInput()
    )
    description = forms.CharField(max_length=200, required=False)

    class Meta:
        nullable_fields = [
            "description",
        ]


class BGPRoutingInstanceCSVForm(StatusModelCSVFormMixin, CSVModelForm):
    """Form for importing BGPRoutingInstance from CSV data."""

    device = CSVModelChoiceField(
        queryset=Device.objects.all(),
        to_field_name="name",
        help_text="Assigned device's name",
    )

    autonomous_system = CSVModelChoiceField(
        queryset=models.AutonomousSystem.objects.all(),
        to_field_name="asn",
        help_text="Assigned autonomous system number",
    )

    router_id = CSVModelChoiceField(
        queryset=IPAddress.objects.all(),
        to_field_name="address",
        help_text="Router ID - IP Address",
        required=False,
    )

    class Meta:
        model = models.BGPRoutingInstance
        fields = models.BGPRoutingInstance.csv_headers


class PeeringRoleForm(NautobotModelForm):
    """Form for creating/updating PeeringRole records."""

    slug = utilities_forms.SlugField()

    class Meta:
        model = models.PeeringRole
        fields = ("name", "slug", "color", "description")


class PeeringRoleFilterForm(NautobotFilterForm):
    """Form for filtering PeeringRole records in combination with PeeringRoleFilterSet."""

    model = models.PeeringRole
    q = forms.CharField(required=False, label="Search")
    color = forms.CharField(max_length=6, required=False, widget=utilities_forms.ColorSelect())


class PeeringRoleCSVForm(CSVModelForm):
    """Form for importing PeeringRole records from CSV data."""

    class Meta:
        model = models.PeeringRole
        fields = models.PeeringRole.csv_headers


class PeeringRoleBulkEditForm(NautobotBulkEditForm):
    """Form for bulk-editing multiple PeeringRole records."""

    pk = forms.ModelMultipleChoiceField(queryset=models.PeeringRole.objects.all(), widget=forms.MultipleHiddenInput())
    color = forms.CharField(max_length=6, required=False, widget=utilities_forms.ColorSelect())
    description = forms.CharField(max_length=200, required=False)

    class Meta:
        nullable_fields = [
            "description",
        ]


class PeerGroupForm(NautobotModelForm):
    """Form for creating/updating PeerGroup records."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)

        if self.initial.get("routing_instance"):
            self.fields["routing_instance"].disabled = True

    routing_instance = DynamicModelChoiceField(
        queryset=models.BGPRoutingInstance.objects.all(),
        required=True,
        label="BGP Routing Instance",
        help_text="Specify related Routing Instance (Device)",
    )

    source_ip = DynamicModelChoiceField(
        queryset=IPAddress.objects.all(),
        required=False,
        label="Source IP Address",
        query_params={"nautobot_bgp_models_ips_bgp_routing_instance": "$routing_instance"},
    )

    source_interface = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
        required=False,
        label="Source Interface",
        query_params={"nautobot_bgp_models_interfaces_bgp_routing_instance": "$routing_instance"},
    )

    autonomous_system = DynamicModelChoiceField(
        queryset=models.AutonomousSystem.objects.all(),
        required=False,
        label="Autonomous System",
    )

    role = DynamicModelChoiceField(queryset=models.PeeringRole.objects.all(), required=False)

    peergroup_template = DynamicModelChoiceField(queryset=models.PeerGroupTemplate.objects.all(), required=False)

    secret = DynamicModelChoiceField(queryset=Secret.objects.all(), required=False)

    class Meta:
        model = models.PeerGroup
        fields = (
            "routing_instance",
            "name",
            "peergroup_template",
            "description",
            "enabled",
            "role",
            "source_ip",
            "source_interface",
            "autonomous_system",
            "import_policy",
            "export_policy",
            "secret",
            "extra_attributes",
        )


class PeerGroupBulkEditForm(NautobotBulkEditForm):
    """Form for bulk-editing multiple PeerGroup records."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.PeerGroupTemplate.objects.all(), widget=forms.MultipleHiddenInput()
    )
    description = forms.CharField(max_length=200, required=False)

    class Meta:
        nullable_fields = [
            "description",
        ]


class PeerGroupTemplateForm(NautobotModelForm):
    """Form for creating/updating PeerGroup records."""

    autonomous_system = DynamicModelChoiceField(
        queryset=models.AutonomousSystem.objects.all(),
        required=False,
        label="Autonomous System",
    )

    role = DynamicModelChoiceField(queryset=models.PeeringRole.objects.all(), required=False)

    secret = DynamicModelChoiceField(queryset=Secret.objects.all(), required=False)

    class Meta:
        model = models.PeerGroupTemplate
        fields = (
            "name",
            "description",
            "enabled",
            "role",
            "autonomous_system",
            "import_policy",
            "export_policy",
            "extra_attributes",
        )


class PeerGroupTemplateBulkEditForm(NautobotBulkEditForm):
    """Form for bulk-editing multiple PeerGroupTemplate records."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.PeerGroupTemplate.objects.all(), widget=forms.MultipleHiddenInput()
    )
    description = forms.CharField(max_length=200, required=False)

    class Meta:
        nullable_fields = [
            "description",
        ]


class PeerGroupFilterForm(NautobotFilterForm):
    """Form for filtering PeerGroup records in combination with PeerGroupFilterSet."""

    model = models.PeerGroup

    q = forms.CharField(required=False, label="Search")

    role = DynamicModelMultipleChoiceField(
        queryset=models.PeeringRole.objects.all(), to_field_name="slug", required=False
    )

    enabled = forms.NullBooleanField(
        required=False, widget=utilities_forms.StaticSelect2(choices=utilities_forms.BOOLEAN_WITH_BLANK_CHOICES)
    )

    autonomous_system = DynamicModelMultipleChoiceField(
        queryset=models.AutonomousSystem.objects.all(), to_field_name="asn", required=False
    )


class PeerGroupTemplateFilterForm(NautobotFilterForm):
    """Form for filtering PeerGroupTemplate records in combination with PeerGroupTemplateFilterSet."""

    model = models.PeerGroup

    q = forms.CharField(required=False, label="Search")

    role = DynamicModelMultipleChoiceField(
        queryset=models.PeeringRole.objects.all(), to_field_name="slug", required=False
    )

    enabled = forms.NullBooleanField(
        required=False, widget=utilities_forms.StaticSelect2(choices=utilities_forms.BOOLEAN_WITH_BLANK_CHOICES)
    )

    autonomous_system = DynamicModelMultipleChoiceField(
        queryset=models.AutonomousSystem.objects.all(), to_field_name="asn", required=False
    )


class PeerGroupTemplateCSVForm(CSVModelForm):
    """Form for importing PeerGroupTemplate from CSV data."""

    role = CSVModelChoiceField(
        queryset=models.PeeringRole.objects.all(),
        to_field_name="name",
        help_text="Assigned Peering Role name",
        required=False,
    )

    autonomous_system = CSVModelChoiceField(
        queryset=models.AutonomousSystem.objects.all(),
        to_field_name="asn",
        help_text="Assigned autonomous system number",
        required=False,
    )

    class Meta:
        model = models.PeerGroupTemplate
        fields = models.PeerGroupTemplate.csv_headers


class PeerGroupCSVForm(CSVModelForm):
    """Form for importing PeerGroup from CSV data."""

    device = CSVModelChoiceField(
        queryset=Device.objects.all(),
        required=True,
        to_field_name="name",
        help_text="Parent device of assigned interface (if any)",
    )

    # routing_instance = CSVModelChoiceField(
    #     queryset=models.BGPRoutingInstance.objects.all(),
    #     # to_field_name="name",
    #     help_text="Assigned routing instance",
    #     required=False,
    # )

    peergroup_template = CSVModelChoiceField(
        queryset=models.PeerGroupTemplate.objects.all(),
        to_field_name="name",
        help_text="Assigned peering group template name",
        required=False,
    )

    autonomous_system = CSVModelChoiceField(
        queryset=models.AutonomousSystem.objects.all(),
        to_field_name="asn",
        help_text="Assigned autonomous system number",
        required=False,
    )

    role = CSVModelChoiceField(
        queryset=models.PeeringRole.objects.all(),
        to_field_name="name",
        help_text="Assigned Peering Role name",
        required=False,
    )

    source_interface = CSVModelChoiceField(
        queryset=Interface.objects.all(),
        to_field_name="name",
        help_text="Peer group source Interface name",
        required=False,
    )

    source_ip = CSVModelChoiceField(
        queryset=IPAddress.objects.all(),
        to_field_name="name",
        help_text="Peer group source IP address",
        required=False,
    )

    def __init__(self, data=None, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        if data:
            # Limit rack_group queryset by assigned site
            params = {f"device__{self.fields['device'].to_field_name}": data.get("device")}
            self.fields["routing_instance"].queryset = self.fields["routing_instance"].queryset.filter(**params)

    # TODO(mzb): @Glenn How do we approach `to_field_name' on the BGPRoutingInstance model ?

    class Meta:
        model = models.PeerGroup
        fields = models.PeerGroup.csv_headers


class PeerEndpointForm(NautobotModelForm):
    """Form for creating/updating PeerEndpoint records."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)

        if self.initial.get("routing_instance"):
            self.fields["routing_instance"].disabled = True

        _prefix = f"{self.prefix}-" if self.prefix else ""
        self.fields["source_ip"].widget.add_query_param(
            "nautobot_bgp_models_ips_bgp_routing_instance", f"${_prefix}routing_instance"
        )
        self.fields["source_interface"].widget.add_query_param(
            "nautobot_bgp_models_interfaces_bgp_routing_instance", f"${_prefix}routing_instance"
        )
        self.fields["peer_group"].widget.add_query_param("routing_instance", f"${_prefix}routing_instance")

    routing_instance = DynamicModelChoiceField(
        queryset=models.BGPRoutingInstance.objects.all(),
        required=False,
        label="BGP Routing Instance",
        help_text="Specify related Routing Instance (Device)",
    )

    autonomous_system = DynamicModelChoiceField(
        queryset=models.AutonomousSystem.objects.all(),
        required=False,
        label="Autonomous System",
    )

    source_ip = DynamicModelChoiceField(
        queryset=IPAddress.objects.all(),
        required=False,
        label="Source IP Address",
    )

    source_interface = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
        required=False,
        label="Source Interface",
    )

    peer_group = DynamicModelChoiceField(
        queryset=models.PeerGroup.objects.all(),
        required=False,
        label="Peer Group",
    )

    role = DynamicModelChoiceField(queryset=models.PeeringRole.objects.all(), required=False)

    secret = DynamicModelChoiceField(queryset=Secret.objects.all(), required=False)

    peering = DynamicModelChoiceField(  # Hidden & optional - update peers manually for new peerings.
        queryset=models.Peering.objects.all(),
        widget=forms.HiddenInput(),
        required=False,
    )

    class Meta:
        model = models.PeerEndpoint
        fields = (
            "peering",
            "routing_instance",
            "description",
            "enabled",
            "role",
            "source_ip",
            "source_interface",
            "autonomous_system",
            "peer_group",
            "import_policy",
            "export_policy",
            "secret",
            "extra_attributes",
        )

    def save(self, commit=True):
        """Save model changes on successful form submission."""
        endpoint = super().save(commit=commit)

        if commit:
            endpoint.peering.update_peers()

        return endpoint



class PeerEndpointCSVForm(CSVModelForm):
    """Form for importing PeerEndpoint from CSV data."""

    class Meta:
        model = models.PeerEndpoint
        fields = models.PeerEndpoint.csv_headers


class PeerEndpointFilterForm(NautobotFilterForm):
    """Form for filtering PeerEndpoint records in combination with PeerEndpointFilterSet."""

    model = models.PeerEndpoint
    tag = TagFilterField(model)


class PeerEndpointBulkEditForm(NautobotBulkEditForm):
    """Form for bulk-editing multiple PeerEndpoint records."""

    pk = forms.ModelMultipleChoiceField(queryset=models.PeerEndpoint.objects.all(), widget=forms.MultipleHiddenInput())

    class Meta:
        nullable_fields = []


class PeeringForm(NautobotModelForm):
    """Form for creating/updating Peering records."""

    class Meta:
        model = models.Peering
        fields = ("status",)


class PeeringFilterForm(NautobotFilterForm):
    """Form for filtering Peering records in combination with PeeringFilterSet."""

    model = models.Peering
    field_order = [
        "q",
        "role",
        "status",
        "device",
    ]
    role = DynamicModelMultipleChoiceField(
        queryset=models.PeeringRole.objects.all(), to_field_name="slug", required=False
    )

    device = DynamicModelMultipleChoiceField(queryset=Device.objects.all(), to_field_name="name", required=False)


class AddressFamilyForm(NautobotModelForm):
    """Form for creating/updating AddressFamily records."""

    routing_instance = DynamicModelChoiceField(
        queryset=models.BGPRoutingInstance.objects.all(),
        required=True,
        label="BGP Routing Instance",
        help_text="Specify related Routing Instance (Device)",
    )

    afi_safi = forms.ChoiceField(
        label="AFI-SAFI",
        choices=choices.AFISAFIChoices,
        required=False,
        widget=utilities_forms.StaticSelect2(),
    )

    vrf = DynamicModelChoiceField(
        queryset=VRF.objects.all(),
        required=False,
        label="VRF",
    )

    multipath = forms.NullBooleanField(required=False, widget=utilities_forms.BulkEditNullBooleanSelect())

    class Meta:
        model = models.AddressFamily
        fields = (
            "routing_instance",
            "afi_safi",
            "vrf",
            "import_policy",
            "export_policy",
            "multipath",
        )


class AddressFamilyBulkEditForm(NautobotBulkEditForm):
    """Form for bulk-editing multiple AddressFamily records."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.AutonomousSystem.objects.all(), widget=forms.MultipleHiddenInput()
    )

    class Meta:
        nullable_fields = []


class AddressFamilyFilterForm(NautobotFilterForm):
    """Form for filtering AddressFamily records in combination with AddressFamilyFilterSet."""

    model = models.AddressFamily

    routing_instance = DynamicModelMultipleChoiceField(queryset=models.BGPRoutingInstance.objects.all(), required=False)

    afi_safi = forms.MultipleChoiceField(
        label="AFI-SAFI",
        choices=choices.AFISAFIChoices,
        required=False,
        widget=utilities_forms.StaticSelect2Multiple(),
    )

    vrf = DynamicModelMultipleChoiceField(queryset=VRF.objects.all(), required=False)


class AddressFamilyCSVForm(CSVModelForm):
    """Form for importing AddressFamily from CSV data."""

    class Meta:
        model = models.AddressFamily
        fields = models.AddressFamily.csv_headers
