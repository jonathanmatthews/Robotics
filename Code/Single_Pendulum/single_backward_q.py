'''Start-up algorithm that simply kicks, waits a half period,
    and kicks again.'''
    
from utility_functions import last_maxima
import pickle


class BackwardQ():
    def __init__(self, values, all_data, **kwargs):
        print 'Startup script'
        self.period = kwargs.get('period', 0.005)
        self.start_time = values['time']
        self.duration = kwargs.get('duration', float('inf'))
        self.max_angle = kwargs.get('max_angle', 5)
        self.wait_time = 1.253   # defined by the half period of a swing
        self.last_move = 0      # time last kick was performed
        self.first_kick = True  # used to check if it is first kick
        #self.pkl_file = open('Q_table.p', 'rb')
        self.pkl_file = open('Q_rot_prot2.p', 'rb')
        self.data1 = pickle.load(self.pkl_file)
        print self.data1
    
    def get_state(self, x_pos, x_vel):
        #states=[0,1,2,3]
        if(x_pos<=0):
            if(x_vel<0):
                state=0
            elif(x_vel>=0):
                state=1
        elif(x_pos>0):
            if(x_vel>0):
                state=2
            elif(x_vel<=0):
                state=3
        return state
    #def get_state(self, x_pos, x_vel):
        ##states=[0,1,2,3]
        #if(x_pos>=0):
            #if(x_vel>=0):
                #state=0
            #elif(x_vel<0):
                #state=1
        #elif(x_pos<0):
            #if(x_vel<=0):
                #state=2
            #elif(x_vel>0):
                #state=3
        #return state
  

        

    def algo(self, values, all_data):
        t = values['time'] - self.start_time  # renames current time to t
        print 'Time: {:.2f}'.format(values['time']), 'Big encoder: {:.2f}'.format(values['be'])
        
        state = self.get_state(-values['be'], -values['av'])
        best_action = self.data1[state].index(max(self.data1[state]))
        
        if best_action == 1:
            return "extended"
        elif best_action == 0:
            return "seated"
