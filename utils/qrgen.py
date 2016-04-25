"""
create a user definimed number of unique QR codes and export to CSV
"""

import csv
import os
from itertools import groupby
from random import randint

import click
import qrcode
import qrcode.image.svg
import time


def ingest(path, vdc_name, id_name):
    """
    read in existing IDs, return a tuple of (VDC, id)
    """
    f = open(path, 'rt')
    ids = []

    try:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                ids += [(int(row[vdc_name]), int(row[id_name]))]
            except Exception, e:
                print 'could not parse baseline id of: ' + str(row[col_name]) + ' due to ' + str(e)
    finally:
        f.close()

    return ids


def find_max_vdc(baseids):
    """
    return a list of tuples with VDC id, max id value
    """
    maxs = []

    for key, group in groupby(baseids, lambda x: x[0]):
        max = 0
        for v in group:
            if v[1] > max:
                max = v[1]

        maxs+=[(key,max)]

    return maxs

def genids(baseids, num, vdcs_add):
    """
    return a array with a tuple of associated codes and qr images

    dict contains:
    id | int]
    vdc | int
    code | QR object
    path | str (initial null)
    """

    #a list of tuples containing (VDC id, max id value)
    vdcs_max = find_max_vdc(baseids)

    factory = qrcode.image.svg.SvgPathImage
    imgs = []

    for v in vdcs_add:
        try:
            #get the tuple value of max id form array if it exists
            newid = vdcs_max[[i[0]for i in vdcs_max].index(v)][1] + 1
        except:
            newid = 1

        for i in xrange(newid, newid+num):
            id_mrg = str(v) + '-' + str(newid)
            newcode = qrcode.make(id_mrg, image_factory=factory)

            baseids += [(v,newid)]
            imgs += [{'id_mrg' : id_mrg, 'id' : newid, 'vdc' : v, 'code' : newcode, 'path' : None}]
            newid+=1


    if len(baseids) != len(set(baseids)):
        raise Exception('There are duplicates! Freak out! Halting...')

    return imgs

def saveimg(idimg, path):
    """
    save all teh images
    """
    path = _get_path(path)

    if not os.path.exists(path):
        os.makedirs(path)

    for v in idimg:
        #v[0] = name, v[1] = image
        v['path'] = path
        with open(path + str(v['id_mrg']) + '.svg', 'w+') as imgfile:
            v['code'].save(imgfile,'SVG')


def createcsv(idimg, path):
    """
    create a CSV with id and path to images
    """
    f = open(_get_path(path) + 'qrout.csv', 'wt')
    try:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["id_merge","@qr","vdc","id"])
        for v in idimg:
            writer.writerow([v['id_mrg'],v['path'],v['vdc'],v['id']])
    finally:
        f.close()

def _get_path(path):
    return os.path.dirname(path) + '/imgs/' + time.strftime("%Y-%m-%d-%H%M") + '/'

@click.command()
@click.option('--path', help='path to CSV')
@click.option('--id_col_name', help='name of column with existing unique IDs')
@click.option('--vdc_col_name', help='name of column with existing VDC IDs')
@click.option('--num', help='how many unique IDs to generate', type=int)
@click.option('--vdcs', help='comma delimited list of vdcs in which work will take place')
def run(path, vdc_col_name, id_col_name, num, vdcs):
        baseids = ingest(path, vdc_col_name, id_col_name)
        idimg = genids(baseids, num, [int(i) for i in vdcs.split(',')])
        saveimg(idimg, path)
        createcsv(idimg, path)

if __name__ == '__main__':
    run()


