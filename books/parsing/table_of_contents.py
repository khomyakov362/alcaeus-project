from lxml import etree as ET

parser = ET.XMLParser(recover=True, encoding='utf-8')


def get_table_of_contents(xml_str: str):

    def el_to_dict(el: ET.ElementBase, path: str) -> dict:
        n = el.attrib.get('n')
        new_path = (path + f'[@n={n}]').replace('][', ' and ')
        return{
        'path': new_path,
        'tag': el.tag, 
        'type': el.attrib.get('type'), 
        'subtype': el.attrib.get('subtype'),
        'n': n,
        }

    def make_parent_dict(el: ET.ElementBase, path: str, child_tag_name: str) -> dict:

        parent_dict = el_to_dict(el, path)
        children = el.findall(f'./{child_tag_name}') 
        child_path = parent_dict['path'] + f'/{child_tag_name}'
        parent_dict['children'] = list(map(lambda el: el_to_dict(el, child_path), children))
        
        return parent_dict

    document = ET.fromstring(bytes(xml_str, encoding='utf-8'), parser=parser)

    NSMAP = document.nsmap
    NAMESPACE = NSMAP.get(None)
    if NAMESPACE:
        N = '{' + NAMESPACE + '}'
    else:
        N = ''

    paths = [
        (f'.//{N}text/{N}body/{N}div1', f'{N}div2'),
        (f'.//{N}text/{N}body/[@type="textpart"]', f'{N}div'),
        (f'.//{N}text/{N}body/{N}div/{N}div[@type="textpart"]', f'{N}div'),
        (f'.//{N}text/{N}body/{N}div', f'{N}div'),
    ]

    for path in paths:

        print(path)
        divs = document.find(path[0])

        if divs is not None and len(divs) > 0:
            return list(map(lambda el: make_parent_dict(el, path[0], path[1]), divs))

    print('Could not retrieve the table of contents.')
    print('Paths tried:')
    for path in paths:
        print(path)
    print(f'Namespaces: {NSMAP}')
