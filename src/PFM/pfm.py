from docplex.mp.model import Model
import time
import psutil
import os
import pandas as pd

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
mdl = Model(name="Fluxo_Maximo")
fluxo = {(u, v): mdl.continuous_var(lb=0, ub=c, name=f"x_{u}_{v}") for (u, v, c) in arestas}
fonte = 1
destino = n_vertices
mdl.maximize(mdl.sum(fluxo[fonte, j] for j in range(1, n_vertices + 1) if (fonte, j) in fluxo))

for i in range(1, n_vertices + 1):
    if i not in [fonte, destino]:
        mdl.add_constraint(
            mdl.sum(fluxo[u, i] for u in range(1, n_vertices + 1) if (u, i) in fluxo) ==
            mdl.sum(fluxo[i, v] for v in range(1, n_vertices + 1) if (i, v) in fluxo)
        )

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
    resultado = []
    for (u, v) in fluxo:
        valor = fluxo[u, v].solution_value
        if valor > 0:
            print(f"x[{u},{v}]: {valor:.0f}")
            resultado.append((u, v, valor))

    print(f"\nFuncao Objetivo Valor = {mdl.objective_value:.0f}")
    print(f"..({end_time - start_time:.6f} seconds).\n")
    print(f"Memory usage before end: {mem_after:.6f} MB")

    df_resultado = pd.DataFrame(resultado, columns=["Origem", "Destino", "Fluxo"])
    
    print(df_resultado.to_string(index=False))
else:
    print("Nenhuma solução encontrada.")
