import psutil
import threading
import os
from colorama import Fore, Style
import _thread
import time

__all__ = ['exit_on_out_of_ram']


def exit_on_out_of_ram(minimal_ram: int, warn_on: int = None, print_warning: bool = True, sleep_time: float = 0.5):
    def surely_kill_the_process():
        _thread.interrupt_main()
        # If it's still alive for some reasons
        time.sleep(10)
        os._exit(1)

    def watching_cycle():
        nonlocal warn_on
        if not warn_on:
            warn_on = 2 * minimal_ram

        try:
            while True:
                ram_stat = psutil.virtual_memory()
                available_ram = ram_stat.available
                if available_ram <= warn_on and print_warning:
                    percents = 100 - ram_stat.percent
                    print(f"{Fore.RED}[WARNING]: Running out of RAM: available {available_ram} bytes"
                          f"({percents:.2f}% of total){Style.RESET_ALL}")
                if available_ram < minimal_ram:
                    print(f"{Fore.RED}Further execution may cause freezing of your machine. "
                          f"Finishing the program by sending KeyboardInterrupt...{Style.RESET_ALL}")
                    surely_kill_the_process()
        except Exception as e:
            print(e)
            print(f"{Fore.RED}Something went wrong in {exit_on_out_of_ram.__name__}. "
                  f"Finishing the program by sending KeyboardInterrupt...{Style.RESET_ALL}")
            surely_kill_the_process()
        time.sleep(sleep_time)

    thread = threading.Thread(target=watching_cycle)
    thread.daemon = True
    thread.start()


def main():
    one_gigabyte = 1 << 30
    exit_on_out_of_ram(one_gigabyte)

    # explode your RAM
    extremely_big_number = 1 << 9999999
    _ = [i for i in range(extremely_big_number)]


if __name__ == '__main__':
    main()
