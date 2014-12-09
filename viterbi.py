try:
    from IPython import embed
except:
    pass

import sys
import math as Math

class Viterbi(object):
    def __init__(self, hmm):
        self.hmm = hmm
        self.states = hmm.states

    # Returns the most likely state sequence for the given
    # 'output' sequence, i.e., the state sequence of the highest
    # conditional probability given the output sequence, according to
    # the hmm that was provided by the constructor. The returned
    # state sequence should have the same number of elements as the
    # given output sequence

    def _init_backpointer(self, output):
        back_pointer = [{}]
        path = {}

        # Initialize base cases (t == 0)
        for state in self.states:
            back_pointer[0][state] = self.hmm.start_prob(state) * \
                    self.hmm.output_prob(state, output[0])
            path[state] = [state]

        return back_pointer, path

    def most_likely_sequence(self, output):
        lookup_lambda = lambda x: x[0]
        hmm = self.hmm
        states = self.states
        back_pointer, path = self._init_backpointer(output)

        # The cache is warm, use these
        trans_prob = hmm.transitions_probabilities
        output_prob = hmm.output_probabilities

        # Run Viterbi for t > 0
        for t in range(1, len(output)):
            back_pointer.append({})
            newpath = {}

            for state in states:
                state_prob_array = []
                output_p = output_prob[state][output[t]]

                for state_0 in states:
                    state_0_prob = back_pointer[t-1][state_0] * \
                            trans_prob[state_0][state] * \
                            output_p

                    state_prob_array.append((state_0_prob, state_0))

                (prob, max_state) = max(state_prob_array, key = lookup_lambda)
                back_pointer[t][state] = prob
                newpath[state] = path[max_state] + [state]

            # Don't need to remember the old paths
            path = newpath

        n = 0
        # if only one element is observed max is sought in the initialization values
        if len(output) != 1:
            n = t
        (prob, state) = max((back_pointer[n][state], state) for state in self.states)

        return (prob, path[state])
