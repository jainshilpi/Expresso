#hin_dict = 'rnd_passoptions=2e.pkl.gz'
hin_dict = 'rnd.pkl.gz'

histodict={
    
    ##normal plots
    'normal':{'hsumw':{'sumw':{'label':'sumw','axis':'sumw','file':hin_dict,'stack':False,'scale':1}},
              #plot1
              
              'hcutflow':{'cutflow':{'label':'cutflow','axis':'selection','file':hin_dict,'stack':False}},
              #plot2
              
              'hevents_processed':{'events_processed':{'label':'events_processed','axis':'events_processed','file':hin_dict,'stack':False}},
              #plot3
              
              'hpteta':{'pteta_el0':{'label':'noflip_el0','axis':'pt','file':hin_dict,'stack':True},
                                 'pteta_el1':{'label':'noflip_el1','axis':'pt','file':hin_dict,'stack':True,'scale':1},
                                 'pteta':{'label':'noflip','axis':'pt','file':hin_dict,'stack':False}},
              #plot4
              
              'hpteta_flip':{'pteta_flip_el0':{'label':'flip_el0','axis':'pt','file':hin_dict,'stack':True},
                               'pteta_flip_el1':{'label':'flip_el1','axis':'pt','file':hin_dict,'stack':True},
                               'pteta_flip':{'label':'flip','axis':'pt','file':hin_dict,'stack':False},
                               },
              #plot5

              'hNele':{'Nele':{'label':'Nele','axis':'Nele','file':hin_dict,'stack':False}},
              'hpteta_flip_bins':{'pteta_flip_bins':{'label':'flip_bins','axis':'Flipbins','file':hin_dict,'stack':False}},
              'hpteta_Noflip_bins':{'pteta_Noflip_bins':{'label':'Noflip_bins','axis':'Flipbins','file':hin_dict,'stack':False}},
              },
    'ratio':{
        'hpt_flip':
        {
            'pt_flip_el0':[{'label':'pteta_el0','axis':'pt','file':hin_dict},
                           {'label':'pteta_flip_el0','axis':'pt','file':hin_dict},
                           {'color':'k'}],
            'pt_flip_el1':[{'label':'pteta_el1','axis':'pt','file':hin_dict},
                           {'label':'pteta_flip_el1','axis':'pt','file':hin_dict},
                           {'color':'blue'}],
            'pt_flip':[{'label':'pteta','axis':'pt','file':hin_dict},
                       {'label':'pteta_flip','axis':'pt','file':hin_dict},
                       {'color':'red'}],
        },

        'habseta_flip':
        {
            'abseta_flip_el0':[{'label':'pteta_el0','axis':'abseta','file':hin_dict},
                               {'label':'pteta_flip_el0','axis':'abseta','file':hin_dict},
                               {'color':'k'}],
            
            'abseta_flip_el1':[{'label':'pteta_el1','axis':'abseta','file':hin_dict},
                               {'label':'pteta_flip_el1','axis':'abseta','file':hin_dict},
                               {'color':'blue'}],
            
            'abseta_flip':[{'label':'pteta','axis':'abseta','file':hin_dict},
                           {'label':'pteta_flip','axis':'abseta','file':hin_dict},
                           {'color':'yellow'}],
        },
    
        
        'hflipBins':
        {
            'flipbins_el':[{'label':'pteta_Noflip_bins','axis':'Flipbins','file':hin_dict},
                               {'label':'pteta_flip_bins','axis':'Flipbins','file':hin_dict},
                               {'color':'k'}],

        },
        
    },

    '2Dratio':{
        'hpt_eta':[{'label':'pteta_flip','xaxis':'pt','yaxis':'abseta','file':hin_dict},
                   {'label':'pteta','xaxis':'pt','yaxis':'abseta','file':hin_dict}]
        }
}

