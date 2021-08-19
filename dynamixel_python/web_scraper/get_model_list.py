import urllib.request
import xml.etree.ElementTree as ET

OPEN_TAG = '<table>'
CLOSE_TAG = '</table>'

HREF_OPEN = 'href="'

def get_model_list(url):
    full_html = urllib.request.urlopen(url).read().decode('utf-8')

    model_list = []

    start = full_html.find(OPEN_TAG)
    while start > 0:
        end = full_html.find(CLOSE_TAG)
        this_series = full_html[start:end]

        href_start = this_series.find(HREF_OPEN)
        while href_start>0:
            this_series = this_series[href_start+len(HREF_OPEN):]
            url = this_series[:this_series.find('"')]
            this_series = this_series[len(HREF_OPEN):]
            href_start = this_series.find(HREF_OPEN)
            if url[0] == '#':
                print(b'not using '+ url)
                continue
            model_list.append(tuple(url.split('/')[-3:-1]))


        full_html = full_html[end+len(CLOSE_TAG):]
        start = full_html.find(OPEN_TAG)
    return model_list

if __name__ == '__main__':
    url = 'https://emanual.robotis.com/docs/en/dxl/'
    print(get_model_list(url))

