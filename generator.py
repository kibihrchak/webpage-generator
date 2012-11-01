def select_menuitem(menu, search_item):
    output_menu = list(menu)

    for i, item in enumerate(menu):
        if item["Name"] == search_item:
            output_menu[i] = dict(item)

            output_menu[i]["Selected"] = True
            break

    return output_menu


def parse_menufile(f):
    header = f.readline()

    name_pos = header.find("Name")
    text_pos = header.find("Text")
    link_pos = header.find("Link")

    entries = []

    f.readline() # skip empty line

    # reading entries
    data = f.readline()

    while data != '':
        name = data[name_pos:text_pos].strip()
        text = data[text_pos:link_pos].strip()
        link = data[link_pos:].strip()

        entry = {}

        entry["Name"] = name
        entry["Text"] = text
        entry["Link"] = link

        entries.append(entry)

        data = f.readline()

    entries[0]["First"] = True
    entries[-1]["Last"] = True

    return entries


def parse_pagefile(f):
    header = f.readline()

    field_pos = header.find("Field")
    value_pos = header.find("Value")

    fields = {}

    f.readline() # skip empty line

    # reading fields
    data = f.readline()

    while data != '':
        field = data[field_pos:value_pos].strip()
        value = data[value_pos:].strip()

        fields[field] = value

        data = f.readline()

    # some data formatting
    fields['cont_src'] = fields['cont_src'].split(' ')

    return fields


if __name__ == "__main__":
    import glob
    import pystache

    # parse main menu
    with open("main.menu", 'r') as main_menu_file:
        main_menu = parse_menufile(main_menu_file)

    # load main template
    with open("main.mustache", 'r') as f:
        main_template = f.read()

    # pass through all pages
    page_files = glob.glob("*.page")

    for filename in page_files:
        f = open(filename, 'r')

        parsed_data = parse_pagefile(f) # parse page information

        f.close()

        # select main menu entry
        current_main_menu =\
            select_menuitem(main_menu, parsed_data["menu_name"])

        if ("subm_src" in parsed_data): # if submeny exists
            # parse submenu
            subm_file = open(parsed_data["subm_src"], 'r')

            current_submenu = parse_menufile(subm_file)

            subm_file.close()

            # select submenu entry
            current_submenu =\
                select_menuitem(current_submenu, parsed_data["subm_name"])

            parsed_data["subm_using"] = True
        else:
            parsed_data["subm_using"] = False


        # prepare dictionary for first-pass generation
        pystache_hash = parsed_data

        pystache_hash["main_menu"] = current_main_menu

        if pystache_hash["subm_using"] == True:
            pystache_hash["submenu"] = current_submenu

        # load body content layout file
        with open(parsed_data["cont_type"], 'r') as cont_file:
            pystache_hash["body_placeholder"] = cont_file.read()

        if "head_src" in parsed_data:
            with open(parsed_data["head_src"], 'r') as head_file:
                pystache_hash["head_placeholder"] = head_file.read()

        # do first-pass generation
        first_pass = pystache.render(main_template, pystache_hash)

        # load content files
        pystache_hash = {}

        for i, filename in enumerate(parsed_data["cont_src"]):
            with open(filename, 'r') as cont_file:
                pystache_hash["pl" + str(i)] = cont_file.read().strip()

        # do second-pass generation
        second_pass = pystache.render(first_pass, pystache_hash)

        # write output
        with open(parsed_data["output"], 'w') as first_pass_file:
            first_pass_file.write(second_pass)
