import traceback
from migrations.subscription import subscription
from utils.log import log
from utils.benchmark import benchmark

def main():
    benchmark_start = benchmark.start(1)
    log.info(f"🚀 Process initiated, {benchmark_start}.")
    print(f"🚀 Process initiated, {benchmark_start}.")

    try:
        # Begin the Process
        subscription()


        
    except Exception as e:
        log.error(f"❌ Something went wrong: {e}")
        log.error(f"❌ Detailed error: {traceback.format_exc()}")
        print("✅ Process " + benchmark.progress(1))

    # End of the process
    benchmark_end = benchmark.end(1)
    print(f"✅ Process completed {benchmark_end}.\n" + ("_" * 80))
    log.info(f"✅ Process completed {benchmark_end}.\n" + ("_" * 80))

if __name__ == "__main__":
    main()
