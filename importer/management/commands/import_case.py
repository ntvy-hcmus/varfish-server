"""Django command for importing a case after annotation with ``varfish-annotator``."""

import tempfile

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from annotation.models import Annotation
from projectroles.models import Project
from variants.models import SmallVariant, Case


class Command(BaseCommand):
    """Implementation of importing a case from pedigree, variants, and genotype file.

    The necessary steps are:

    - Create a new ``Case`` in the appropriate ``Project`` (specified by UUID)
    - Import the variant ``Annotation`` records for the case's variants
    - Import the ``SmallVariant`` call information

    All steps are executed in a transaction, so no stale state is left in the database.
    """

    #: Help message displayed on the command line.
    help = "Import case from PED file and varfish-annotator output."

    def add_arguments(self, parser):
        """Add the command's argument to the ``parser``."""
        parser.add_argument("--case-name", help="Name to assign to the case", required=True)
        parser.add_argument("--index-name", help="The name of the index sample", required=True)
        parser.add_argument("--path-ped", help="Path to pedigree input file", required=True)
        parser.add_argument("--path-genotypes", help="Path to genotypes TSV file", required=True)
        parser.add_argument("--path-variants", help="Path to variants TSV file", required=True)
        parser.add_argument("--project-uuid", help="UUID of the project to add the case to", required=True)

    @transaction.atomic
    def handle(self, *args, **options):
        """Perform the import of the case."""
        project = self._get_project(options["project_uuid"])
        case = self._create_case(project, options["case_name"], options["index_name"], options["path_ped"])
        self._import_variants(options["path_variants"])
        self._import_genotypes(case, options["path_genotypes"])

    def _get_project(self, project_uuid):
        """Get query or raise appropriate exception."""
        try:
            return Project.objects.get(sodar_uuid=project_uuid)
        except ObjectDoesNotExist:
            raise CommandError("Project with UUID {} does not exist".format(project_uuid))

    def _create_case(self, project, case_name, index_name, path_ped):
        """Create ``Case`` object."""
        self.stdout.write('Reading PED and creating case...')
        # Build Pedigree.
        pedigree = []
        seen_index = False
        with open(path_ped, 'rt') as pedf:
            for line in pedf:
                line = line.strip()
                _, patient, father, mother, sex, affected = line.split("\t")
                seen_index = seen_index or patient == index_name
                sex = int(sex)
                affected = int(affected)
                pedigree.append({
                    "patient": patient,
                    "father": father,
                    "mother": mother,
                    "sex": sex,
                    "affected": affected,
                })
        if not seen_index:
            raise CommandError("Index {} not seen in pedigree!".format(index_name))
        # Construct ``Case`` object.
        case = Case.objects.create(
            name=case_name,
            index=index_name,
            pedigree=pedigree,
            project=project,
        )
        self.stdout.write(self.style.SUCCESS('Done creating case'))
        return case

    def _import_variants(self, path_variants):
        """Import variants TSV file into database."""
        self.stdout.write('Importing variants...')
        Annotation.objects.from_csv(
            path_variants,
            delimiter="\t",
            ignore_conflicts=True,
            drop_constraints=False,
            drop_indexes=False,
        )
        self.stdout.write(self.style.SUCCESS('Finished importing variants'))

    def _import_genotypes(self, case, path_genotypes):
        """Import variants TSV file into database."""
        self.stdout.write('Creating temporary genotype file...')
        with tempfile.NamedTemporaryFile("w+t") as tempf:
            with open(path_genotypes, "rt") as inputf:
                header = inputf.readline().strip()
                try:
                    replace_idx = header.split('\t').index("case_id")
                except ValueError as e:
                    raise CommandError("Column 'case_id' not found in genotypes TSV") from e
                tempf.write(header)
                tempf.write("\n")
                while True:
                    line = inputf.readline().strip()
                    if not line:
                        break
                    arr = line.split("\t")
                    arr[replace_idx] = str(case.pk)
                    tempf.write("\t".join(arr))
                    tempf.write("\n")
            tempf.flush()
            self.stdout.write('Importing genotype file...')
            SmallVariant.objects.from_csv(
                tempf.name,
                delimiter="\t",
                null=".",
                ignore_conflicts=True,
                drop_constraints=False,
                drop_indexes=False,
            )
            self.stdout.write(self.style.SUCCESS('Finished importing genotypes'))