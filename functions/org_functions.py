from classes.organisation_class import Organisation


def return_specific_org_from_list(list_of_orgs: list, org_needed: int) -> Organisation:
    """This returns a specific organisation from a list of organisations as an Organisation object.

    Keyword arguments:
    list_of_orgs (list) -- A list of Organisation objects that a value needs extracting from.
    org_needed (int) -- The organisation id of the Organisation object needed from the list"""
    for org in list_of_orgs:
        if org.org_id == org_needed:
            return org
    else:
        raise ValueError("Org ID provided ({}) is not in the list of organisations".format(org_needed))
