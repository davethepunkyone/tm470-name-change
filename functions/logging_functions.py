import datetime
import os


def get_logging_directory() -> str:
    """This returns the logging directory as a str.

    Expected path: /logging"""
    return os.path.join(os.getcwd(), 'logging')


def check_logging_directory() -> None:
    """This checks that the logging directory exists and if not, creates the directory ready for use."""
    current_logging_dir = get_logging_directory()
    if not os.path.exists(current_logging_dir):
        os.mkdir(current_logging_dir)
        print("CREATED DIR: {}".format(current_logging_dir))


def log_info(message_to_log: str) -> None:
    """This prints the specified message to the debug menu as an INFO log.

    Keyword arguments:
    message_to_log (str) -- The message to log to the debug menu."""
    print("INFO: " + str(message_to_log))


def log_benchmark(process_to_log: str) -> None:
    """This logs a benchmark value to the benchmark log file.  Benchmarks record the activity and the time that
    activity was conducted in the following format: BENCHMARK|Activity|TIME|datetime (dd/mm/yyyy hh:mm:ss)

    Keyword arguments:
    process_to_log (str) -- The process to log to the benchmark file."""
    check_logging_directory()
    current_time = datetime.datetime.now()
    benchmark_string = "BENCHMARK|" + str(process_to_log) + "|TIME|" + \
                       datetime.datetime.strftime(current_time, "%d/%m/%Y %H:%M:%S")
    print(benchmark_string)
    bm = open(get_logging_directory() + "/benchmark_log.txt", "a")
    bm.write(benchmark_string + "\n")
    bm.close()
