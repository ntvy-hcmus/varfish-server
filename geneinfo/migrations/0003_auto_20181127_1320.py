# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-27 13:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("geneinfo", "0002_auto_20181106_1022")]

    operations = [
        migrations.AddIndex(
            model_name="hgnc",
            index=models.Index(fields=["symbol"], name="geneinfo_hg_symbol_0a5edc_idx"),
        ),
        migrations.AddIndex(
            model_name="hgnc",
            index=models.Index(
                fields=["ensembl_gene_id", "entrez_id", "symbol"],
                name="geneinfo_hg_ensembl_d28f87_idx",
            ),
        ),
    ]
