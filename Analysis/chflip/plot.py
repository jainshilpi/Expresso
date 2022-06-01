#################################################################################################
hin_dict = './Analysis/chflip/output/results.pkl.gz'

histodict={
    
    'cutflow':{'cutflow':{'label':'cutflow','axis':'selection','file':hin_dict,'stack':False}
               },
    'events_processed':{'events_processed':{'label':'events_processed','axis':'events_processed','file':hin_dict,'stack':False}
               },
    'ptabseta_noflip':{'ptabseta_noflip_el0':{'label':'ptabseta_noflip_el0','axis':'pt','file':hin_dict,'stack':True},
                       'ptabseta_noflip_el1':{'label':'ptabseta_noflip_el1','axis':'pt','file':hin_dict,'stack':True},
                       'ptabseta_noflip':{'label':'ptabseta_noflip','axis':'pt','file':hin_dict,'stack':False},
                      },
    'ptabseta_flip':{'ptabseta_flip_el0':{'label':'ptabseta_flip_el0','axis':'pt','file':hin_dict,'stack':True},
                     'ptabseta_flip_el1':{'label':'ptabseta_flip_el1','axis':'pt','file':hin_dict,'stack':True},
                     'ptabseta_flip':{'label':'ptabseta_flip','axis':'pt','file':hin_dict,'stack':False},
                     },
}
