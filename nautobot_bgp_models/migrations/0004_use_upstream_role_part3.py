# Generated by Django 3.2.17 on 2023-02-12 20:25

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("nautobot_bgp_models", "0003_use_upstream_role_part2"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="peerendpoint",
            name="role",
        ),
        migrations.RemoveField(
            model_name="peergroup",
            name="role",
        ),
        migrations.RemoveField(
            model_name="peergrouptemplate",
            name="role",
        ),
        migrations.DeleteModel(
            name="PeeringRole",
        ),
    ]