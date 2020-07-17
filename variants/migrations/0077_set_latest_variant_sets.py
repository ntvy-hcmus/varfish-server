# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-07-27 15:58
from __future__ import unicode_literals

from django.db import migrations


def set_latest_variant_sets(apps, _schema_editor):
    ReferenceSite = apps.get_model("variants", "SmallVariantSet")
    for variant_set in ReferenceSite.objects.filter(state="active"):
        variant_set.case.latest_variant_set = variant_set
        variant_set.case.save()


def unset_latest_variant_sets(apps, _schema_editor):
    ReferenceSite = apps.get_model("variants", "Case")
    for case in ReferenceSite.objects.all():
        case.latest_variant_set = None
        case.save()


def set_latest_structural_variant_sets(apps, _schema_editor):
    ReferenceSite = apps.get_model("svs", "StructuralVariantSet")
    for variant_set in ReferenceSite.objects.filter(state="active"):
        variant_set.case.latest_structural_variant_set = variant_set
        variant_set.case.save()


def unset_latest_structural_variant_sets(apps, _schema_editor):
    ReferenceSite = apps.get_model("variants", "Case")
    for case in ReferenceSite.objects.all():
        case.latest_structural_variant_set = None
        case.save()


class Migration(migrations.Migration):

    dependencies = [
        ("variants", "0076_auto_20200727_1558"),
    ]

    operations = [
        migrations.RunPython(set_latest_variant_sets, unset_latest_variant_sets),
        migrations.RunPython(
            set_latest_structural_variant_sets, unset_latest_structural_variant_sets
        ),
    ]
