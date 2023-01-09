import math 

class Robot:

    '''
    This Class will perform robot's final position and will calculate its distance from 
    position zero (0,0).

    __init__(self)
    final_destination
    finalPosition(self, moves):
    main(self)
    '''
    def __init__(self) -> None:

        '''
        Initialize the first position of the Robot
        '''
        self.p = (0,0)

    def final_destination(self):

        '''
        This function returns the position of the Robot from its original position (0,0)
        '''
        return math.sqrt( ((self.p[0])**2)+((self.p[1])**2) )

    def finalPosition(self, moves: list):

        '''
        Finds the final position of the Robot based on a list of instructions

        Parameters
        ----------
        moves (list)
            Instructions as a list which starts with BEGIN and when first “STOP” instruction 
            is given, it calculates the distance of Robot from the original position (0,0).
            Example of the instruction list could be like: 
            ['BEGIN','LEFT 2','UP 3','STOP']
            The first word indicates direction and the number shows steps.
        '''

        try:
            for move in moves:
                if (move == 'BEGIN'):
                    self.p = (0,0)
        
                elif('LEFT' in move):
                    n = int(move[4:])
                    self.p = (self.p[0]-n,self.p[1])
        
                elif('RIGHT' in move):
                    n = int(move[5:])
                    self.p = (self.p[0]+n,self.p[1])
                
                elif('DOWN' in move):
                    n = int(move[4:])
                    self.p = (self.p[0],self.p[1]-n)

                elif('UP' in move):
                    n = int(move[2:])
                    self.p = (self.p[0],self.p[1]+n)

                elif(move == 'STOP'):
                    print(f' The final position of Ropot is {self.p} and the distance from its original position (0,0) is {self.final_destination()}')
                    break

                else:
                    raise ValueError('Unknown instruction is detected!! Please check your instruction inputs')

        except TypeError:
            print('Wrong format!! Please check your instruction inputs')

    def main(self):

        instructions = ['BEGIN','LEFT 2','UP 7','LEFT 4','DOWN 3','RIGHT 3','STOP']
        self.finalPosition(instructions)

if __name__ == '__main__':
    rob = Robot() 
    rob.main()