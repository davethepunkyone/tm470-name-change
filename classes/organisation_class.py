
class Organisation:

    def __init__(self, **kwargs):
        self._org_id = None
        self._org_name = None
        self._requires_verified = None
        self._avg_time_to_process_days = None
        if len(kwargs) > 0:
            self.sort_kwargs(**kwargs)

    def sort_kwargs(self, **kwargs):
        for key, value in kwargs.items():
            if key == "org_id":
                self.org_id = value
            elif key == "org_name":
                self.org_name = value
            elif key == "requires_verified":
                self.requires_verified = value
            elif key == "avg_time_to_process_days":
                self.avg_time_to_process_days = value
            else:
                raise KeyError("Keyword ({}) provided is not a valid property".format(key))

    @property
    def org_id(self) -> int:
        return self._org_id

    @org_id.setter
    def org_id(self, org_id: int) -> None:
        self._org_id = org_id

    @property
    def org_name(self) -> str:
        return self._org_name

    @org_name.setter
    def org_name(self, org_name_to_use: str) -> None:
        self._org_name = org_name_to_use

    @property
    def requires_verified(self) -> bool:
        return self._requires_verified

    @requires_verified.setter
    def requires_verified(self, req_ver: bool) -> None:
        self._requires_verified = req_ver

    @property
    def avg_time_to_process_days(self) -> int:
        return self._avg_time_to_process_days

    @avg_time_to_process_days.setter
    def avg_time_to_process_days(self, process_time: int) -> None:
        self._avg_time_to_process_days = process_time
