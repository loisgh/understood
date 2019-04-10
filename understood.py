from bs4 import BeautifulSoup
import urllib3
import time
import operator


def parse_html(data, links_dict):
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
                    elif "#" in link.get('href'):
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
            return links_dict, the_link


def get_html_page_for_parsing(in_url, first_page):
    page = http.request('GET', in_url)
    if not first_page:
        first_page = page.geturl()
        print(first_page)
    soup = BeautifulSoup(page.data, features="html.parser")
    data = soup.find_all('p')
    return data, first_page


def main():
    random_links = {}
    random_pages_chosen = 1
    count = 1
    while random_pages_chosen < 4:
        first_page = None
        next_link_to_grab = 'https://en.wikipedia.org/wiki/Special:Random'
        philosophy = False
        links_dict = {}
        while not philosophy:
            data, first_page = get_html_page_for_parsing(next_link_to_grab, first_page)
            links_dict, next_link_to_grab = parse_html(data, links_dict)
            count += 1
            if count > 100:
                print("We could not find the philosphy page after 100 lookups")
                break
            if next_link_to_grab.get('title') == "Philosophy":
                philosophy = "True"
                print("We needed to clickthrough {} links to get to the philosphy page".format(count))
                random_links[first_page] = count
            else:
                time.sleep(2)       # Throttle requests so that wikipedia will not stop serving pages to you
                next_link_to_grab = "https://en.wikipedia.org" + next_link_to_grab.get('href')
        random_pages_chosen += 1
    sorted_pages = sorted(random_links.items(), key=operator.itemgetter(1))
    myfile = open("pages.out.txt", 'w')
    for info in sorted_pages:
        output = "{},{}\n".format(info[1], info[0])
        myfile.write(output)
    myfile.close()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()
main()
