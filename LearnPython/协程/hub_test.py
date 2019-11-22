from hub_lib import hub
import time
hub.patch(thread=False)

urls = [
    "https://www.google.com/intl/en_ALL/images/logo.gif",
    "http://python.org/images/python-logo.gif",
    "http://us.i1.yimg.com/us.yimg.com/i/ww/beta/y3.gif",
]


def fetch(url):
    print("opening", url)
    time.sleep(2)
    body = [2]
    print("done with", url)
    return url, body


if __name__ == '__main__':

    start = time.time()
    services = []
    for i in urls:
        b = fetch(i)
        thr = hub.spawn_after(b)
        services.append(thr)
    hub.joinall(services)

    print(time.time() - start)
