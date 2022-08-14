import math
import copy
import random

class GA:
    def __init__( self, population, key_list ):
        self.element = len( key_list )
        self.population = population
        self.key_list = key_list
        self.parent = []
        self.scores = []
        self.ones = []
        self.best_population = None
        self.best_score = -1
        self.best_one = 0
        self.mutation_rate = 0.05
        self.next_individual_rate = 0.5
        self.ticket_kind = ""

        for i in range( 0, self.population ):
            t = {}
            
            for k in self.key_list:
                t[k] = self.score_create()

            self.parent.append( t )

    def get_best( self ):
        return self.best_population, self.best_score

    def get_parent( self ):
        return self.parent

    def set_ticket_kind( self, kind ):
        self.ticket_kind = kind

    def scores_set( self, score_list, one_list ):
        self.scores = copy.deepcopy( score_list )
        self.ones = copy.deepcopy( one_list )

    def score_create( self ):
        score = random.random()
        score += 0.05
        score *= 10
        score = int( score )
        score /= 10
        return score

    def softmax( self, score_list ):
        result = []
        sum_value = 0

        # 一回正規化する max rangeにひっかかかる
        # scoreは絶対0以上
        sum_value = sum( score_list )

        for i in range( 0, len( score_list ) ):
            if not sum_value == 0:
                result.append( score_list[i] / sum_value )
            else:
                result.append( score_list[i] )

        for i in range( 0, len( result ) ):
            result[i] = math.exp( result[i] )

        sum_value = sum( result )

        for i in range( 0, len( result ) ):
            result[i] /= sum_value

        return result

    def roulette( self, roulette_scores ):
        softmax_scores = self.softmax( roulette_scores )
        result = []
        before = -1
        
        while 1:
            if len( result ) == 2:
                break
            
            get_num = -1
            ru = random.random()
            sum_value = 0

            for i in range( 0, len( softmax_scores ) ):
                sum_value += softmax_scores[i]

                if ru < sum_value:
                    get_num = i
                    break

            if get_num == -1:
                get_num = len( softmax_scores ) - 1

            if not before == get_num:
                result.append( get_num )
                before = get_num   

        return result[0], result[1]

    def random_crossing( self, parent1, parent2 ):
        result = {}
        two_point = []
        before = -1

        for k in self.key_list:
            if random.random() < 0.5:
                result[k] = parent1[k]
            else:
                result[k] = parent2[k]
            
        return result

    def mutation( self, data ):
        for k in data.keys():
            if random.random() < self.mutation_rate:
                data[k] = self.score_create()

        return data        

    def ranking( self, N ):
        rank_list = list( range( 1, N + 1 ) )
        p1, p2 = self.roulette( rank_list )
        p1 = N - p1 - 1
        p2 = N - p2 - 1
        return p1, p2
        
    def next_genetic( self ):
        next_individual = []
        next_check = []

        for i in range( 0, self.population ):
            next_check.append( { "score": self.scores[i], "parent": self.parent[i] } )
            
            if self.best_score < self.scores[i]:
                self.best_one = self.ones[i]
                self.best_score = self.scores[i]
                self.best_population = self.parent[i]

        next_check = sorted( next_check, key=lambda x:x["score"], reverse = True )
        next_elite_count = int( self.population * self.next_individual_rate )
        
        for i in range( 0, next_elite_count ):
            next_individual.append( copy.deepcopy( next_check[i]["parent"] ) )

        while 1:
            if len( next_individual ) == self.population:
                break
            
            point1, point2 = self.ranking( next_elite_count )
            #child = self.two_crossing( self.parent[point1], self.parent[point2] )
            child = self.random_crossing( next_individual[point1], next_individual[point2] )
            child = self.mutation( child )
            next_individual.append( child )

        self.parent = copy.deepcopy( next_individual )
