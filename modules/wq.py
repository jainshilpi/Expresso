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
                #'environment_file': 'my-coffea-env.tar.gz',
                'extra_input_files': ["modules/IHEPProcessor.py"],#,"modules/ExpressoTools.py","modules/ExpressoPlotTools.py","modules/paths.py"],

                'retries': 3,

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

                # this resource values may be omitted when using
                # resources_mode: 'auto', but they do make the initial portion
                # of a workflow run a little bit faster.
                # Rather than using whole workers in the exploratory mode of
                # resources_mode: auto, tasks are forever limited to a maximum
                # of 8GB of mem and disk.
                #
                # NOTE: The very first tasks in the exploratory
                # mode will use the values specified here, so workers need to be at least
                # this large. If left unspecified, tasks will use whole workers in the
                # exploratory mode.
                #'cores': 1,
                #'disk': 8000,   #MB
                # 'memory': 10000, #MB

                # control the size of accumulation tasks. Results are
                # accumulated in groups of size chunks_per_accum, keeping at
                # most chunks_per_accum at the same time in memory per task.
                'chunks_per_accum': 25,
                'chunks_accum_in_mem': 2,

                # terminate workers on which tasks have been running longer than average.
                # This is useful for temporary conditions on worker nodes where a task will
                # be finish faster is ran in another worker.
                # the time limit is computed by multipliying the average runtime of tasks
                # by the value of 'fast_terminate_workers'.  Since some tasks can be
                # legitimately slow, no task can trigger the termination of workers twice.
                #
                # warning: small values (e.g. close to 1) may cause the workflow to misbehave,
                # as most tasks will be terminated.
                #
                # Less than 1 disables it.
                'fast_terminate_workers': 0,
                'wrapper':os.getcwd()+'/wrap.py',
                #'x509_proxy':'/afs/cern.ch/user/a/akapoor/proxy/myx509',
                'verbose': False,
                'print_stdout': False,
            }
        for key in wq.keys():
            self.wq[key]=wq[key]
        
    
    def getwq(self):
        return self.wq

            
                       
                         
                          
                         
