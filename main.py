from sistema_ponto.cadastro import CadastroFuncionario
from sistema_ponto.reconhecimento import ReconhecimentoFacial
from sistema_ponto.treino import TreinadorModelo


def menu():
    while True:
        print("\n" + "=" * 40)
        print(" SISTEMA DE PONTO FACIAL ")
        print("=" * 40)
        print("1 - Cadastrar novo funcionario")
        print("2 - Treinar modelo")
        print("3 - Iniciar reconhecimento / bater ponto")
        print("4 - Sair")
        print("=" * 40)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome = input("Digite o nome do funcionario: ").strip()
            cadastro = CadastroFuncionario(max_fotos=100)
            cadastro.cadastrar(nome)

        elif opcao == "2":
            treinador = TreinadorModelo()
            treinador.treinar()

        elif opcao == "3":
            reconhecimento = ReconhecimentoFacial(
                limite_confianca=65,
                tempo_espera_registro=10
            )
            reconhecimento.iniciar()

        elif opcao == "4":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
