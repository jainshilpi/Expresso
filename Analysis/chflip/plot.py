hin_dict = 'analysis2/results.pkl.gz'

histodict={
    
    ##normal plots
    'normal':{'hsumw':{'sumw':{'label':'sumw','axis':'sumw','file':hin_dict,'stack':False,'scale':1}},
              #plot1
              
              'hcutflow':{'cutflow':{'label':'cutflow','axis':'selection','file':hin_dict,'stack':False}},
              #plot2
              
              'hevents_processed':{'events_processed':{'label':'events_processed','axis':'events_processed','file':hin_dict,'stack':False}},
              #plot3
              
              'hptabseta':{'ptabseta_el0':{'label':'ptabseta_noflip_el0','axis':'pt','file':hin_dict,'stack':True},
                                 'ptabseta_el1':{'label':'ptabseta_noflip_el1','axis':'pt','file':hin_dict,'stack':True,'scale':1},
                                 'ptabseta':{'label':'ptabseta_noflip','axis':'pt','file':hin_dict,'stack':False}},
              #plot4
              
              'hptabseta_flip':{'ptabseta_flip_el0':{'label':'ptabseta_flip_el0','axis':'pt','file':hin_dict,'stack':True},
                               'ptabseta_flip_el1':{'label':'ptabseta_flip_el1','axis':'pt','file':hin_dict,'stack':True},
                               'ptabseta_flip':{'label':'ptabseta_flip','axis':'pt','file':hin_dict,'stack':False},
                               },
              #plot5

              'hNele':{'Nele':{'label':'Nele','axis':'Nele','file':hin_dict,'stack':False}},
              'hptabseta_flip_bins':{'ptabseta_flip_bins':{'label':'ptabseta_flip_bins','axis':'Flipbins','file':hin_dict,'stack':False}},
              'hptabseta_Noflip_bins':{'ptabseta_Noflip_bins':{'label':'ptabseta_Noflip_bins','axis':'Flipbins','file':hin_dict,'stack':False}},
              },
    'ratio':{
        'hpt_flip':
        {
            'pt_flip_el0':[{'label':'ptabseta_el0','axis':'pt','file':hin_dict},
                           {'label':'ptabseta_flip_el0','axis':'pt','file':hin_dict},
                           {'color':'k'}],
            'pt_flip_el1':[{'label':'ptabseta_el1','axis':'pt','file':hin_dict},
                           {'label':'ptabseta_flip_el1','axis':'pt','file':hin_dict},
                           {'color':'blue'}],
            'pt_flip':[{'label':'ptabseta','axis':'pt','file':hin_dict},
                       {'label':'ptabseta_flip','axis':'pt','file':hin_dict},
                       {'color':'red'}],
        },

        'habseta_flip':
        {
            'abseta_flip_el0':[{'label':'ptabseta_el0','axis':'abseta','file':hin_dict},
                               {'label':'ptabseta_flip_el0','axis':'abseta','file':hin_dict},
                               {'color':'k'}],
            
            'abseta_flip_el1':[{'label':'ptabseta_el1','axis':'abseta','file':hin_dict},
                               {'label':'ptabseta_flip_el1','axis':'abseta','file':hin_dict},
                               {'color':'blue'}],
            
            'abseta_flip':[{'label':'ptabseta','axis':'abseta','file':hin_dict},
                           {'label':'ptabseta_flip','axis':'abseta','file':hin_dict},
                           {'color':'yellow'}],
        },
    
        
        'hflipBins':
        {
            'flipbins_el':[{'label':'ptabseta_Noflip_bins','axis':'Flipbins','file':hin_dict},
                               {'label':'ptabseta_flip_bins','axis':'Flipbins','file':hin_dict},
                               {'color':'k'}],

        },
        
    },

    '2Dratio':{
        'hpt_eta':[{'label':'ptabseta_flip','xaxis':'pt','yaxis':'abseta','file':hin_dict},
                   {'label':'ptabseta','xaxis':'pt','yaxis':'abseta','file':hin_dict}]
        }

}
