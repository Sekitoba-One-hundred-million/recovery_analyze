import math
import random

class GA:
    def __init__( self, population, key_list ):
        self.element = len( key_list )
        self.population = population
        self.key_list = key_list
        self.parent = []
        self.scores = []
        self.best_population = None
        self.best_score = -1
        self.mutation_rate = 0.05

        for i in range( 0, self.population ):
            t = {}
            
            for k in self.key_list:
                t[k] = self.score_create()

            self.parent.append( t )

    def get_best( self ):
        return self.best_population, self.best_score

    def get_parent( self ):
        return self.parent

    def scores_set( self, scores ):
        self.scores = scores

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
        max_value = max( score_list )

        for i in range( 0, len( score_list ) ):
            sum_value += score_list[i]

        for i in range( 0, len( score_list ) ):
            result.append( score_list[i] / sum_value )

        return result

    def roulette( self ):
        softmax_scores = self.softmax( self.scores )
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

    def two_crossing( self, parent1, parent2 ):
        result = {}
        two_point = []
        before = -1

        while 1:
            if len( two_point ) == 2:
                break
            
            p = random.randint( 1, self.element - 2 )

            if not before == p:
                before = p
                two_point.append( p )

        min_point = min( two_point )
        max_point = max( two_point )

        for k in self.key_list[0:min_point]:
            result[k] = parent1[k]

        for k in self.key_list[min_point:max_point]:
            result[k] = parent2[k]

        for k in self.key_list[max_point:self.element]:
            result[k] = parent1[k]
            
        return result

    def mutation( self, data ):
        for k in data.keys():
            if random.random() < self.mutation_rate:
                data[k] = self.score_create()

        return data        
        
    def next_genetic( self ):
        result = []

        for i in range( 0, self.population ):
            if self.best_score < self.scores[i]:
                self.best_score = self.scores[i]
                self.best_population = self.parent[i]

        for i in range( 0, self.population ):
            point1, point2 = self.roulette()
            child = self.two_crossing( self.parent[point1], self.parent[point2] )
            child = self.mutation( child )
            result.append( child )

        self.parent = result
