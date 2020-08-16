import datetime
import os


def get_logging_directory() -> str:
    parent_dir = os.path.dirname(os.getcwd())
    return os.path.join(parent_dir, 'logging')


def check_logging_directory() -> None:
    current_logging_dir = get_logging_directory()
    if not os.path.exists(current_logging_dir):
        os.mkdir(current_logging_dir)
        print("CREATED DIR: {}".format(current_logging_dir))


def log_info(message_to_log: str) -> None:
    print("INFO: " + str(message_to_log))


def log_benchmark(process_to_log: str) -> None:
    check_logging_directory()
    current_time = datetime.datetime.now()
    benchmark_string = "BENCHMARK|" + str(process_to_log) + "|TIME|" + \
                       datetime.datetime.strftime(current_time, "%d/%m/%Y %H:%M:%S")
    print(benchmark_string)
    bm = open(get_logging_directory() + "/benchmark_log.txt", "a")
    bm.write(benchmark_string + "\n")
    bm.close()
