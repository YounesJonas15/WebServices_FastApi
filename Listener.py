import os
import time
import requests

def listener(path):
    try:
        dirs = os.listdir(path)
        before = set(dirs)

        while True:
            after = set(os.listdir(path))
            added = after - before

            if added:
                for file_name in added:
                    print(file_name)
                    file_path = path + "/" + file_name
                    data = {"file_path" : file_path}
                    print (data)
                    response = requests.post("http://127.0.0.1:8001/Orchestration/", json = data)
                    if response.status_code == 200:
                        print(f"File successfully sent.")
                    else:
                        print(f"Failed to send file. Status code: {response.status_code}")
            before = after
            time.sleep(1)  # Ajout d'une pause pour éviter une utilisation excessive du CPU
    except Exception as e:
        print(f"Error in listener: {e}")

# Start listening for changes in the "demandes" directory
listener("demandes")
