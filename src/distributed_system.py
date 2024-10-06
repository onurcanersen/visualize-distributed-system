from neo4j_manager import Neo4jManager
import subprocess
import re
import schedule
import time

class DistributedSystem:
    def __init__(self):
        self.fetch_interval = 30
        self.neo4j_manager = Neo4jManager()     
        self.fetch_information()

    def _run_dump_information(self):
        try:
            output = subprocess.check_output(["bash", "../scripts/dump_information.sh"], universal_newlines=True)

            info_pattern = re.compile(r"(Information\d+)\nP:\s*(\d+)\nC:\s*(\d+)", re.MULTILINE)
            
            matches = info_pattern.findall(output)

            for match in matches:
                info, p_id, c_id = match
                self.neo4j_manager.create_application(p_id)
                self.neo4j_manager.create_application(c_id)
                self.neo4j_manager.create_information(p_id, c_id, info)
                print(f"Information: {info}, P: {p_id}, C: {c_id}")
        
        except Exception as e:
            print(e)

    def fetch_information(self):
        self._run_dump_information()

        schedule.every(self.fetch_interval).seconds.do(self._run_dump_information)

        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    distributed_system = DistributedSystem()