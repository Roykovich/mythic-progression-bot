def get_lowest_ilvl(items):
    items_list = items.items()
    items_list = [(item, ilvl['item_level']) for item, ilvl in items_list]
    lowest_ilvl = items_list[0][1]

    for item in items_list[1:]:
        if item[0] == 'shirt' or item[0] == 'tabard':
            continue

        if item[1] < lowest_ilvl:
            lowest_ilvl = item[1]
    
    return lowest_ilvl


