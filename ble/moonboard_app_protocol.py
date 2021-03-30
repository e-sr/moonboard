import logging
import string

X_GRID_NAMES = string.ascii_uppercase[0:11]

def position_trans(p):
    """convert led number (strip number) to moonboard grid """
    col= p//18
    row= (p%18) +1
    if col%2==1:
        row=19-row
    return X_GRID_NAMES[col]+str(row)
    
def decode_problem_string(s):
    holds = {'START':[],'MOVES':[],'TOP':[]}
    for h in s.split(','):
        t,p = h[0],position_trans(int(h[1:]))
        if t=='S':
            holds['START'].append(p)
        if t=='P':
            holds['MOVES'].append(p)
        if t=='E':
            holds['TOP'].append(p)
    return holds

class UnstuffSequence():
    """
    hold sequence come separated in parts due to BLE packet size limitation
    this class serves to put different parts together
    """
    START = 'l#'
    STOP= '#'

    def __init__(self,logger=None):
        if logger is None:
            self.logger= logging
        else:
            self.logger=logger
        self.s=''

    def process_bytes(self, ba):
        """ 
        process new incoming bytes and return if new problem is available. 
        handle some error due to multiple connected devices sending simoultaneously.
        """

        s = bytearray.fromhex(ba).decode()
        self.logger.debug("incoming bytes:"+str(s))
        
        if s[:2]==self.START:
            self.logger.debug('START')
            if self.s =='':
                if s[-1]==self.STOP:
                    return s[2:-1]
                else:
                    self.s=s[2:]
            else:
                self.logger.debug('error: alredy started')
                self.s= ''
        elif s[-1]==self.STOP:
            self.logger.debug('STOP')
            if self.s!='':
                ret = self.s+s[:-1]
                self.s=''
                return ret
            else:
                self.logger.debug('error: not started')
                self.s= ''
        else:
            self.s+=s