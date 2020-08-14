from classes.organisation_class import Organisation


def return_specific_org_from_list(list_of_orgs: list, org_needed: int) -> Organisation:
    for org in list_of_orgs:
        if org.org_id == org_needed:
            return org
    else:
        raise ValueError("Org ID provided ({}) is not in the list of organisations".format(org_needed))
