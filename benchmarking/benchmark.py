"Benchmark diskcache.DjangoCache"

import collections as co
import os
import pickle
import random
import shutil
import time
from threading import Thread

from utils import Complex, display

PROCS = 8
OPS = int(1e5)
RANGE = int(1.1e3)
WARMUP = int(1e3)
USE_STRINGS = True


def setup():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    import django

    django.setup()


def worker(num, name):
    setup()

    from django.core.cache import caches

    obj = caches[name]

    random.seed(num)

    timings = co.defaultdict(list)

    time.sleep(0.01)  # Let other processes start.

    for count in range(OPS):
        key = str(random.randrange(RANGE)).encode("utf-8")
        value = str(count).encode("utf-8") * random.randrange(1, 100)
        if not USE_STRINGS:
            value = Complex(value)
        choice = random.random()

        if choice < 0.900:
            start = time.time()
            result = obj.get(key)
            end = time.time()
            miss = result is None
            action = "get"
        elif choice < 0.990:
            start = time.time()
            result = obj.set(key, value)
            end = time.time()
            miss = result is False
            action = "set"
        else:
            start = time.time()
            result = obj.delete(key)
            end = time.time()
            miss = result is False
            action = "delete"

        if count > WARMUP:
            delta = end - start
            timings[action].append(delta)
            if miss:
                timings[action + "-miss"].append(delta)

    with open(f"output-{num}.pkl", "wb") as writer:
        pickle.dump(timings, writer, protocol=pickle.HIGHEST_PROTOCOL)


def prepare(name):
    setup()

    from django.core.cache import caches

    obj = caches[name]

    for key in range(RANGE):
        key = str(key).encode("utf-8")
        obj.set(key, key)

    try:
        obj.close()
    except Exception:
        pass


def dispatch():
    setup()

    for name in ["locmem", "lrumem", "lrumem_pure"]:
        shutil.rmtree("tmp", ignore_errors=True)

        preparer = Thread(target=prepare, args=(name,))
        preparer.start()
        preparer.join()

        processes = [Thread(target=worker, args=(value, name)) for value in range(PROCS)]

        for process in processes:
            process.start()

        for process in processes:
            process.join()

        timings = co.defaultdict(list)

        for num in range(PROCS):
            filename = f"output-{num}.pkl"

            with open(filename, "rb") as reader:
                output = pickle.load(reader)

            for key in output:
                timings[key].extend(output[key])

            os.remove(filename)

        name = "{}-{}-{}".format(name, "strings" if USE_STRINGS else "objects", RANGE)
        display(name, timings)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,)
    parser.add_argument(
        "-p", "--processes", type=int, default=PROCS, help="Number of processes to start",
    )
    parser.add_argument(
        "-n", "--operations", type=float, default=OPS, help="Number of operations to perform",
    )
    parser.add_argument(
        "-r", "--range", type=int, default=RANGE, help="Range of keys",
    )
    parser.add_argument(
        "-w",
        "--warmup",
        type=float,
        default=WARMUP,
        help="Number of warmup operations before timings",
    )
    parser.add_argument(
        "--profile", action="store_true", help="Run the benchmark with cProfile in the foreground"
    )
    parser.add_argument(
        "--complex",
        action="store_true",
        help="Use class instances as cache values rather than strings",
    )

    args = parser.parse_args()

    PROCS = int(args.processes)
    OPS = int(args.operations)
    RANGE = int(args.range)
    WARMUP = int(args.warmup)
    USE_STRINGS = not args.complex

    if args.profile:
        for x in range(PROCS):
            worker(x, "lrumem")
    else:
        dispatch()
