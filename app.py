#! /usr/bin/env python3
from time import sleep
from selenium import webdriver
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from os import path
import sys, time
import config

class MyHandler(FileSystemEventHandler):
    file_cache = {}
    def on_modified(self, event):
        seconds = int(time.time())
        key = (seconds, event.src_path)
        if key in self.file_cache:
            return
        self.file_cache[key] = True
        print(f'{event.src_path} has been {event.event_type}')
        try:
            web_browser.refresh()
        except:
            observer.stop()
            print('Browser is not running!\nPress CTRL+C to exit.')


if __name__ == "__main__":
    if not path.exists(config.project_dir):
        print('Project directory does not exist!\nPlease open config.py and give a valid path.')
        sys.exit()
    
    web_browser = webdriver.Firefox(executable_path='./geckodriver') if config.browser.lower() == 'firefox' else webdriver.Chrome(executable_path='./chromedriver')
    web_browser.get(config.url)
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=config.project_dir, recursive=True)
    observer.start()

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()