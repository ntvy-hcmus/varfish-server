# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-26 19:30
from __future__ import unicode_literals

import bgjobs.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("projectroles", "0006_add_remote_projects"),
        ("bgjobs", "0004_backgroundjob_user"),
        ("variants", "0019_rebuild_var_stats"),
    ]

    operations = [
        migrations.CreateModel(
            name="ComputeProjectVariantsStatsBgJob",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "sodar_uuid",
                    models.UUIDField(
                        default=uuid.uuid4, help_text="Job Specialization SODAR UUID", unique=True
                    ),
                ),
                (
                    "bg_job",
                    models.ForeignKey(
                        help_text="Background job for state etc.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="compute_project_variants_stats",
                        to="bgjobs.BackgroundJob",
                    ),
                ),
            ],
            bases=(bgjobs.models.JobModelMessageMixin, models.Model),
        ),
        migrations.CreateModel(
            name="ProjectRelatedness",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("sample1", models.CharField(max_length=200)),
                ("sample2", models.CharField(max_length=200)),
                ("het_1_2", models.IntegerField()),
                ("het_1", models.IntegerField()),
                ("het_2", models.IntegerField()),
                ("n_ibs0", models.IntegerField()),
                ("n_ibs1", models.IntegerField()),
                ("n_ibs2", models.IntegerField()),
            ],
            options={"ordering": ("sample1", "sample2"), "abstract": False},
        ),
        migrations.CreateModel(
            name="ProjectVariantStats",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                )
            ],
        ),
        migrations.CreateModel(
            name="CaseAwareProject",
            fields=[],
            options={"proxy": True, "indexes": []},
            bases=("projectroles.project",),
        ),
        migrations.AlterField(
            model_name="pedigreerelatedness",
            name="stats",
            field=models.ForeignKey(
                help_text="Pedigree relatedness information",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="relatedness",
                to="variants.CaseVariantStats",
            ),
        ),
        migrations.AddField(
            model_name="projectvariantstats",
            name="project",
            field=models.OneToOneField(
                help_text="The variant statistics object for this projects",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="variant_stats",
                to="projectroles.Project",
            ),
        ),
        migrations.AddField(
            model_name="projectrelatedness",
            name="stats",
            field=models.ForeignKey(
                help_text="Pedigree relatedness information",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="relatedness",
                to="variants.ProjectVariantStats",
            ),
        ),
        migrations.AddField(
            model_name="computeprojectvariantsstatsbgjob",
            name="project",
            field=models.ForeignKey(
                help_text="Project in which this objects belongs",
                on_delete=django.db.models.deletion.CASCADE,
                to="projectroles.Project",
            ),
        ),
    ]
