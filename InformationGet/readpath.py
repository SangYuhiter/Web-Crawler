# -*- coding: utf-8 -*-
import os


def listfiels(path):
    path = path.replace("\\", "/")
    mlist = os.listdir(path)

    for m in mlist:
        mpath = os.path.join(path, m)
        if os.path.isfile(mpath):
            pt = os.path.abspath(mpath)
            # print pt.decode("gbk").encode("utf-8") #会报错
            print(pt)
        else:
            pt = os.path.abspath(mpath)
            print(pt)
            listfiels(pt)

