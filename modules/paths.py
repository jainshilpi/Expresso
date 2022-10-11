import os
import modules
pjoin = os.path.join

def IHEP_path(path):
    return pjoin(modules.__path__[0], path)

def golden_json_path(year):
    gjpath={
        "2016":IHEP_path("data/goldenJsons/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt"),
        "2016APV":IHEP_path("data/goldenJsons/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt"),
        "2017":IHEP_path("data/goldenJsons/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt"),
        "2018":IHEP_path("data/goldenJsons/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt")
    }
    if year=="2016" or year=="2017" or year=="2016APV" or year=="2018":
        gjyearpath=gjpath[year]
    else:
        raise ValueError(f"Error: Unknown year \"{year}\".")
    return gjyearpath
