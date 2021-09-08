import requests
import threading
from requests import exceptions
from requests.exceptions import HTTPError
# Data is retrieved using the MetaWeather API at https://www.metaweather.com/api/

threadLock = threading.Lock()

class newThread (threading.Thread):
    def __init__(self, tID, name, apiURL):
        threading.Thread.__init__(self)
        self.tID = tID
        self.name = name
        self.URL = apiURL
    def run(self):
        # Getting a lock to sync the threads, then freeing a lock to release the next thread
        threadLock.acquire()
        average_max_temp(self.name, self.URL)
        threadLock.release()

def average_max_temp(name, URL):
    try:
        response = requests.get(URL)
        response.raise_for_status()
        jsonResponse = response.json()
        total = counter = 0

        for k, v in jsonResponse.items():
            if k == 'consolidated_weather':
                for dictionary in v:
                    total += dictionary['max_temp']
                    counter += 1
            total = total/counter
            print(name + " Average Max Temp: " + str(total))
            break

    except HTTPError as http_err:
        print(f'An HTTP error has occurred: {http_err}')
    except Exception as err:
        print(f'Another error has occurred: {err}')

def main():
    tList = []
    
    t1 = newThread(1, "Salt Lake City", "https://www.metaweather.com/api/location/2487610/")
    t2 = newThread(2, "Los Angeles", "https://www.metaweather.com/api/location/2442047/")
    t3 = newThread(3, "Boise", "https://www.metaweather.com/api/location/2366355/")

    t1.start()
    t2.start()
    t3.start()

    tList.append(t1)
    tList.append(t2)
    tList.append(t3)

    for t in tList:
        t.join()
    #print("Exiting the main thread")

if __name__ == '__main__':
    main()
    