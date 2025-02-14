from docplex.mp.model import Model
import time
import psutil
import os
import pandas as pd

def ler_dados_designacao(arquivo):
    with open(arquivo, 'r') as f:
        linhas = f.readlines()
    n = int(linhas[0].strip())
    custos = []
    for linha in linhas[1:n+1]:
        custos.append(list(map(int, linha.strip().split())))
    return n, custos

arquivo_designacao = "in.txt"
n, custos = ler_dados_designacao(arquivo_designacao)
mdl = Model(name="Problema_Designacao")
x = {(i, j): mdl.binary_var(name=f"x_{i}_{j}") for i in range(n) for j in range(n)}
mdl.minimize(mdl.sum(x[i, j] * custos[i][j] for i in range(n) for j in range(n)))

for i in range(n):
    mdl.add_constraint(mdl.sum(x[i, j] for j in range(n)) == 1, f"trabalhador_{i}")
for j in range(n):
    mdl.add_constraint(mdl.sum(x[i, j] for i in range(n)) == 1, f"tarefa_{j}")

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
    for i in range(n):
        for j in range(n):
            valor = x[i, j].solution_value
            if valor > 0:
                print(f"x[{i},{j}]: {valor:.0f}")
                resultado.append((i, j, valor))

    print(f"\nFuncao Objetivo Valor = {mdl.objective_value:.0f}")
    print(f"..({end_time - start_time:.6f} seconds).\n")
    print(f"Memory usage before end: {mem_after:.6f} MB")

    df_resultado = pd.DataFrame(resultado, columns=["Trabalhador", "Tarefa", "Atribuído"])
    
    print(df_resultado.to_string(index=False))
else:
    print("Nenhuma solução encontrada.")
