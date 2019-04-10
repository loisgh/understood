from bs4 import BeautifulSoup
import urllib3
import time


def parse_html(data):
    the_link = None
    for p in data:
        we_should_return = False
        # hatnote is class with font set to italic
        if p.get('class') != 'hatnote':
            links = p.find_all('a', href=True)
            if links:
                for link in links:
                    if link in links_dict:
                        continue
                    elif link.get('href').startswith("#"):
                        continue
                    elif not link.get('title'):
                        continue
                    elif '(' and ')' in link.get('title'):
                        continue
                    else:
                        the_link = link
                        if not link:
                            continue
                        we_should_return = True
                        links_dict[link] = 1
                        print(link)
                        break
        if not the_link:
            continue
        if we_should_return:
            return the_link


def get_html_page_for_parsing(in_url, first_page):
    page = http.request('GET', in_url)
    if not first_page:
        first_page = page.geturl()
        print(first_page)
    soup = BeautifulSoup(page.data, features="html.parser")
    data = soup.find_all('p')
    return data, first_page


def main():
    first_page = None
    next_link_to_grab = 'https://en.wikipedia.org/wiki/Special:Random'
    philosophy = False
    count = 1
    myfile = open("pages.out.txt", 'w')
    while not philosophy:
        data, first_page = get_html_page_for_parsing(next_link_to_grab, first_page)
        next_link_to_grab = parse_html(data)
        count += 1
        if count > 100:
            print("We could not find the philosphy page after 100 lookups")
            break
        if next_link_to_grab.get('title') == "Philosophy":
            philosophy = "True"
            print("We needed to clickthrough {} links to get to the philosphy page".format(count))
            output = "{},{}".format(first_page, count)
            myfile.write(output)
            myfile.close()
        else:
            time.sleep(2)       # Throttle requests so that wikipedia will not stop serving pages to you
            next_link_to_grab = "https://en.wikipedia.org" + next_link_to_grab.get('href')


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()
links_dict = {}
main()
