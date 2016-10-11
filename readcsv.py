#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
f1 = open('D:\\result.txt', 'w+')
reader = csv.reader(open('D:\\goallist.csv'))
result = []
print >>f1, reader.fieldnames