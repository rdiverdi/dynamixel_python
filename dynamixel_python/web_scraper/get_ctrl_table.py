import json
import urllib.request
import xml.etree.ElementTree as ET

import pkg_resources

from collections import namedtuple

EEPROM_TABLE_TAG = '<h2 id="control-table-of-eeprom-area">'
RAM_TABLE_TAG = '<h2 id="control-table-of-ram-area">'
TABLE_OPEN = '<table>'
TABLE_CLOSE = '</table>'

HEADER_TAG = 'thead'
BODY_TAG = 'tbody'
ROW_TAG = 'tr'

ATTRIBUTE_HEADER = 'Data Name'


class TableRow:
    def __init__(self):
        pass

class AttributeTable:
    def __init__(self, text):
        self.root = ET.fromstring(text)
        self.header_xml = self.root.find(HEADER_TAG)
        self.rows_xml = self.root.find(BODY_TAG)
        self.header = self._parse_row(self.header_xml.find(ROW_TAG))
        self.index_dict = {self.header[i]: i for i in range(len(self.header))}
        self.rows = []
        for row_xml in self.rows_xml.findall(ROW_TAG):
            row = self._parse_row(row_xml)
            self.rows.append({row[self.index_dict[ATTRIBUTE_HEADER]] : {self.header[i]: row[i] for i in range(len(row))}})


    def _parse_row(self, xml_list):
        ret = []
        for tag in xml_list:
            a = tag.find('a')
            if a is not None:
                ret.append(a.text)
                continue
            em = tag.find('em')
            if em is not None:
                ret.append(em.text)
                continue
            ret.append(tag.text)
            if tag.text is None:
                print(ET.tostring(xml_list))
                print('\n')
        return ret
        

def build_model_json(series, model, base_folder = '.', urlbase='https://emanual.robotis.com/docs/en/dxl/'):
    """ pull the control table for selected dynamixel model from the web page
        and build the json file """
    url = urlbase + series + '/' + model
    full_html = urllib.request.urlopen(url).read().decode('utf-8')
    # find eeprom table
    split1 = full_html[full_html.find(EEPROM_TABLE_TAG):]
    eeprom_table_xml = split1[split1.find(TABLE_OPEN):split1.find(TABLE_CLOSE)] + TABLE_CLOSE
    eeprom_table = AttributeTable(eeprom_table_xml)

    split2 = full_html[full_html.find(RAM_TABLE_TAG):]
    ram_table_xml = split2[split2.find(TABLE_OPEN):split2.find(TABLE_CLOSE)] + TABLE_CLOSE
    ram_table = AttributeTable(ram_table_xml)

    model_dict = {'eeprom': eeprom_table.rows, 'ram': ram_table.rows}
    f = open(base_folder + '/' + model + '.json', 'w')
    json.dump(model_dict, f, indent=2, sort_keys=True)
    f.close()
