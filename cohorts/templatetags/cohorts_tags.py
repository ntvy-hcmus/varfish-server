from django import template

from variants.models import Case

register = template.Library()


@register.filter
def get_accessible_cases(item, user):
    """Return all accessible for a cohort and user."""
    return getattr(item, "get_accessible_cases_for_user")(user)


@register.filter
def check_accessible_cases(item, user):
    """Check if all cases of a cohort are accessible for a user."""
    if user == item.user or user.is_superuser:
        return True

    return set(item.cases.filter(project__roles__user=user)) == set(item.cases.all())


@register.filter
def case_is_in_project(item, project):
    """Check if a case (extracted from a form item) is in a project.

    This just helps to organize the form and group the case checkboxes by project.
    """
    return Case.objects.get(id=item.data["value"]).project == project
