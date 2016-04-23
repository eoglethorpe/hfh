"""
create a user definimed number of unique QR codes and export to CSV
"""

import csv

import click
import qrcode
import qrcode.image.svg
from random import randint

def ingest(path, col_name):
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


def save(img):
    print img
    with open('/Users/ewanog/code/repos/hfh/utils/' + str(img),'w+') as imgfile:
        img.save(imgfile,'SVG')

def genids(baseids, num):
    """
    return a array with a tuple of associated codes and qr images
    """
    factory = qrcode.image.svg.SvgPathImage
    imgs = []
#    minr = 100000
#    maxr = 999999
    minr = 1
    maxr = 10
    print baseids

    for i in xrange(num):
        newid = randint(minr,maxr)
        while newid in baseids:
            print str(newid) + 'is in!'
            newid = randint(minr,maxr)

        newcodeloc = save(qrcode.make(newid, image_factory=factory))
        imgs += [(newid, newcodeloc)]
        baseids += [newid]

    if len(baseids) != len(set(baseids)):
        raise Exception('There are duplicates! Halting...')

    return imgs


def export(idimg, path):
    pass


@click.command()
@click.option('--path', help='path to CSV')
@click.option('--col_name', help='name of column with existing unique IDs')
@click.option('--num', help='how many unique IDs to generate', type=int)
def run(path, col_name, num):
        baseids = ingest(path, col_name)
        idimg = genids(baseids, num)
        export(idimg, path)

if __name__ == '__main__':
    run()


