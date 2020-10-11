import os, threading

try:
    import requests
    from colorama import Fore, init
except (ModuleNotFoundError):
    os.system('pip install requests colorama')
init(convert=True)

class RobloxChecker:
    def __init__(self, threadCount):
        self.threadCount = threadCount
        self.threads = []
        self.names = open('names.txt', 'r').read().replace("\r", '').split('\n')
        self.lock = threading.Lock()
        self.valid = 0
        self.total = 0

    def setTitle(self):
        os.system(f'title [RobloxChecker] - {self.valid}/{self.total} - valid')

    def start(self):
        for name in self.names:
            while True:
                if threading.active_count() <= self.threadCount:
                    threading.Thread(target=self.check, args=(name,)).start()
                    break

    def check(self, name: str):
        if name and len(name) > 3 < 20:
            self.total += 1
            request = requests.get( f'https://auth.roblox.com/v1/usernames/validate?birthday=2000-04-20T08:00:00.000Z&context=Signup&username={name.lower()}').json()

            if request['code'] == 0:
                self.valid+=1
                self.lock.acquire()
                print(f'[{Fore.RED}RobloxChecker{Fore.RESET}] {Fore.GREEN}Not Taken{Fore.RESET}: {name}')
                self.setTitle()
                self.lock.release()
                with open('valid.txt', 'a+') as file:
                        file.write(f'{name}\n')
                        file.close()
            else:
                self.lock.acquire()
                print(f'[{Fore.RED}RobloxChecker{Fore.RESET}] {Fore.MAGENTA}Name Taken{Fore.RESET}: {name}')
                self.setTitle()
                self.lock.release()
                

if __name__ == '__main__':
    os.system('cls')
    print(f'[{Fore.RED}RobloxChecker{Fore.RESET}] -> Threads: ', end='')
    threads = input('')
    check = RobloxChecker(int(threads))
    check.start()
