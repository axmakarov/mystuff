#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import io

def open_with_csv(filename, d=';'):
    data = []
    with io.open(filename, 'r', encoding='utf-8') as csvin:
        csvin = csv.reader(csvin, delimiter=d)

        for row in csvin:
        	data.append (row)
    return data

inp = open_with_csv('D:\\dev-trash\\test.csv')
out = open('D:\\dev-trash\\ouput2.txt', 'w+')

















