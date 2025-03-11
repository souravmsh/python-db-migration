# Migrating Between MSSQL and MySQL Databases Using Python and Docker

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
git clone git@github.com:souravmsh/mssql-to-mysql-db-migration.git
cd mssql-to-mysql-db-migration
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
│── utils/
│   ├── config.py
│   ├── log.py
│   ├── migrate.py
│   ├── mysql.py
│   ├── mssql.py
│── main.py
│── test.py 


## **6. Migration Table Information**
Migration table scripts are located inside the `migrations/` directory. Each Python file inside this directory represents a specific table migration.

To run a single migration file inside `main.py`, use the following format:

### **Example: Running the `Client` Migration**
```python
import time
from migrations.subscription import Subscription
from utils.log import log

def main():
    log.info(f"🚀 Migration process started...")
    # time.sleep(1000)

    try:
        Subscription()
    except Exception as e:
        log.error(f"❌ An error occurred: {e}")

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
python migrations/client.py
```
This will execute the database migration process.

To execute a specific table migration:
```sh
docker exec -it migration-app python migrations/client.py
```
or
```sh
docker exec -it migration-app sh
python migrations/client.py
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

## **Sample Command to Run `app/main.py`**
To execute the migration script directly in one command:
```sh
docker exec -it migration-app python main.py
```
or run specific table:-
```sh
docker exec -it migration-app python migrations/subscription.py
```

---

## **Conclusion**
You have now successfully set up and run the database migration project inside a Docker container. 🚀 Let me know if you need further assistance! 😊

