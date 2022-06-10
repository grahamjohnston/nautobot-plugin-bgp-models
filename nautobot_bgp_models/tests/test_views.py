# """Unit test automation for Model classes in nautobot_bgp_models."""
#
# from django.contrib.contenttypes.models import ContentType
#
# from nautobot.dcim.models import Device, DeviceRole, DeviceType, Interface, Manufacturer, Site
# from nautobot.extras.models import Status
# from nautobot.ipam.models import IPAddress, VRF
# from nautobot.utilities.testing import ViewTestCases
#
# from nautobot_bgp_models import models
# from nautobot_bgp_models.choices import AFISAFIChoices
#
#
# class AutonomousSystemTestCase(ViewTestCases.PrimaryObjectViewTestCase):
#     """Test views related to the AutonomousSystem model."""
#
#     model = models.AutonomousSystem
#
#     def _get_base_url(self):
#         return "plugins:{}:{}_{{}}".format(self.model._meta.app_label, self.model._meta.model_name)
#
#     @classmethod
#     def setUpTestData(cls):
#         """One-time class data setup."""
#         status_active = Status.objects.get(slug="active")
#         status_active.content_types.add(ContentType.objects.get_for_model(models.AutonomousSystem))
#
#         models.AutonomousSystem.objects.create(
#             asn=4200000000, status=status_active, description="Reserved for private use"
#         )
#         models.AutonomousSystem.objects.create(
#             asn=4200000001, status=status_active, description="Also reserved for private use"
#         )
#         models.AutonomousSystem.objects.create(
#             asn=4200000002, status=status_active, description="Another reserved for private use"
#         )
#
#         tags = cls.create_tags("Alpha", "Beta", "Gamma")
#
#         cls.form_data = {
#             "asn": 65551,
#             "description": "Hello, world!",
#             "status": status_active.pk,
#             "tags": [tag.pk for tag in tags],
#         }
#
#         cls.csv_data = (
#             "asn,status",
#             "4200000003,active",
#             "4200000004,active",
#             "4200000005,active",
#         )
#
#         cls.bulk_edit_data = {
#             "description": "New description",
#         }
#
#
# class PeeringRoleTestCase(ViewTestCases.OrganizationalObjectViewTestCase, ViewTestCases.BulkEditObjectsViewTestCase):
#     """Test views related to the PeeringRole model."""
#
#     model = models.PeeringRole
#
#     def _get_base_url(self):
#         return "plugins:{}:{}_{{}}".format(self.model._meta.app_label, self.model._meta.model_name)
#
#     @classmethod
#     def setUpTestData(cls):
#         """One-time class data setup."""
#         models.PeeringRole.objects.create(
#             name="Internal", slug="internal", color="0000ff", description="Internal peering"
#         )
#         models.PeeringRole.objects.create(name="Customer", slug="customer", color="ff0000")
#         models.PeeringRole.objects.create(name="Tenant", slug="tenant", color="00ff00")
#
#         cls.form_data = {
#             "name": "Temporary",
#             "slug": "temporary",
#             "color": "ffffff",
#             "description": "Temporary peering",
#         }
#
#         cls.csv_data = (
#             "name,slug,color",
#             "Role 1,role-1,111111",
#             "Role 2,role-2,222222",
#             "Role 3,role-3,333333",
#         )
#
#         cls.bulk_edit_data = {"color": "123456", "description": "Generic description"}
#
#
# class PeerGroupTestCase(
#     ViewTestCases.GetObjectViewTestCase,
#     ViewTestCases.GetObjectChangelogViewTestCase,
#     ViewTestCases.CreateObjectViewTestCase,
#     ViewTestCases.EditObjectViewTestCase,
#     ViewTestCases.DeleteObjectViewTestCase,
#     ViewTestCases.ListObjectsViewTestCase,
# ):
#     """Test views related to the PeerGroup model."""
#
#     model = models.PeerGroup
#
#     def _get_base_url(self):
#         return "plugins:{}:{}_{{}}".format(self.model._meta.app_label, self.model._meta.model_name)
#
#     @classmethod
#     def setUpTestData(cls):
#         """One-time class data setup."""
#
#         peeringrole = models.PeeringRole.objects.create(name="Internal", slug="internal", color="ffffff")
#
#         models.PeerGroup.objects.create(name="Group A", role=peeringrole)
#         models.PeerGroup.objects.create(name="Group B", role=peeringrole)
#         models.PeerGroup.objects.create(name="Group C", role=peeringrole)
#
#         cls.form_data = {
#             "name": "Group D",
#             "role": peeringrole.pk,
#             # TODO: other attributes
#         }
#
#
# class PeerEndpointTestCase(
#     ViewTestCases.GetObjectViewTestCase,
#     ViewTestCases.GetObjectChangelogViewTestCase,
#     # TODO Investigate how to enable tests that requires additional parameters (peering)
#     # ViewTestCases.CreateObjectViewTestCase,
#     # ViewTestCases.EditObjectViewTestCase,
#     ViewTestCases.DeleteObjectViewTestCase,
#     ViewTestCases.ListObjectsViewTestCase,
# ):
#     """Test views related to the PeerEndpoint model."""
#
#     model = models.PeerEndpoint
#     maxDiff = None
#
#     def _get_base_url(self):
#         return "plugins:{}:{}_{{}}".format(self.model._meta.app_label, self.model._meta.model_name)
#
#     @classmethod
#     def setUpTestData(cls):  # pylint: disable=too-many-locals
#         """One-time class data setup."""
#         status_active = Status.objects.get(slug="active")
#
#         manufacturer = Manufacturer.objects.create(name="Cisco", slug="cisco")
#         devicetype = DeviceType.objects.create(manufacturer=manufacturer, model="CSR 1000V", slug="csr1000v")
#         site = Site.objects.create(name="Site 1", slug="site-1")
#         devicerole = DeviceRole.objects.create(name="Router", slug="router", color="ff0000")
#         device = Device.objects.create(
#             device_type=devicetype,
#             device_role=devicerole,
#             name="Device 1",
#             site=site,
#             status=status_active,
#         )
#         interface = Interface.objects.create(name="Loopback1", device=device)
#         interface_2 = Interface.objects.create(name="Loopback2", device=device)
#         vrf = VRF.objects.create(name="red")
#
#         address_1 = IPAddress.objects.create(
#             address="1.1.1.1/32", status=status_active, vrf=vrf, assigned_object=interface
#         )
#         address_3 = IPAddress.objects.create(address="3.3.3.3/32", status=status_active, vrf=vrf)
#         address_2 = IPAddress.objects.create(address="2.2.2.2/32", status=status_active, vrf=vrf)
#         address_4 = IPAddress.objects.create(
#             address="4.4.4.4/32", status=status_active, vrf=vrf, assigned_object=interface_2
#         )
#
#         peeringrole = models.PeeringRole.objects.create(name="Internal", slug="internal", color="ffffff")
#
#         peergroup = models.PeerGroup.objects.create(name="Group A", role=peeringrole, vrf=vrf)
#
#         peering1 = models.Peering.objects.create(
#             role=peeringrole,
#             status=status_active,
#         )
#         peering2 = models.Peering.objects.create(
#             role=peeringrole,
#             status=status_active,
#         )
#         peering3 = models.Peering.objects.create(
#             role=peeringrole,
#             status=status_active,
#         )
#
#         models.PeerEndpoint.objects.create(
#             local_ip=address_1,
#             peer_group=peergroup,
#             vrf=vrf,
#             source_interface=interface,
#             router_id=address_1,
#             peering=peering1,
#         )
#         models.PeerEndpoint.objects.create(local_ip=address_2, vrf=vrf, peering=peering2)
#         models.PeerEndpoint.objects.create(local_ip=address_3, vrf=vrf, peering=peering3)
#         cls.form_data = {
#             "local_ip": address_4.pk,
#             "peer_group": peergroup.pk,
#             "vrf": vrf.pk,
#             "source_interface_interface": interface_2.pk,
#             "router_id": address_4.pk,
#             "maximum_paths_ibgp": 4,
#             "maximum_paths_ebgp": 8,
#             "maximum_paths_eibgp": 2,
#             "maximum_prefix": 100,
#             "multipath": True,
#             "bfd_multiplier": 3,
#             "bfd_minimum_interval": 100,
#             "bfd_fast_detection": False,
#             "import_policy": "SOMEPOLICY",
#             "export_policy": "",
#             "enforce_first_as": None,
#             "send_community": False,
#             "peering": peering2.pk,
#         }
#
#
# class PeeringTestCase(
#     ViewTestCases.GetObjectViewTestCase,
#     ViewTestCases.GetObjectChangelogViewTestCase,
#     ViewTestCases.CreateObjectViewTestCase,
#     ViewTestCases.EditObjectViewTestCase,
#     ViewTestCases.DeleteObjectViewTestCase,
#     ViewTestCases.ListObjectsViewTestCase,
# ):
#     """Test views related to the Peering model."""
#
#     model = models.Peering
#     maxDiff = None
#
#     def _get_base_url(self):
#         return "plugins:{}:{}_{{}}".format(self.model._meta.app_label, self.model._meta.model_name)
#
#     @classmethod
#     def setUpTestData(cls):
#         """One-time class data setup."""
#         status_active = Status.objects.get(slug="active")
#         status_active.content_types.add(ContentType.objects.get_for_model(models.Peering))
#
#         peeringrole_internal = models.PeeringRole.objects.create(name="Internal", slug="internal", color="000000")
#         peeringrole_customer = models.PeeringRole.objects.create(name="Customer", slug="customer", color="ffffff")
#
#         models.Peering.objects.create(status=status_active, role=peeringrole_internal)
#         models.Peering.objects.create(status=status_active, role=peeringrole_internal)
#         models.Peering.objects.create(status=status_active, role=peeringrole_internal)
#
#         cls.form_data = {
#             "status": status_active.pk,
#             "role": peeringrole_customer.pk,
#             "authentication_key": "thisisatest",
#         }
#
#
# class AddressFamilyTestCase(
#     ViewTestCases.GetObjectViewTestCase,
#     ViewTestCases.GetObjectChangelogViewTestCase,
#     ViewTestCases.CreateObjectViewTestCase,
#     ViewTestCases.EditObjectViewTestCase,
#     ViewTestCases.DeleteObjectViewTestCase,
#     ViewTestCases.ListObjectsViewTestCase,
# ):
#     """Test views related to the AddressFamily model."""
#
#     model = models.AddressFamily
#     maxDiff = None
#
#     def _get_base_url(self):
#         return "plugins:{}:{}_{{}}".format(self.model._meta.app_label, self.model._meta.model_name)
#
#     @classmethod
#     def setUpTestData(cls):
#         """One-time class data setup."""
#         status_active = Status.objects.get(slug="active")
#
#         manufacturer = Manufacturer.objects.create(name="Cisco", slug="cisco")
#         devicetype = DeviceType.objects.create(manufacturer=manufacturer, model="CSR 1000V", slug="csr1000v")
#         site = Site.objects.create(name="Site 1", slug="site-1")
#         devicerole = DeviceRole.objects.create(name="Router", slug="router", color="ff0000")
#         device = Device.objects.create(
#             device_type=devicetype,
#             device_role=devicerole,
#             name="Device 1",
#             site=site,
#             status=status_active,
#         )
#         interface = Interface.objects.create(name="Loopback1", device=device)
#
#         address = IPAddress.objects.create(address="1.1.1.1/32", status=status_active, assigned_object=interface)
#
#         peeringrole = models.PeeringRole.objects.create(name="Internal", slug="internal", color="ffffff")
#
#         peergroup = models.PeerGroup.objects.create(name="Group A", role=peeringrole)
#         peering = models.Peering.objects.create(status=status_active, role=peeringrole)
#
#         peerendpoint = models.PeerEndpoint.objects.create(
#             local_ip=address,
#             peer_group=peergroup,
#             source_interface=interface,
#             router_id=address,
#             peering=peering,
#         )
#
#         models.AddressFamily.objects.create(afi_safi=AFISAFIChoices.AFI_IPV4)
#         models.AddressFamily.objects.create(peer_group=peergroup, afi_safi=AFISAFIChoices.AFI_IPV4)
#         models.AddressFamily.objects.create(peer_endpoint=peerendpoint, afi_safi=AFISAFIChoices.AFI_IPV4)
#
#         cls.form_data = {
#             "afi_safi": AFISAFIChoices.AFI_VPNV4,
#             "peer_group": None,
#             "peer_endpoint": peerendpoint.pk,
#             "import_policy": "IMPORT",
#             "export_policy": "EXPORT",
#             "redistribute_static_policy": "REDISTRIBUTE_STATIC",
#         }
