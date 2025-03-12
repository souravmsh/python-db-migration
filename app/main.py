import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.log import log
from utils.benchmark import benchmark
from migrations.subscription import subscription
# from migrations.email import email

def run_task(task):
    try:
        task()
    except Exception as e:
        log.error(f"❌ Task {task.__name__} failed: {e}")
        log.error(f"❌ Detailed error: {traceback.format_exc()}")

def main():
    benchmark_start = benchmark.start(1)
    log.info(f"🚀 Process initiated, {benchmark_start}.")
    print(f"🚀 Process initiated, {benchmark_start}.")

    # tasks = [subscription, email]  # List of tasks to run in parallel
    tasks = [subscription]  # List of tasks to run in parallel
    num_threads = len(tasks)

    try:
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = {executor.submit(run_task, task): task.__name__ for task in tasks}
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    log.error(f"❌ Exception in {futures[future]} execution: {e}")
    except Exception as e:
        log.error(f"❌ Something went wrong: {e}")
        log.error(f"❌ Detailed error: {traceback.format_exc()}")

    benchmark_end = benchmark.end(1)
    print(f"✅ Process completed {benchmark_end}.\n" + ("_" * 80))
    log.info(f"✅ Process completed {benchmark_end}.\n" + ("_" * 80))

if __name__ == "__main__":
    main()
