"""
create a user definimed number of unique QR codes and export to CSV
"""

import csv
import os

import click
import qrcode
import qrcode.image.svg
import time
from random import randint

def ingest(path, col_name):
    """
    read in existing IDs
    """
    f = open(path, 'rt')
    ids = []

    try:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                ids += [int(row[col_name])]
            except Exception, e:
                print 'could not parse baseline id of: ' + str(row[col_name]) + ' due to ' + str(e)
    finally:
        f.close()

    return ids

def genids(baseids, num):
    """
    return a array with a tuple of associated codes and qr images

    dict contains:
    id | int
    code | QR object
    path | str (initial null)
    """
    factory = qrcode.image.svg.SvgPathImage
    imgs = []
    minr = 100000
    maxr = 999999
#    minr = 1
#    maxr = 10
    print baseids

    for i in xrange(num):
        newid = randint(minr,maxr)
        while newid in baseids:
            print str(newid) + 'is in!'
            newid = randint(minr,maxr)

        newcode = qrcode.make(newid, image_factory=factory)
        baseids += [newid]
        imgs += [{'id' : newid, 'code' : newcode, 'path' : None}]

    if len(baseids) != len(set(baseids)):
        raise Exception('There are duplicates! Freak out! Halting...')

    return imgs

def saveimg(idimg, path):
    """
    save all teh images
    """
    path =  _get_path(path)

    if not os.path.exists(path):
        os.makedirs(path)

    for v in idimg:
        #v[0] = name, v[1] = image
        v['path'] = path
        with open(path + str(v['id']) + '.svg', 'w+') as imgfile:
            v['code'].save(imgfile,'SVG')


def createcsv(idimg, path):
    """
    create a CSV with id and path to images
    """
    f = open(_get_path(path) + 'qrout.csv', 'wt')
    try:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["id","@qr"])
        for v in idimg:
            writer.writerow([v['id'],v['path']])
    finally:
        f.close()

def _get_path(path):
    return os.path.dirname(path) + '/imgs/' + time.strftime("%Y-%m-%d-%H%M") + '/'

@click.command()
@click.option('--path', help='path to CSV')
@click.option('--col_name', help='name of column with existing unique IDs')
@click.option('--num', help='how many unique IDs to generate', type=int)
def run(path, col_name, num):
        baseids = ingest(path, col_name)
        idimg = genids(baseids, num)
        saveimg(idimg, path)
        createcsv(idimg, path)

if __name__ == '__main__':
    run()


