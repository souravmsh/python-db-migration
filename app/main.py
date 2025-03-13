import traceback
from concurrent.futures import ThreadPoolExecutor
from utils.log import log
from utils.benchmark import benchmark
from migrations.subscription import subscription

def run_task(task, name):
    try:
        log.info(f"🚀 Task {name} started.")
        task()
        log.info(f"✅ Task {name} completed.")
    except Exception as e:
        log.error(f"❌ Task {name} failed: {e}")
        log.error(f"❌ Detailed error: {traceback.format_exc()}")

def main():
    benchmark_start = benchmark.start(1)
    log.info(f"🚀 Process initiated, {benchmark_start}.")
    print(f"🚀 Process initiated, {benchmark_start}.")

    # Define multiple jobs to run in parallel
    jobs = {
        "Subscription Job": subscription,
        "Email Job": subscription,
        "Another Subscription": subscription,
    }

    try:
        with ThreadPoolExecutor(max_workers=len(jobs)) as executor:
            futures = {executor.submit(run_task, task, name): name for name, task in jobs.items()}
            for future in futures:
                future.result()  # Ensures all tasks run in parallel
    except Exception as e:
        log.error(f"❌ Something went wrong: {e}")
        log.error(f"❌ Detailed error: {traceback.format_exc()}")

    benchmark_end = benchmark.end(1)
    print(f"✅ Process completed {benchmark_end}.\n" + ("_" * 80))
    log.info(f"✅ Process completed {benchmark_end}.\n" + ("_" * 80))

if __name__ == "__main__":
    main()
