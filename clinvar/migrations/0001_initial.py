# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-19 10:45
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Clinvar",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("release", models.CharField(max_length=32)),
                ("chromosome", models.CharField(max_length=32)),
                ("position", models.IntegerField()),
                ("reference", models.CharField(max_length=512)),
                ("alternative", models.CharField(max_length=512)),
                ("start", models.IntegerField()),
                ("stop", models.IntegerField()),
                ("strand", models.CharField(max_length=1, null=True)),
                ("variation_type", models.CharField(max_length=16, null=True)),
                ("variation_id", models.IntegerField(null=True)),
                ("rcv", models.CharField(max_length=16, null=True)),
                (
                    "scv",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=16, null=True), size=None
                    ),
                ),
                ("allele_id", models.IntegerField(null=True)),
                ("symbol", models.CharField(max_length=16, null=True)),
                ("hgvs_c", models.CharField(max_length=512, null=True)),
                ("hgvs_p", models.CharField(max_length=512, null=True)),
                ("molecular_consequence", models.CharField(max_length=1024, null=True)),
                ("clinical_significance", models.CharField(max_length=64)),
                (
                    "clinical_significance_ordered",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=512), size=None
                    ),
                ),
                ("pathogenic", models.IntegerField()),
                ("likely_pathogenic", models.IntegerField()),
                ("uncertain_significance", models.IntegerField()),
                ("likely_benign", models.IntegerField()),
                ("benign", models.IntegerField()),
                ("review_status", models.CharField(max_length=64, null=True)),
                (
                    "review_status_ordered",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=64, null=True), size=None
                    ),
                ),
                ("last_evaluated", models.DateField(null=True)),
                (
                    "all_submitters",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=512, null=True), size=None
                    ),
                ),
                (
                    "submitters_ordered",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=512, null=True), size=None
                    ),
                ),
                (
                    "all_traits",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=512), size=None
                    ),
                ),
                (
                    "all_pmids",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.IntegerField(null=True), size=None
                    ),
                ),
                ("inheritance_modes", models.CharField(max_length=32, null=True)),
                ("age_of_onset", models.CharField(max_length=32, null=True)),
                ("prevalence", models.CharField(max_length=32, null=True)),
                ("disease_mechanism", models.CharField(max_length=32, null=True)),
                (
                    "origin",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=16, null=True), size=None
                    ),
                ),
                (
                    "xrefs",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=16, null=True), size=None
                    ),
                ),
                (
                    "dates_ordered",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.DateField(null=True), size=None
                    ),
                ),
                ("multi", models.IntegerField()),
            ],
        ),
        migrations.AddIndex(
            model_name="clinvar",
            index=models.Index(
                fields=["release", "chromosome", "position", "reference", "alternative"],
                name="clinvar_cli_release_457ca8_idx",
            ),
        ),
    ]
