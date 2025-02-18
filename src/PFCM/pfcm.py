from docplex.mp.model import Model
import time
import psutil
import os

def ler_grafo(arquivo):
    with open(arquivo, 'r') as f:
        linhas = f.readlines()
    n_vertices, n_arestas = map(int, linhas[0].strip().split())
    arestas = []
    for linha in linhas[1:]:
        u, v, c, l = map(int, linha.strip().split())
        arestas.append((u, v, c, l))  
    return n_vertices, n_arestas, arestas

arquivo_grafo = os.path.join(os.path.dirname(__file__), 'in.txt')
n_vertices, n_arestas, arestas = ler_grafo(arquivo_grafo)
mdl = Model(name="Fluxo_Custo_Minimo")
fluxo = {(u, v): mdl.continuous_var(lb=0, name=f"x_{u}_{v}") for (u, v, c, l) in arestas}

# Função objetivo: Minimizar o custo total
mdl.minimize(mdl.sum(fluxo[u, v] * c for (u, v, c, l) in arestas))

# Nós de oferta, demanda e transbordo
oferta = {1: 10, 2: 10, 3: 10}
demanda = {4: -8, 7: -7, 8: -6, 9: -9}
transbordo = {5: 0, 6: 0}

# Restrições de oferta
todos_os_nos = set(range(1, n_vertices + 1))
for i in oferta:
    mdl.add_constraint(mdl.sum(fluxo[u, v] for (u, v, c, l) in arestas if u == i) -
                       mdl.sum(fluxo[v, u] for (v, u, c, l) in arestas if u == i) <= oferta[i])

# Restrições de demanda
for i in demanda:
    mdl.add_constraint(mdl.sum(fluxo[u, v] for (u, v, c, l) in arestas if u == i) -
                       mdl.sum(fluxo[v, u] for (v, u, c, l) in arestas if u == i) <= demanda[i])

# Restrições de transbordo
for i in transbordo:
    mdl.add_constraint(mdl.sum(fluxo[u, v] for (u, v, c, l) in arestas if u == i) -
                       mdl.sum(fluxo[v, u] for (v, u, c, l) in arestas if u == i) == 0)

# Restrições de capacidade
for (u, v, c, l) in arestas:
    mdl.add_constraint(fluxo[u, v] <= l)

process = psutil.Process(os.getpid())
mem_before = process.memory_info().rss / (1024.0 * 1024.0)

print("--------Informacoes da Execucao:----------")
print(f"#Var: {len(fluxo)}")
print(f"#Restricoes: {sum(1 for _ in mdl.iter_constraints())}")
print(f"Memory usage after variable creation: {mem_before:.6f} MB")

mdl.context.solver.log_output = True
start_time = time.time()
solucao = mdl.solve()
end_time = time.time()
mem_after = process.memory_info().rss / (1024.0 * 1024.0)

print(f"Memory usage after cplex(Model): {mem_after:.6f} MB")
print(f"Elapsed time = {end_time - start_time:.6f} seconds.\n")

if solucao:
    print("Status da FO:", mdl.get_solve_status())
    print("\nVariaveis de decisao:")
    for (u, v) in fluxo:
        if fluxo[u, v].solution_value > 0:
            print(f"x[{u},{v}]: {fluxo[u, v].solution_value:.0f}")

    print(f"\nFuncao Objetivo Valor = {mdl.objective_value:.0f}")
    print(f"..({end_time - start_time:.6f} seconds).\n")
    print(f"Memory usage before end: {mem_after:.6f} MB")
else:
    print("Nenhuma solucao encontrada.")