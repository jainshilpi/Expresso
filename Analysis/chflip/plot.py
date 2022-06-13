hin_dict = 'analysis/results.pkl.gz'

histodict={
    
    ##normal plots
    'normal':{'sumw':{'sumw':{'label':'sumw','axis':'sumw','file':hin_dict,'stack':False,'scale':1}},
              #plot1
              
              'cutflow':{'cutflow':{'label':'cutflow','axis':'selection','file':hin_dict,'stack':False}},
              #plot2
              
              'events_processed':{'events_processed':{'label':'events_processed','axis':'events_processed','file':hin_dict,'stack':False}},
              #plot3
              
              'ptabseta_noflip':{'ptabseta_noflip_el0':{'label':'ptabseta_noflip_el0','axis':'pt','file':hin_dict,'stack':True},
                                 'ptabseta_noflip_el1':{'label':'ptabseta_noflip_el1','axis':'pt','file':hin_dict,'stack':True,'scale':1},
                                 'ptabseta_noflip':{'label':'ptabseta_noflip','axis':'pt','file':hin_dict,'stack':False}},
              #plot4
              
              'ptabseta_flip':{'ptabseta_flip_el0':{'label':'ptabseta_flip_el0','axis':'pt','file':hin_dict,'stack':True},
                               'ptabseta_flip_el1':{'label':'ptabseta_flip_el1','axis':'pt','file':hin_dict,'stack':True},
                               'ptabseta_flip':{'label':'ptabseta_flip','axis':'pt','file':hin_dict,'stack':False},
                               },
              #plot5

              'Nele':{'Nele':{'label':'Nele','axis':'Nele','file':hin_dict,'stack':False}},
              },
    'ratio':{
        'pt_noflip':
        {
            'pt_noflip_el0':[{'label':'ptabseta_noflip_el0','axis':'pt','file':hin_dict},
                             {'label':'ptabseta_flip_el0','axis':'pt','file':hin_dict},
                             {'color':'k'}],
            'pt_noflip_el1':[{'label':'ptabseta_noflip_el1','axis':'pt','file':hin_dict},
                             {'label':'ptabseta_flip_el1','axis':'pt','file':hin_dict},
                             {'color':'blue'}],
            'pt_noflip':[{'label':'ptabseta_noflip','axis':'pt','file':hin_dict},
                         {'label':'ptabseta_flip','axis':'pt','file':hin_dict},
                         {'color':'red'}],
        },

        'abseta_noflip':
        {
            'abseta_noflip_el0':[{'label':'ptabseta_noflip_el0','axis':'abseta','file':hin_dict},
                                 {'label':'ptabseta_flip_el0','axis':'abseta','file':hin_dict},
                                 {'color':'k'}],
            
            'abseta_noflip_el1':[{'label':'ptabseta_noflip_el1','axis':'abseta','file':hin_dict},
                                 {'label':'ptabseta_flip_el1','axis':'abseta','file':hin_dict},
                                 {'color':'blue'}],
            
            'abseta_noflip':[{'label':'ptabseta_noflip','axis':'abseta','file':hin_dict},
                             {'label':'ptabseta_flip','axis':'abseta','file':hin_dict},
                             {'color':'yellow'}]
        }
        },
    '2Dratio':{
        'pt_eta':[{'label':'ptabseta_flip','xaxis':'pt','yaxis':'abseta','file':hin_dict},
                  {'label':'ptabseta_noflip','xaxis':'pt','yaxis':'abseta','file':hin_dict}]
        }

}
