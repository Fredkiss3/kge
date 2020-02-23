from concurrent.futures import as_completed
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import urllib.request

URLS = ['http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://some-made-up-domain.com/',
        'http://eboagroup.com/']


def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()


def main1():
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:

        future_to_url = {executor.submit(
            load_url, url, 30): url for url in URLS}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
            else:
                print('%r page is %d bytes' % (url, len(data)))


values = [2, 3, 4, 5]


def square(n):
    import time
    time.sleep(.5)
    return n * n




def main():
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = executor.map(square, values)
        for result in results:
            print(result)


# if __name__ == '__main__':
#     main()
