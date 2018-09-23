#!/usr/bin/env python3

#   Copyright (C) 2018  Monika Kairaityte <monika@kibit.lt>
#
#   This file is part of cppreference-doc
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see http://www.gnu.org/licenses/.

from commands.preprocess_cssless import *
import argparse
import concurrent.futures
import os
import shutil

def main():
    parser = argparse.ArgumentParser(prog='preprocess_qch.py')
    parser.add_argument('--src', required=True, type=str,
            help='Source directory where raw website copy resides')
    parser.add_argument('--dst', required=True, type=str,
            help='Destination folder to put preprocessed archive to')
    parser.add_argument('--verbose', action='store_true', default=False,
            help='If set, verbose output is produced')
    args = parser.parse_args()

    source_root = args.src
    dest_root = args.dst
    verbose = args.verbose

    if os.path.isdir(dest_root):
        shutil.rmtree(dest_root)

    paths_list = []
    for root, dirs, files in os.walk(source_root):
        for file in files:
            if file.endswith(".html"):
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, source_root)
                dst_path = os.path.join(dest_root, rel_path)
                tuple = (src_path, dst_path)
                paths_list.append(tuple)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [ (executor.submit(preprocess_html_merge_cssless,
                                     src_path, dst_path), i)
                    for i, (src_path, dst_path) in enumerate(paths_list) ]

        for future, i in futures:
            print('Processing file: {}/{}: {}'.format(i, len(paths_list),
                                                      paths_list[i][1]))
            output = future.result()
            if verbose:
                print(output)

if __name__ == "__main__":
    main()
