from classes.organisation_class import Organisation


def mock_list_of_organisations() -> list:
    mock_org_1 = Organisation(org_id=50, org_name="Testing Organisation 1", avg_time_to_process_days=3)
    mock_org_2 = Organisation(org_id=55, org_name="Another Testing Organisation", avg_time_to_process_days=14)
    mock_org_3 = Organisation(org_id=57, org_name="Open University", avg_time_to_process_days=5)

    return [mock_org_1, mock_org_2, mock_org_3]

