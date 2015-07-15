#!/usr/bin/env python
# -*- coding: UTF-8 -*-


def to_24(string):
    hour, minute, trail = string.split('.')
    sec, period = trail.split(' ')

    hour = int(hour)
    minute = int(minute)
    sec = int(sec)

    is_pm = period.lower() == "pm"

    if hour == 12:
        if not is_pm:
            hour += 12
    elif is_pm:
        hour += 12

    return "%s.%s.%s" % (
        str(hour).zfill(2),
        str(minute).zfill(2),
        str(sec).zfill(2),
    )


if __name__ == '__main__':
    from folder_list import FolderList

    root = FolderList("/Users/Saevon/Pictures/Screenshots/Witch's House/")
    for file in root:
        # Check if the file's been renamed already
        if "PM" not in file.name or "AM" not in file.name:
            continue

        # Convert to the new format
        prefix, time = file.name.split(' at ')
        suffix = to_24(time)
        new_name = '%s at %s' % (prefix, suffix)

        file.rename(new_name)

    # print to_24("12.05.20 PM")
    # print to_24("12.05.20 AM")
    # print to_24("1.05.20 AM")
    # print to_24("1.05.20 PM")
