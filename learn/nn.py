import numpy as np
import math
import random
from torch import nn, optim, cuda
import torch.nn.functional as F
import torch

from tqdm import tqdm

import sekitoba_data_manage as dm
import sekitoba_library as lib

class MoneyNN( nn.Module ):
    def __init__( self, n ):
        super( MoneyNN, self ).__init__()
        self.l1 = nn.Linear( n, n )
        self.l2 = nn.Linear( n, n )
        self.l3 = nn.Linear( n, n )
        self.l4 = nn.Linear( n, n )
        self.l5 = nn.Linear( n, n )
        self.l6 = nn.Linear( n, n )
        self.l7 = nn.Linear( n, n )
        self.l8 = nn.Linear( n, n )
        self.l9 = nn.Linear( n, n )
        self.l10 = nn.Linear( n, n )
        self.l11 = nn.Linear( n, n )
        self.l12 = nn.Linear( n, n )
        self.l13 = nn.Linear( n, n )
        self.l14 = nn.Linear( n, n )
        self.l15 = nn.Linear( n, n )
        self.l16 = nn.Linear( n, n )
        self.l17 = nn.Linear( n, n )
        self.l18 = nn.Linear( n, n )
        self.l30 = nn.Linear( n, 2 )
        
        self.b1 = nn.BatchNorm1d( n )
        self.b2 = nn.BatchNorm1d( n )
        self.b3 = nn.BatchNorm1d( n )
        self.b4 = nn.BatchNorm1d( n )
        self.b5 = nn.BatchNorm1d( n )
        self.b6 = nn.BatchNorm1d( n )
        self.b7 = nn.BatchNorm1d( n )
        self.b8 = nn.BatchNorm1d( n )
        self.b9 = nn.BatchNorm1d( n )
        self.b10 = nn.BatchNorm1d( n )
        self.b11 = nn.BatchNorm1d( n )
        self.b12 = nn.BatchNorm1d( n )
        self.b13 = nn.BatchNorm1d( n )
        self.b14 = nn.BatchNorm1d( n )
        self.b15 = nn.BatchNorm1d( n )
        self.b16 = nn.BatchNorm1d( n )
        self.b17 = nn.BatchNorm1d( n )
            
    def forward( self, x ):
        h1 = torch.tanh( self.l1( x ) )
        h2 = torch.tanh( self.b1( self.l2( h1 ) ) )
        h3 = torch.tanh( self.b2( self.l3( h2 ) ) )
        h4 = torch.tanh( self.b3( self.l4( h3 + h2 ) ) )
        h5 = torch.tanh( self.b4( self.l5( h4 ) ) )
        h6 = torch.tanh( self.b5( self.l6( h5 + h4 ) ) )
        h7 = torch.tanh( self.b6( self.l7( h6 ) ) )
        h8 = torch.tanh( self.b7( self.l8( h7 + h6 ) ) )
        h9 = torch.tanh( self.b8( self.l9( h8 ) ) )
        #h10 = F.relu( self.b9( self.l10( h9 + h8 ) ) )
        #h11 = F.relu( self.b10( self.l11( h10 ) ) )
        #h12 = F.relu( self.b11( self.l12( h11 + h10 ) ) )
        #h13 = F.relu( self.b12( self.l13( h12 ) ) )
        #h14 = F.relu( self.b13( self.l14( h13 + h12 ) ) )
        #h15 = F.relu( self.b14( self.l15( h14 ) ) )
        #h16 = F.relu( self.b15( self.l16( h15 + h14 ) ) )
        #h17 = F.relu( self.b16( self.l17( h16 ) ) )
        #h18 = F.relu( self.b17( self.l18( h17 + h16 ) ) )
        h30 = self.l30( h9 )
        return torch.tanh( h30 )
