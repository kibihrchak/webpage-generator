# Python Webpage Generator

## Goal

Goal is to make HTML generator based on provided template and data. It should support two-level menus, as well as custom content container organization. Template generation is based on [Mustache][mustache].


## Inputs

Input for generator are:

-   master template (`main.mustache`)
    
    Contains master template for all pages. It has placeholders for all necessary parts, as well as static data for items that are shared among all the pages.

-   menus (`*.menu` files)
    
    Menus used in the webpages. They are classified as:
    
    -   first-level menu: `main.menu`
    -   second-level menus: all other `.menu` files
    
    Their content is:
    
    -   menu entry name
    -   text that is show in menu
    -   link to `.html` page

-   page informations (`.page` files)
    
    These files contain specifications and some data for separate webpages. Final output (all `.html` files) will be generated in 1-to-1 relation with these files. 
    
    Data provided in page information files is:
    
    -   page title
    -   main menu entry that will be selected when this page is on
    -   *[optional]* which submenu is used
    -   *[optional]* submenu entry that will be selected when page is on
    -   *[optional]* additional data to be inserted in `<head>` tag
    -   layout type
    -   content source file(s)
    -   output file name

-   layout file (`layout`)
    
    This file specifies possible layouts. User will select appropriate layout by writing its name in `layout` field of `.page` file.
    
    Layout data is:
    
    -   its internal name
    -   content layout file (`.layout`) file
    -   additional head data (`.head`) file
    
    Content layout file specifies content placeholders. Placeholders are named as `pl#`, where `#` is increasing number, starting from 0. Content source files are inserted in those placeholders by order they are provided in `.page` file.

-   content files (`.data` files)
    
    Data to be put in content placeholders.

-   header files (`.head` files)
    
    User data that will be inserted in `<head>` tag.


## Used Mustache tags

-   `title`: page title
-   `head_placeholder`: placeholder for additional header data
-   `head_layout`: placeholder for layout head data
-   `main_menu`: start of main menu. Inside tags:
    
    -   `Text`
    -   `Link`
    -   `Selected`
    -   `First`
    -   `Last`

-   `subm_using`: is submenu available
-   `submenu`: start of submenu. Inside tags are same as for `main_menu`
-   `body_layout`: placeholder for body content. Inside it are tags `pl#`, where `#` is a number starting from 0.


[mustache]: http://mustache.github.com/
