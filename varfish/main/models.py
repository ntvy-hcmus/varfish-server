import uuid as uuid_object

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
from projectroles.models import Project
from postgres_copy import CopyManager


class SmallVariant(models.Model):
    release = models.CharField(max_length=32)
    chromosome = models.CharField(max_length=32)
    position = models.IntegerField()
    reference = models.CharField(max_length=512)
    alternative = models.CharField(max_length=512)
    var_type = models.CharField(max_length=8)
    case_id = models.IntegerField()
    genotype = JSONField()
    in_clinvar = models.NullBooleanField()
    exac_frequency = models.FloatField(null=True)
    exac_homozygous = models.IntegerField(null=True)
    exac_heterozygous = models.IntegerField(null=True)
    exac_hemizygous = models.IntegerField(null=True)
    thousand_genomes_frequency = models.FloatField(null=True)
    thousand_genomes_homozygous = models.IntegerField(null=True)
    thousand_genomes_heterozygous = models.IntegerField(null=True)
    thousand_genomes_hemizygous = models.IntegerField(null=True)
    gnomad_exomes_frequency = models.FloatField(null=True)
    gnomad_exomes_homozygous = models.IntegerField(null=True)
    gnomad_exomes_heterozygous = models.IntegerField(null=True)
    gnomad_exomes_hemizygous = models.IntegerField(null=True)
    gnomad_genomes_frequency = models.FloatField(null=True)
    gnomad_genomes_homozygous = models.IntegerField(null=True)
    gnomad_genomes_heterozygous = models.IntegerField(null=True)
    gnomad_genomes_hemizygous = models.IntegerField(null=True)
    refseq_gene_id = models.CharField(max_length=16, null=True)
    refseq_transcript_id = models.CharField(max_length=16, null=True)
    refseq_transcript_coding = models.NullBooleanField()
    refseq_hgvs_c = models.CharField(max_length=512, null=True)
    refseq_hgvs_p = models.CharField(max_length=512, null=True)
    refseq_effect = ArrayField(models.CharField(max_length=64), null=True)
    ensembl_gene_id = models.CharField(max_length=16, null=True)
    ensembl_transcript_id = models.CharField(max_length=16, null=True)
    ensembl_transcript_coding = models.NullBooleanField()
    ensembl_hgvs_c = models.CharField(max_length=512, null=True)
    ensembl_hgvs_p = models.CharField(max_length=512, null=True)
    ensembl_effect = ArrayField(models.CharField(max_length=64, null=True))
    #    before_change = models.IntegerField(null=True)
    #    after_change = models.IntegerField(null=True)
    #    inserted_bases = models.CharField(max_length=512, null=True)
    # project = models.ForeignKey(
    #     Project,
    #     help_text='Project in which this objects belongs',
    # )
    # sodar_uuid = models.UUIDField(
    #     default=uuid_object.uuid4,
    #     unique=True,
    #     help_text='SmallVariant SODAR UUID',
    # )
    objects = CopyManager()

    class Meta:
        unique_together = (
            "release",
            "chromosome",
            "position",
            "reference",
            "alternative",
            "case_id",
            "ensembl_gene_id",
            "refseq_gene_id",
        )
        indexes = [
            # index for base query
            models.Index(
                fields=[
                    "exac_frequency",
                    "gnomad_exomes_frequency",
                    "gnomad_genomes_frequency",
                    "thousand_genomes_frequency",
                    "exac_homozygous",
                    "gnomad_exomes_homozygous",
                    "gnomad_genomes_homozygous",
                    "thousand_genomes_homozygous",
                    "refseq_effect"
                ]
            ),
            models.Index(
                fields=[
                    "exac_frequency",
                    "gnomad_exomes_frequency",
                    "gnomad_genomes_frequency",
                    "thousand_genomes_frequency",
                    "exac_homozygous",
                    "gnomad_exomes_homozygous",
                    "gnomad_genomes_homozygous",
                    "thousand_genomes_homozygous",
                    "ensembl_effect",
                ]
            ),
            # for join with clinvar, dbsnp
            models.Index(
                fields=[
                    "release",
                    "chromosome",
                    "position",
                    "reference",
                    "alternative",
                ],
            ),
            # for join with annotation
            models.Index(
                fields=[
                    "release",
                    "chromosome",
                    "position",
                    "reference",
                    "alternative",
                    "ensembl_gene_id",
                ],
            ),
            models.Index(
                fields=[
                    "release",
                    "chromosome",
                    "position",
                    "reference",
                    "alternative",
                    "refseq_gene_id",
                ],
            ),
            # for join with hgnc
            models.Index(
                fields=["ensembl_gene_id"]
            ),
            models.Index(
                fields=["refseq_gene_id"]
            ),
            # for join with case
            models.Index(
                fields=["case_id"]
            )
        ]


class Case(models.Model):
    sodar_uuid = models.UUIDField(default=uuid_object.uuid4, unique=True, help_text='Case SODAR UUID')
    name = models.CharField(max_length=512)
    index = models.CharField(max_length=32)
    pedigree = JSONField()
    project = models.ForeignKey(
        Project,
        help_text='Project in which this objects belongs',
    )

    class Meta:
        unique_together = (
            "name",
            "index",
        )
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        return self.name


class Dbsnp(models.Model):
    release = models.CharField(max_length=32)
    chromosome = models.CharField(max_length=32)
    position = models.IntegerField()
    reference = models.CharField(max_length=512)
    alternative = models.CharField(max_length=512)
    rsid = models.CharField(max_length=16)
    objects = CopyManager()

    class Meta:
        unique_together = (
            "release",
            "chromosome",
            "position",
            "reference",
            "alternative",
        )
        indexes = [models.Index(fields=["release", "chromosome", "position", "reference", "alternative"])]


class Annotation(models.Model):
    release = models.CharField(max_length=32)
    chromosome = models.CharField(max_length=32)
    position = models.IntegerField()
    reference = models.CharField(max_length=512)
    alternative = models.CharField(max_length=512)
    database = models.CharField(max_length=8, null=True)
    effect = ArrayField(models.CharField(max_length=64, null=True))
    gene_id = models.CharField(max_length=64, null=True)
    transcript_id = models.CharField(max_length=64, null=True)
    transcript_coding = models.NullBooleanField()
    hgvs_c = models.CharField(max_length=512, null=True)
    hgvs_p = models.CharField(max_length=512, null=True)
    objects = CopyManager()

    class Meta:
        unique_together = (
            "release",
            "chromosome",
            "position",
            "reference",
            "alternative",
            "transcript_id",
        )
        indexes = [
            models.Index(
                fields=[
                    "release",
                    "chromosome",
                    "position",
                    "reference",
                    "alternative",
                    "gene_id",
                ]
            )
        ]


class ImportInfo(models.Model):
    table = models.CharField(max_length=16)
    timestamp = models.DateTimeField(editable=False)
    release = models.CharField(max_length=16)
    comment = models.CharField(max_length=1024)


class Exac(models.Model):
    release = models.CharField(max_length=32)
    chromosome = models.CharField(max_length=32)
    position = models.IntegerField()
    reference = models.CharField(max_length=512)
    alternative = models.CharField(max_length=512)
    ac = models.IntegerField(null=True)
    ac_afr = models.IntegerField(null=True)
    ac_amr = models.IntegerField(null=True)
    ac_eas = models.IntegerField(null=True)
    ac_fin = models.IntegerField(null=True)
    ac_nfe = models.IntegerField(null=True)
    ac_oth = models.IntegerField(null=True)
    ac_sas = models.IntegerField(null=True)
    an = models.IntegerField(null=True)
    an_afr = models.IntegerField(null=True)
    an_amr = models.IntegerField(null=True)
    an_eas = models.IntegerField(null=True)
    an_fin = models.IntegerField(null=True)
    an_nfe = models.IntegerField(null=True)
    an_oth = models.IntegerField(null=True)
    an_sas = models.IntegerField(null=True)
    hemi = models.IntegerField(null=True)
    hemi_afr = models.IntegerField(null=True)
    hemi_amr = models.IntegerField(null=True)
    hemi_eas = models.IntegerField(null=True)
    hemi_fin = models.IntegerField(null=True)
    hemi_nfe = models.IntegerField(null=True)
    hemi_oth = models.IntegerField(null=True)
    hemi_sas = models.IntegerField(null=True)
    hom = models.IntegerField(null=True)
    hom_afr = models.IntegerField(null=True)
    hom_amr = models.IntegerField(null=True)
    hom_eas = models.IntegerField(null=True)
    hom_fin = models.IntegerField(null=True)
    hom_nfe = models.IntegerField(null=True)
    hom_oth = models.IntegerField(null=True)
    hom_sas = models.IntegerField(null=True)
    popmax = models.CharField(max_length=8, null=True)
    ac_popmax = models.IntegerField(null=True)
    an_popmax = models.IntegerField(null=True)
    af_popmax = models.FloatField(null=True)
    hemi_popmax = models.IntegerField(null=True)
    hom_popmax = models.IntegerField(null=True)
    af = models.FloatField(null=True)
    af_afr = models.FloatField(null=True)
    af_amr = models.FloatField(null=True)
    af_eas = models.FloatField(null=True)
    af_fin = models.FloatField(null=True)
    af_nfe = models.FloatField(null=True)
    af_oth = models.FloatField(null=True)
    af_sas = models.FloatField(null=True)
    objects = CopyManager()

    class Meta:
        unique_together = (
            "release",
            "chromosome",
            "position",
            "reference",
            "alternative",
        )
        indexes = [
            models.Index(
                fields=[
                    "release",
                    "chromosome",
                    "position",
                    "reference",
                    "alternative",
                ]
            )
        ]


class EnsemblToKegg(models.Model):
    gene_id = models.CharField(max_length=32)
    kegginfo_id = models.IntegerField()
    objects = CopyManager()

    class Meta:
        unique_together = ["gene_id", "kegginfo_id"]
        indexes = [
            models.Index(
                fields=["gene_id"]
            )
        ]


class RefseqToKegg(models.Model):
    gene_id = models.CharField(max_length=32)
    kegginfo_id = models.IntegerField()
    objects = CopyManager()

    class Meta:
        unique_together = ["gene_id", "kegginfo_id"]
        indexes = [
            models.Index(
                fields=["gene_id"]
            )
        ]


class KeggInfo(models.Model):
    kegg_id = models.CharField(max_length=16)
    name = models.CharField(max_length=512)
    objects = CopyManager()


class GnomadExomes(models.Model):
    release = models.CharField(max_length=32)
    chromosome = models.CharField(max_length=32)
    position = models.IntegerField()
    reference = models.CharField(max_length=512)
    alternative = models.CharField(max_length=512)
    ac = models.IntegerField(null=True)
    ac_afr = models.IntegerField(null=True)
    ac_amr = models.IntegerField(null=True)
    ac_asj = models.IntegerField(null=True)
    ac_eas = models.IntegerField(null=True)
    ac_fin = models.IntegerField(null=True)
    ac_nfe = models.IntegerField(null=True)
    ac_oth = models.IntegerField(null=True)
    ac_sas = models.IntegerField(null=True)
    an = models.IntegerField(null=True)
    an_afr = models.IntegerField(null=True)
    an_amr = models.IntegerField(null=True)
    an_asj = models.IntegerField(null=True)
    an_eas = models.IntegerField(null=True)
    an_fin = models.IntegerField(null=True)
    an_nfe = models.IntegerField(null=True)
    an_oth = models.IntegerField(null=True)
    an_sas = models.IntegerField(null=True)
    hemi = models.IntegerField(null=True)
    hemi_afr = models.IntegerField(null=True)
    hemi_amr = models.IntegerField(null=True)
    hemi_asj = models.IntegerField(null=True)
    hemi_eas = models.IntegerField(null=True)
    hemi_fin = models.IntegerField(null=True)
    hemi_nfe = models.IntegerField(null=True)
    hemi_oth = models.IntegerField(null=True)
    hemi_sas = models.IntegerField(null=True)
    hom = models.IntegerField(null=True)
    hom_afr = models.IntegerField(null=True)
    hom_amr = models.IntegerField(null=True)
    hom_asj = models.IntegerField(null=True)
    hom_eas = models.IntegerField(null=True)
    hom_fin = models.IntegerField(null=True)
    hom_nfe = models.IntegerField(null=True)
    hom_oth = models.IntegerField(null=True)
    hom_sas = models.IntegerField(null=True)
    popmax = models.CharField(max_length=8, null=True)
    ac_popmax = models.IntegerField(null=True)
    an_popmax = models.IntegerField(null=True)
    af_popmax = models.FloatField(null=True)
    hemi_popmax = models.IntegerField(null=True)
    hom_popmax = models.IntegerField(null=True)
    af = models.FloatField(null=True)
    af_afr = models.FloatField(null=True)
    af_amr = models.FloatField(null=True)
    af_asj = models.FloatField(null=True)
    af_eas = models.FloatField(null=True)
    af_fin = models.FloatField(null=True)
    af_nfe = models.FloatField(null=True)
    af_oth = models.FloatField(null=True)
    af_sas = models.FloatField(null=True)
    objects = CopyManager()

    class Meta:
        unique_together = (
            "release",
            "chromosome",
            "position",
            "reference",
            "alternative",
        )
        indexes = [
            models.Index(
                fields=[
                    "release",
                    "chromosome",
                    "position",
                    "reference",
                    "alternative",
                ]
            )
        ]


class GnomadGenomes(models.Model):
    release = models.CharField(max_length=32)
    chromosome = models.CharField(max_length=32)
    position = models.IntegerField()
    reference = models.CharField(max_length=512)
    alternative = models.CharField(max_length=512)
    ac = models.IntegerField(null=True)
    ac_afr = models.IntegerField(null=True)
    ac_amr = models.IntegerField(null=True)
    ac_asj = models.IntegerField(null=True)
    ac_eas = models.IntegerField(null=True)
    ac_fin = models.IntegerField(null=True)
    ac_nfe = models.IntegerField(null=True)
    ac_oth = models.IntegerField(null=True)
    an = models.IntegerField(null=True)
    an_afr = models.IntegerField(null=True)
    an_amr = models.IntegerField(null=True)
    an_asj = models.IntegerField(null=True)
    an_eas = models.IntegerField(null=True)
    an_fin = models.IntegerField(null=True)
    an_nfe = models.IntegerField(null=True)
    an_oth = models.IntegerField(null=True)
    hemi = models.IntegerField(null=True)
    hemi_afr = models.IntegerField(null=True)
    hemi_amr = models.IntegerField(null=True)
    hemi_asj = models.IntegerField(null=True)
    hemi_eas = models.IntegerField(null=True)
    hemi_fin = models.IntegerField(null=True)
    hemi_nfe = models.IntegerField(null=True)
    hemi_oth = models.IntegerField(null=True)
    hom = models.IntegerField(null=True)
    hom_afr = models.IntegerField(null=True)
    hom_amr = models.IntegerField(null=True)
    hom_asj = models.IntegerField(null=True)
    hom_eas = models.IntegerField(null=True)
    hom_fin = models.IntegerField(null=True)
    hom_nfe = models.IntegerField(null=True)
    hom_oth = models.IntegerField(null=True)
    popmax = models.CharField(max_length=8, null=True)
    ac_popmax = models.IntegerField(null=True)
    an_popmax = models.IntegerField(null=True)
    af_popmax = models.FloatField(null=True)
    hemi_popmax = models.IntegerField(null=True)
    hom_popmax = models.IntegerField(null=True)
    af = models.FloatField(null=True)
    af_afr = models.FloatField(null=True)
    af_amr = models.FloatField(null=True)
    af_asj = models.FloatField(null=True)
    af_eas = models.FloatField(null=True)
    af_fin = models.FloatField(null=True)
    af_nfe = models.FloatField(null=True)
    af_oth = models.FloatField(null=True)
    objects = CopyManager()

    class Meta:
        unique_together = (
            "release",
            "chromosome",
            "position",
            "reference",
            "alternative",
        )
        indexes = [
            models.Index(
                fields=[
                    "release",
                    "chromosome",
                    "position",
                    "reference",
                    "alternative",
                ]
            )
        ]


class ThousandGenomes(models.Model):
    release = models.CharField(max_length=32)
    chromosome = models.CharField(max_length=32)
    position = models.IntegerField()
    reference = models.CharField(max_length=512)
    alternative = models.CharField(max_length=512)
    ac = models.IntegerField(null=True)
    an = models.IntegerField(null=True)
    het = models.IntegerField(null=True)
    hom = models.IntegerField(null=True)
    af = models.FloatField(null=True)
    af_afr = models.FloatField(null=True)
    af_amr = models.FloatField(null=True)
    af_eas = models.FloatField(null=True)
    af_eur = models.FloatField(null=True)
    af_sas = models.FloatField(null=True)
    objects = CopyManager()

    class Meta:
        unique_together = (
            "release",
            "chromosome",
            "position",
            "reference",
            "alternative",
        )
        indexes = [
            models.Index(
                fields=[
                    "release",
                    "chromosome",
                    "position",
                    "reference",
                    "alternative",
                ]
            )
        ]


class Hgnc(models.Model):
    hgnc_id = models.CharField(max_length=16)
    symbol = models.CharField(max_length=32)
    name = models.CharField(max_length=128)
    locus_group = models.CharField(max_length=32, null=True)
    locus_type = models.CharField(max_length=32, null=True)
    status = models.CharField(max_length=32, null=True)
    location = models.CharField(max_length=64, null=True)
    location_sortable = models.CharField(max_length=64, null=True)
    alias_symbol = models.CharField(max_length=128, null=True)
    alias_name = models.CharField(max_length=512, null=True)
    prev_symbol = models.CharField(max_length=128, null=True)
    prev_name = models.CharField(max_length=1024, null=True)
    gene_family = models.CharField(max_length=256, null=True)
    gene_family_id = models.CharField(max_length=32, null=True)
    date_approved_reserved = models.CharField(max_length=32, null=True)
    date_symbol_changed = models.CharField(max_length=32, null=True)
    date_name_changed = models.CharField(max_length=32, null=True)
    date_modified = models.CharField(max_length=16, null=True)
    entrez_id = models.CharField(max_length=16, null=True)
    ensembl_gene_id = models.CharField(max_length=32, null=True)
    vega_id = models.CharField(max_length=32, null=True)
    ucsc_id = models.CharField(max_length=16, null=True)
    ena = models.CharField(max_length=64, null=True)
    refseq_accession = models.CharField(max_length=128, null=True)
    ccds_id = models.CharField(max_length=256, null=True)
    uniprot_ids = models.CharField(max_length=256, null=True)
    pubmed_id = models.CharField(max_length=64, null=True)
    mgd_id = models.CharField(max_length=256, null=True)
    rgd_id = models.CharField(max_length=32, null=True)
    lsdb = models.CharField(max_length=1024, null=True)
    cosmic = models.CharField(max_length=32, null=True)
    omim_id = models.CharField(max_length=32, null=True)
    mirbase = models.CharField(max_length=16, null=True)
    homeodb = models.CharField(max_length=16, null=True)
    snornabase = models.CharField(max_length=16, null=True)
    bioparadigms_slc = models.CharField(max_length=32, null=True)
    orphanet = models.CharField(max_length=16, null=True)
    pseudogene_org = models.CharField(max_length=32, null=True)
    horde_id = models.CharField(max_length=16, null=True)
    merops = models.CharField(max_length=16, null=True)
    imgt = models.CharField(max_length=32, null=True)
    iuphar = models.CharField(max_length=32, null=True)
    kznf_gene_catalog = models.CharField(max_length=32, null=True)
    namit_trnadb = models.CharField(max_length=16, null=True)
    cd = models.CharField(max_length=16, null=True)
    lncrnadb = models.CharField(max_length=32, null=True)
    enzyme_id = models.CharField(max_length=64, null=True)
    intermediate_filament_db = models.CharField(max_length=32, null=True)
    rna_central_ids = models.CharField(max_length=32, null=True)
    objects = CopyManager()

    class Meta:
        indexes = [models.Index(fields=["ensembl_gene_id"])]


class Mim2gene(models.Model):
    omim_id = models.IntegerField()
    omim_type = models.CharField(max_length=32, null=True)
    entrez_id = models.CharField(max_length=16, null=True)
    symbol = models.CharField(max_length=32, null=True)
    ensembl_gene_id = models.CharField(max_length=32, null=True)
    objects = CopyManager()


class Mim2geneMedgen(models.Model):
    omim_id = models.IntegerField()
    entrez_id = models.CharField(max_length=16, null=True)
    omim_type = models.CharField(max_length=32, null=True)
    source = models.CharField(max_length=32, null=True)
    medgen_cui = models.CharField(max_length=8, null=True)
    comment = models.CharField(max_length=64, null=True)
    objects = CopyManager()

    class Meta:
        indexes = [models.Index(fields=["entrez_id"])]


class Hpo(models.Model):
    database_id = models.CharField(max_length=16)
    name = models.CharField(max_length=1024, null=True)
    qualifier = models.CharField(max_length=4, null=True)
    hpo_id = models.CharField(max_length=16, null=True)
    reference = models.CharField(max_length=128, null=True)
    evidence = models.CharField(max_length=4, null=True)
    onset = models.CharField(max_length=16, null=True)
    frequency = models.CharField(max_length=16, null=True)
    sex = models.CharField(max_length=8, null=True)
    modifier = models.CharField(max_length=16, null=True)
    aspect = models.CharField(max_length=1, null=True)
    biocuration = models.CharField(max_length=32, null=True)
    objects = CopyManager()

    class Meta:
        indexes = [
            models.Index(fields=["database_id"]),
        ]


class Clinvar(models.Model):
    release = models.CharField(max_length=32)
    chromosome = models.CharField(max_length=32)
    position = models.IntegerField()
    reference = models.CharField(max_length=512)
    alternative = models.CharField(max_length=512)
    start = models.IntegerField()
    stop = models.IntegerField()
    strand = models.CharField(max_length=1, null=True)
    variation_type = models.CharField(max_length=16, null=True)
    variation_id = models.IntegerField(null=True)
    rcv = models.CharField(max_length=16, null=True)
    scv = ArrayField(models.CharField(max_length=16, null=True))
    allele_id = models.IntegerField(null=True)
    symbol = models.CharField(max_length=16, null=True)
    hgvs_c = models.CharField(max_length=512, null=True)
    hgvs_p = models.CharField(max_length=512, null=True)
    molecular_consequence = models.CharField(max_length=1024, null=True)
    clinical_significance = models.CharField(max_length=64)
    clinical_significance_ordered = ArrayField(models.CharField(max_length=512))
    pathogenic = models.IntegerField()
    likely_pathogenic = models.IntegerField()
    uncertain_significance = models.IntegerField()
    likely_benign = models.IntegerField()
    benign = models.IntegerField()
    review_status = models.CharField(max_length=64, null=True)
    review_status_ordered = ArrayField(models.CharField(max_length=64, null=True))
    last_evaluated = models.DateField(null=True)
    all_submitters = ArrayField(models.CharField(max_length=512, null=True))
    submitters_ordered = ArrayField(models.CharField(max_length=512, null=True))
    all_traits = ArrayField(models.CharField(max_length=512))
    all_pmids = ArrayField(models.IntegerField(null=True))
    inheritance_modes = models.CharField(max_length=32, null=True)
    age_of_onset = models.CharField(max_length=32, null=True)
    prevalence = models.CharField(max_length=32, null=True)
    disease_mechanism = models.CharField(max_length=32, null=True)
    origin = ArrayField(models.CharField(max_length=16, null=True))
    xrefs = ArrayField(models.CharField(max_length=16, null=True))
    dates_ordered = ArrayField(models.DateField(null=True))
    multi = models.IntegerField()
    objects = CopyManager()

    class Meta:
        indexes = [
            models.Index(fields=["release", "chromosome", "position", "reference", "alternative"])
        ]


class KnowngeneAA(models.Model):
    chromosome = models.CharField(max_length=16)
    start = models.IntegerField()
    end = models.IntegerField()
    transcript_id = models.CharField(max_length=16)
    alignment = models.CharField(max_length=100)
    objects = CopyManager()

    class Meta:
        unique_together = (
            "chromosome",
            "start",
            "end",
            "transcript_id",
        )

        indexes = [
            models.Index(fields=["chromosome", "start", "end"])
        ]
