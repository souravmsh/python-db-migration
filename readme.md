# Migrating Between MSSQL / ORACLE and MySQL Databases Using Python and Docker

This guide provides step-by-step instructions to set up and run the database migration project using Docker.

---

## **Prerequisites**
Ensure you have the following installed before proceeding:

1. **Docker** (Install from: [Docker Official Site](https://docs.docker.com/get-docker/))
2. **Docker Compose** (Included with Docker Desktop or install separately: [Docker Compose](https://docs.docker.com/compose/install/))

---

## **1. Clone the Repository**
If you haven't already, clone the repository to your local machine:
```sh
git clone git@github.com:souravmsh/python-db-migration.git
cd python-db-migration
```

---

## **2. Build and Start the Docker Container**
Navigate to the project root directory (where `docker-compose.yml` is located) and build the container:
```sh
docker-compose build
```
Then, start the container:
```sh
docker-compose up -d
```
- The `-d` flag runs the container in detached mode (in the background).

---

## **3. Verify the Running Container**
Check if the container is running successfully:
```sh
docker ps
```
You should see a running container named **migration-app**.

---

## **4. Access the Running Container**
To enter the running container and interact with the environment:
```sh
docker exec -it migration-app sh
```
This will open a shell session inside the container.

---

## **5. Script Directory Structure**
```
app/
│── logs/
│   ├── 2025-10-03.log
│   ├── .....
│── migrations/
│   ├── client.py
│   ├── orders.py
│   ├── subscriber.py
│   ├── .....
│── tests/
│   ├── connection.py
│   ├── subscriber.py
│── utils/
│   ├── benchmark.py
│   ├── config.py
│   ├── log.py
│   ├── migrate.py
│   ├── mysql.py
│   ├── mssql.py
│   ├── oracle.py
│── main.py
│── test.py 
```

---

## **6. Migration Table Information**
Migration table scripts are located inside the `migrations/` directory. Each Python file inside this directory represents a specific table migration.

To run a single migration file inside `main.py`, use the following format:

### **Example: Running the `Client` Migration**
```python
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
```

---

## **7. Run the Migration Script**
Once inside the container, navigate to the root directory and run your migration script:
```sh
python main.py
```
or
```sh
python migrations/subscription.py
```
This will execute the database migration process.

To execute a specific table migration:
```sh
docker exec -it migration-app sh migrations/subscription.py
```
or
```sh
docker exec -it migration-app sh
python migrations/subscription.py
```

---

## **8. Stopping and Removing Containers**
To stop the running container:
```sh
docker-compose down
```
To remove all stopped containers and free up space:
```sh
docker system prune -a
```

---

## **9. Troubleshooting**
### **Check Logs**
If there are any issues, check the logs using:
```sh
docker-compose logs
```
or
```sh
docker logs migration-app
```

### **Verify ODBC Installation**
Inside the container, check if the ODBC drivers are installed correctly:
```sh
odbcinst -q -d
```
This should list available ODBC drivers, including:
```
[ODBC Driver 17 for SQL Server]
[ODBC Driver 18 for SQL Server]
```

---

## **10. Removing and Rebuilding Everything (If Needed)**
If you face issues and need to rebuild everything from scratch:
```sh
docker-compose down --volumes --remove-orphans
docker-compose build --no-cache
docker-compose up -d
```

---

## **11. .env Configuration**

Before running the migration, you need to configure the database connection settings in your `.env` file. Below are the required environment variables:

```
SOURCE_DATABASE=MSSQL           # MSSQL / MYSQL / ORACLE
DESTINATION_DATABASE=MYSQL      # MYSQL / MSSQL / ORACLE
QUERY_CHUNK_SIZE=1000

# MySQL Database Configuration
# ---------------------------------------
MYSQL_HOST=null
MYSQL_PORT=3306
MYSQL_USER=null
MYSQL_PASSWORD=null
MYSQL_DATABASE=null

# MSSQL Database Configuration
# ---------------------------------------
MSSQL_DRIVER="ODBC Driver 18 for SQL Server"
MSSQL_SERVER=null
MSSQL_PORT=1433
MSSQL_DATABASE=null
MSSQL_UID=null
MSSQL_PWD=null
MSSQL_ENCRYPT=yes

# ORACLE Database Configuration
# --------------------------------------- 
ORACLE_HOST=null
ORACLE_PORT=1521 
ORACLE_USER=null
ORACLE_PASSWORD=null
ORACLE_SID=null
```

Make sure to replace the placeholder values (`null`) with your actual database configurations. This will ensure that your migration process can connect to the appropriate databases.

---

## **12. Sample Command to Run `app/main.py`**
To execute the migration script directly in one command:
```sh
docker exec -it migration-app sh main.py
```
or run a specific table:
```sh
docker exec -it migration-app sh migrations/subscription.py
```

---

## **Conclusion**
You have now successfully set up and run the database migration project inside a Docker container. 🚀 Let me know if you need further assistance! 😊