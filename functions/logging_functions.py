import datetime


def log_info(message_to_log: str) -> None:
    print("INFO: " + str(message_to_log))


def log_benchmark(process_to_log: str) -> None:
    current_time = datetime.datetime.now()
    print("BENCHMARK: " + str(process_to_log) + " | TIME: " + datetime.datetime.strftime(current_time,
                                                                                         "%d/%m/%Y %H:%M:%S"))


log_benchmark("test")
