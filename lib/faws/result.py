import lxml.etree
import json

def parse_xml_as_json(root : 'lxml.etree.Element'):
    json = dict()
    for child in root.iterchildren():
        new_value = None
        if child.text and child.text.strip() != '':
            new_value = child.text
        else:
            new_value = parse_xml_as_json(child)
            if len(new_value) == 0:
                new_value = ''
        if child.tag not in json:
            json[child.tag] = new_value
        else:
            if type(json[child.tag]) != list:
                json[child.tag] = [json[child.tag]]
            json[child.tag].append(new_value)
    return json

def prep_response_text(response_text):
    '''
    Prepares the XML response string for lxml
    '''
    # remove any encoding declaration
    encoding_decl_prefix = '<?xml version="1.0" encoding="UTF-8"?>\n'
    if response_text.startswith(encoding_decl_prefix):
        response_text = response_text[len(encoding_decl_prefix):]
    # remove the xmlns declaration. Since lxml doesn't provide a way to get the tag name sans namespace prefix, it just gets in our way
    start = response_text.find(' xmlns="')
    if start >= 0:
        end = response_text.find('"', start+len(' xmlns="'))
        response_text = response_text[:start] + response_text[end+1:]
    return response_text

class AWSResult:

    _tree = None
    _json_full = None
    
    def __init__(self, response_text : str):
        self.response_text = prep_response_text(response_text)
        
    def json_full(self):
        if self._json_full is None:
            self._json_full = parse_xml_as_json(self.tree())
        return self._json_full

    def tree(self):
        '''
        returns response as an lxml.etree.Element
        '''
        if self._tree is None:
            self._tree = lxml.etree.fromstring(self.response_text)
        return self._tree
    
    def xpath(self, path):
        return self.tree().xpath(path)

    def xml(self):
        return self.response_text

    def __getitem__(self, key):
        return self.json()[key]
    
