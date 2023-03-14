# Generated by Django 3.2.16 on 2023-05-25 08:42

from django.db import migrations
import django.db.models.deletion
import nautobot.extras.models.statuses


class Migration(migrations.Migration):
    dependencies = [
        ("extras", "0053_relationship_required_on"),
        ("nautobot_bgp_models", "0002_rename_template_peergroup_peergroup_template"),
    ]

    operations = [
        migrations.AddField(
            model_name="bgproutinginstance",
            name="status",
            field=nautobot.extras.models.statuses.StatusField(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="nautobot_bgp_models_bgproutinginstance_related",
                to="extras.status",
            ),
        ),
    ]
