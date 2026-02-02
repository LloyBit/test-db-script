from script.database import database
from script.commands.base import Command
import docker




class QuitCommand(Command):
    def _stop_postgres_container(self):
        try:
            
            client = docker.from_env()
            for c in client.containers.list(filters={"label": "com.docker.compose.service=postgres"}):
                c.stop()
                print("Postgres container stopped")
        except Exception:
            print("Docker unavailable or not in compose")
    def run(self):
        database.close()
        self._stop_postgres_container()
        exit(0)