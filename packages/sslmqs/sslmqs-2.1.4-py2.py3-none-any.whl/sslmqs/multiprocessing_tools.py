import logging
import signal


def setup_sigterm(exit_event):
    # exit_event can be either a single multiprocessing.Event() or a list.
    def terminate(signum, frame):
        if isinstance(exit_event, list):
            for e in exit_event:
                e.set()
        else:
            exit_event.set()

    signal.signal(signal.SIGINT, terminate)
    signal.signal(signal.SIGTERM, terminate)


def terminate_process(process, log=None, timeout=2):
    defaulted_log = log or logging.getLogger("sslmqs")
    if process:
        process.join(timeout)
        if process.is_alive():
            process.terminate()

        defaulted_log.info("Process {} exited with code {}.".format(
            process.name, process.exitcode))
    else:
        defaulted_log.info("Process {} not exited, because it wasn't started.")
