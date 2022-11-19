import numpy as np
class hcoll:

    def __init__(self, h, isData, xsec, sow, doweight, **conf):
        self.h = h
        self.conf = conf
        self.isData = isData
        self.xsec = xsec
        self.sow = sow
        self.doweight=doweight

    def fill(self, name, weights, mask, obj, cat={}, flatten=False, **axes):
        fullhist = {}
        #print('----------########---')
        for ini, axis in enumerate(axes.keys()):
            arrr = eval(f"obj.{axes[axis]}[mask]")
            if flatten:
                if ini==0:
                    fullhist[axis],weights = ak.flatten(ak.zip(arrr,weights))
                    weights=weights[ak.flatten(mask)]
                else:
                    fullhist[axis] = ak.flatten(arrr)
            else:
                if ini==0:
                    weights=weights[mask]
                fullhist[axis] = arrr
        if self.doweight:
            self.h[name].fill(weight=weights, **cat, **fullhist, **self.conf)
        else:
            self.h[name].fill(**cat, **fullhist, **self.conf)

    def get(self):
        return self.h

def binning(a,b,c):
    return list(np.arange(a,b+c,c))
