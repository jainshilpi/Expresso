from asyncio import events


def preprocess(sample,events,AttachSF=False):
    import modules.ExpressoTools as ET
    import awkward as ak
    import numpy as np
    ###################################
    dataset,isData,histAxisName,year,xsec,sow, nEvents=ET.getInfo(events,sample)
    events['nEvents']=nEvents
    ################################### Start writing your preprocessor below -> for creating new branches on top of the ones already present in the NanoAOD
    ## some variables are auto available picked up from the sample json
    ## The isData variable is true or false depending on if you are operating on data or mc
    ## The xsec has the xsec value, sow has sum of gen weights
    ## histAxisName is the name of the sample from json (will be used as legends for plots)
    
    
    isgentau=abs(events.GenPart.pdgId)==15 # example of creating a mask -> a jagged boolean
    events["GenTaus"]=events.GenPart[isgentau] # like creating a new branch -> this branch is later available

    #let's look at another example
    isgenmu=abs(events.GenPart.pdgId)==13
    events["GenMuons"]=events.GenPart[isgenmu]

    isgenele=abs(events.GenPart.pdgId)==11
    events["GenEles"]=events.GenPart[isgenele]

    

    ################################### Keep the return line as is
    return events,dataset,isData,histAxisName,year,xsec,sow
