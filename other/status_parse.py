def get_state(param, states):
    params = ('OUTPUT', 'VIN', 'VOUT', 'COUT', 'CONSTANT', 'ACK')

    if not list(filter(lambda p: p == param, params)):
        return
        
    if not ':' in param:
        param = param + ':'

    for state in states:
        if param in state:
            try:
                if (param == 'ACK:'):
                    return states[0]
                return state[1]
            except: # States is broken
                return 
    return


status_list = ['OUTPUT: OFF', 'VIN:  39.014 6010', 'VOUT: 3.212 0687', 'COUT: 0.000 0377', 'CONSTANT: CURRENT', 'OK']
print(status_list)

states = list(map(lambda s: s.split(), status_list))
print(states)

output = get_state('VIN', states)
if output:
    print(output)