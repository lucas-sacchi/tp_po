import os
import subprocess

# Dicionário para mapear opções do menu aos caminhos dos scripts
scripts = {
    "1": "PCM/pcm.py",
    "2": "PD/pd.py",
    "3": "PFCM/pfcm.py",
    "4": "PFM/pfm.py",
    "5": "PT/pt.py",
}

def menu():
    while True:
        print("\nSelecione um problema para executar:")
        print("1 - PCM")
        print("2 - PD")
        print("3 - PFCM")
        print("4 - PFM")
        print("5 - PT")
        print("0 - Sair")

        opcao = input("\nDigite o número correspondente: ")

        if opcao == "0":
            print("Saindo...")
            break
        elif opcao in scripts:
            script_path = scripts[opcao]
            print(f"\nExecutando {script_path}...\n")
            subprocess.run(["python", script_path], check=True)
        else:
            print("\nOpção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()
