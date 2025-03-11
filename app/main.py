import time
from tables.subscription import Subscription
from utils.log import log


def main():
    log.info(f"🚀 Migration process started...")
    print(f"🚀 Migration process started...")
    # time.sleep(1000)

    try:
        Subscription()
    except Exception as e:
        log.error(f"❌ An error occurred: {e}")

    log.info("_" * 80)
    print("_" * 80)

if __name__ == "__main__":
    main()

