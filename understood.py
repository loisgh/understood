from bs4 import BeautifulSoup
import urllib3
import time

#TODO write out files   (Maybe Tonight, definitely

def parse_html(data, myfile):
    for idx, p in enumerate(data):
        we_should_return = False
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
                        we_should_return = True;
                        break

        if we_should_return:
            print(link)
            links_dict[link] = 1
            output = "<a href={}, title={}>{}</a>\n".format(link.get("href"), link.get("title"), link.get("title"))
            myfile.write(output)
            return link

def get_html_page_for_parsing(in_url):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    http = urllib3.PoolManager()
    page = http.request('GET', in_url)
    # if in_url.endswith("Special:Random"):
    #     first_url = page.geturl()
    #     links_dict[first_url] = 1
    # else:
    #     first_url = None
    soup = BeautifulSoup(page.data, features="html.parser")
    data = soup.find_all('p')
    return (data)

def main():
    next_link_to_grab = 'https://en.wikipedia.org/wiki/Special:Random'
    philosophy = False
    count = 1
    myfile =  open("pages.out.txt", 'w')
    while not philosophy:
        data = get_html_page_for_parsing(next_link_to_grab)
        # if first_url:
        #     myfile.write("<a href={}</a>\n".format(first_url))
        next_link_to_grab = parse_html(data, myfile)
        count += 1
        if count > 100:
            print("We could not find the philosphy age after 100 lookups")
            break
        if next_link_to_grab.get('title') == "Philosophy":
            philosophy = "True"
            print("We needed to clickthrough {} links to get to the philosphy page".format(count))
            myfile.close()
        else:
            time.sleep(2)       #Throttle requests so that wikipedia will not stop serving pages to you
            next_link_to_grab = "https://en.wikipedia.org" + next_link_to_grab.get('href')

links_dict = {}
main()

