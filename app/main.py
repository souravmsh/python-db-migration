import time
import datetime
import traceback
from migrations.subscription import Subscription
from migrations.bank import Bank
from utils.log import log
from utils.benchmark import benchmark

def main():
    benchmark_start = benchmark.start(1)
    log.info(f"🚀 Migration process initiated at {benchmark_start}.")
    print(f"🚀 Migration process initiated at {benchmark_start}.")

    try:
        # Begin the migration process
        # Subscription()  # Uncomment if you want to run Subscription migration as well
        Bank()
        print(benchmark.progress(1))
        
    except Exception as e:
        log.error(f"❌ Something went wrong: {e}")
        log.error(f"❌ Detailed error: {traceback.format_exc()}")
        print("✅ Migration " + benchmark.progress(1))

    # End of the process
    benchmark_end = benchmark.end(1)
    print(f"✅ Migration completed {benchmark_end}.\n" + ("_" * 80))
    log.info(f"✅ Migration completed {benchmark_end}.\n" + ("_" * 80))

if __name__ == "__main__":
    main()
