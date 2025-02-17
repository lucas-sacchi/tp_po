from docplex.mp.model import Model
import time
import psutil
import os
import pandas as pd

def ler_dados_transporte(arquivo):
    with open(arquivo, 'r') as f:
        linhas = f.readlines()
    S, D = map(int, linhas[0].strip().split())
    oferta = list(map(int, linhas[1:S+1]))
    demanda = list(map(int, linhas[S+1:S+1+D]))
    custos = []
    for linha in linhas[S+1+D:S+1+D+S]:
        custos.append(list(map(int, linha.strip().split())))
    return S, D, oferta, demanda, custos

arquivo_transporte = os.path.join(os.path.dirname(__file__), 'in.txt')
S, D, oferta, demanda, custos = ler_dados_transporte(arquivo_transporte)
mdl = Model(name="Problema_Transporte")
x = {(i, j): mdl.continuous_var(lb=0, name=f"x_{i}_{j}") for i in range(S) for j in range(D)}
mdl.minimize(mdl.sum(x[i, j] * custos[i][j] for i in range(S) for j in range(D)))

for i in range(S):
    mdl.add_constraint(mdl.sum(x[i, j] for j in range(D)) <= oferta[i], f"oferta_{i}")

for j in range(D):
    mdl.add_constraint(mdl.sum(x[i, j] for i in range(S)) == demanda[j], f"demanda_{j}")

process = psutil.Process(os.getpid())
mem_before = process.memory_info().rss / (1024.0 * 1024.0)

print("--------Informacoes da Execucao:----------")
print(f"#Var: {len(x)}")
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
    for i in range(S):
        for j in range(D):
            valor = x[i, j].solution_value
            if valor > 0:
                print(f"x[{i},{j}]: {valor:.0f}")
                resultado.append((i, j, valor))

    print(f"\nFuncao Objetivo Valor = {mdl.objective_value:.0f}")
    print(f"..({end_time - start_time:.6f} seconds).\n")
    print(f"Memory usage before end: {mem_after:.6f} MB")

    df_resultado = pd.DataFrame(resultado, columns=["Fornecedor", "Destino", "Quantidade"])
    
    print(df_resultado.to_string(index=False))
else:
    print("Nenhuma solução encontrada.")
