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
        u, v, c = map(int, linha.strip().split())
        arestas.append((u, v, c))  
    return n_vertices, n_arestas, arestas

arquivo_grafo = "in.txt"
n_vertices, n_arestas, arestas = ler_grafo(arquivo_grafo)
mdl = Model(name="Fluxo_Custo_Minimo")
fluxo = {(u, v): mdl.continuous_var(lb=0, name=f"x_{u}_{v}") for (u, v, c) in arestas}
mdl.minimize(mdl.sum(fluxo[u, v] * c for (u, v, c) in arestas))
fonte = 1
destino = n_vertices

for i in range(1, n_vertices + 1):
    if i == fonte:
        mdl.add_constraint(mdl.sum(fluxo[u, v] for (u, v, c) in arestas if u == i) -
                           mdl.sum(fluxo[v, u] for (v, u, c) in arestas if u == i) == 1)
    elif i == destino:
        mdl.add_constraint(mdl.sum(fluxo[u, v] for (u, v, c) in arestas if u == i) -
                           mdl.sum(fluxo[v, u] for (v, u, c) in arestas if u == i) == -1)
    else:
        mdl.add_constraint(mdl.sum(fluxo[u, v] for (u, v, c) in arestas if u == i) -
                           mdl.sum(fluxo[v, u] for (v, u, c) in arestas if u == i) == 0)

for (u, v, c) in arestas:
    mdl.add_constraint(fluxo[u, v] <= c)

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
    print("Nenhuma solução encontrada.")
