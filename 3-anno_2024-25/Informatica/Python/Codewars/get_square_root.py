def get_square_root(perm):
    n = len(perm)
    visited = [False] * n
    cycles = []
    
    for i in range(n):
        if not visited[i]:
            cycle = []
            cur = i
            while not visited[cur]:
                visited[cur] = True
                cycle.append(cur)
                cur = perm[cur]
            cycles.append(cycle)
    
    odd_cycles = []
    even_cycles = {}
    for cycle in cycles:
        m = len(cycle)
        if m % 2 == 1:
            odd_cycles.append(cycle)
        else:
            even_cycles.setdefault(m, []).append(cycle)
    
    for m, cycle_list in even_cycles.items():
        if len(cycle_list) % 2 != 0:
            return None
    
    square_root_cycles = []
    
    for cycle in odd_cycles:
        m = len(cycle)
        r = (m + 1) // 2
        new_cycle = [cycle[(i * r) % m] for i in range(m)]
        square_root_cycles.append(new_cycle)
    
    for m, cycle_list in even_cycles.items():
        for i in range(0, len(cycle_list), 2):
            A = cycle_list[i]
            B = cycle_list[i+1]
            new_cycle = []
            for j in range(m):
                new_cycle.append(A[j])
                new_cycle.append(B[j])
            square_root_cycles.append(new_cycle)
    
    result = [None] * n
    for cycle in square_root_cycles:
        k = len(cycle)
        for i in range(k):
            result[cycle[i]] = cycle[(i+1) % k]
    
    return result