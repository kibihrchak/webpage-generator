def select_menuitem(menu, search_item):
    """Marks menu item as 'selected' and returns modified menu copy."""

    output_menu = list(menu)

    for i, item in enumerate(menu):
        if item["Name"] == search_item:
            output_menu[i] = dict(item)

            output_menu[i]["Selected"] = True
            break

    return output_menu


def parse_menufile(f):
    """Menu file parser.

    Parses file based on description line word positions.
    Marks first and last entry.
    
    """

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
    """Page file parser."""

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


def parse_layouts(f):
    """Layout file parser."""

    header = f.readline()

    name_pos = header.find("Name")
    layout_pos = header.find("Layout")
    head_pos = header.find("Head")

    entries = []

    f.readline() # skip empty line

    # reading entries
    data = f.readline()

    while data != '':
        name = data[name_pos:layout_pos].strip()
        layout = data[layout_pos:head_pos].strip()
        head = data[head_pos:].strip()

        entry = {}

        entry["Name"] = name
        entry["Layout"] = layout
        entry["Head"] = head

        entries.append(entry)

        data = f.readline()

    return entries


if __name__ == "__main__":
    """Template based page generator.

    Arguments:
    1 - source directory
    2 - destination directory
    """

    import glob
    import pystache
    import sys
    import os

    source_dir = sys.argv[1]
    dest_dir = sys.argv[2]
    path_join = os.path.join


    # parse main menu
    with open(path_join(source_dir, "main.menu"), 'r') as f:
        main_menu = parse_menufile(f)

    # load main template
    with open(path_join(source_dir, "main.mustache"), 'r') as f:
        main_template = f.read()

    # parse content layouts
    with open(path_join(source_dir, "layouts"), 'r') as f:
        layouts = parse_layouts(f)

    # pass through all pages
    page_files = glob.glob(path_join(source_dir, "*.page"))


    for filename in page_files:
        # parse page information
        with open(filename, 'r') as f:
            parsed_data = parse_pagefile(f)

        # select main menu entry
        current_main_menu =\
            select_menuitem(main_menu, parsed_data["menu_name"])

        if ("subm_src" in parsed_data): # if submeny exists
            # parse submenu
            with open(path_join(source_dir,\
                    parsed_data["subm_src"]), 'r') as f:
                current_submenu = parse_menufile(f)

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


        # find current layout
        for layout in layouts:
            if parsed_data["layout"] == layout["Name"]:
                # load current layout head and body content
                if layout["Head"] != "":
                    with open(path_join(source_dir,\
                            layout["Head"]), 'r') as f:
                        pystache_hash["head_layout"] = f.read()

                with open(path_join(source_dir,\
                        layout["Layout"]), 'r') as f:
                    pystache_hash["body_layout"] = f.read()
                
                break


        # load additional head data
        if "head_src" in parsed_data:
            with open(path_join(source_dir, parsed_data["head_src"]),\
                    'r') as head_file:
                pystache_hash["head_placeholder"] = head_file.read()

        # do first-pass generation
        first_pass = pystache.render(main_template, pystache_hash)

        # load content files
        pystache_hash = {}

        for i, filename in enumerate(parsed_data["cont_src"]):
            with open(path_join(source_dir, filename), 'r') as cont_file:
                pystache_hash["pl" + str(i)] = cont_file.read().strip()

        # do second-pass generation
        second_pass = pystache.render(first_pass, pystache_hash)

        # write output
        with open(path_join(dest_dir, parsed_data["output"]),\
                'w') as f:
            f.write(second_pass)
