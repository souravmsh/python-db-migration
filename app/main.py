import time
import datetime
import traceback
from migrations.subscription import Subscription
# from migrations.subscription2 import Subscription2
from utils.log import log

def main():
    start_time = time.perf_counter()
    log.info(f"🚀 Migration process initiated at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")
    print(f"🚀 Migration process initiated at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")

    try:
        # Begin the migration process
        Subscription()  # Uncomment if you want to run Subscription migration as well
        # Subscription2()
    except Exception as e:
        log.error(f"❌ Something went wrong: {e}")
        log.error(f"❌ Detailed error: {traceback.format_exc()}")

    # End of the process
    duration = time.perf_counter() - start_time
    print(f"✅ Migration completed in {duration:.2f} seconds at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.\n" + ("_" * 80))
    log.info(f"✅ Migration completed in {duration:.2f} seconds at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.\n" + ("_" * 80))

if __name__ == "__main__":
    main()
