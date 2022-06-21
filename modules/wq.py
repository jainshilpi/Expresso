import os

class WQ:
    
    def __init__(self,wq):
        self.wq={
                'master_name': '{}-wq-coffea'.format(os.environ['USER']),
                # find a port to run work queue in this range:
                'port': 9123,
                'debug_log': 'debug.log',
                'transactions_log': 'tr.log',
                'stats_log': 'stats.log',
                'extra_input_files': ["modules/IHEPProcessor.py"],
                'retries': 5,
                # use mid-range compression for chunks results. 9 is the default for work
                # queue in coffea. Valid values are 0 (minimum compression, less memory
                # usage) to 16 (maximum compression, more memory usage).
                'compression': 9,
                # automatically find an adequate resource allocation for tasks.
                # tasks are first tried using the maximum resources seen of previously ran
                # tasks. on resource exhaustion, they are retried with the maximum resource
                # values, if specified below. if a maximum is not specified, the task waits
                # forever until a larger worker connects.
                'resource_monitor': True,
                'resources_mode': 'auto',
                # NOTE: The very first tasks in the exploratory
                # mode will use the values specified here, so workers need to be at least
                # this large. If left unspecified, tasks will use whole workers in the
                # exploratory mode.
                #'cores': 1,
                #'disk': 8000,   #MB
                #'memory': 10000, #MB
                'chunks_per_accum': 25,
                'chunks_accum_in_mem': 2,
                'fast_terminate_workers': 0,
                'wrapper':'/publicfs/cms/user/kapoor/2022/Expresso/wrap.sh',
                'verbose': False,
                'print_stdout': False,
            }
        for key in wq.keys():
            self.wq[key]=wq[key]
        
    
    def getwq(self):
        return self.wq

            
                       
                         
                          
                         
