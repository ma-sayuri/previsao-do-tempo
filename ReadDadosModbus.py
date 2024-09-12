import time
from pymodbus.client import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
import datetime
import pyodbc  # Importação do pyodbc para conexão com SQL Server

def atualizar_dados_na_tabela(endereco, valor):
    # Configuração da conexão com o SQL Server
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost\SQLEXPRESS;"  # Substitua pelo nome do seu servidor se não for localhost
        "DATABASE=master;"  # Substitua pelo nome do banco de dados
        "Trusted_Connection=yes;" # Usa a autenticação integrada do Windows
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Verifica se o endereço já existe na tabela
    consulta_sql = "SELECT COUNT(1) FROM DadosModbus WHERE Endereco = ?"
    cursor.execute(consulta_sql, (endereco,))
    existe = cursor.fetchone()

    if existe is not None and existe[0] > 0:
        # Atualiza o valor do endereço existente
        atualizacao_sql = """
        UPDATE DadosModbus
        SET Valor = ?, DataHora = GETDATE()
        WHERE Endereco = ?
        """
        try:
            cursor.execute(atualizacao_sql, (valor, endereco))
            conn.commit()
            print(f"Dados atualizados com sucesso: Endereço={endereco}, Valor={valor}")
        except Exception as e:
            print(f"Erro ao atualizar dados: {e}")
    else:
        # Insere um novo registro se o endereço não existir
        insercao_sql = """
        INSERT INTO DadosModbus (Endereco, Valor)
        VALUES (?, ?)
        """
        try:
            cursor.execute(insercao_sql, (endereco, valor))
            conn.commit()
            print(f"Dados inseridos com sucesso: Endereço={endereco}, Valor={valor}")
        except Exception as e:
            print(f"Erro ao inserir dados: {e}")
        finally:
            cursor.close()
            conn.close()

# Função principal para leitura Modbus
def main():
    cliente_tremembe = ModbusTcpClient('186.227.13.38', port=1002)



    try:
        # Conectar ao servidor Modbus
        if not cliente_tremembe.connect():
            print("Não foi possível conectar ao servidor Modbus.")
            exit()

        while True:
            # Exemplo de leitura de holding registers
            result = cliente_tremembe.read_holding_registers(101, 2, slave=1)  # Modifique conforme necessário

            # Verificação se a leitura foi bem-sucedida
            if result.isError():
                print(f"Erro ao ler registers: {result}")
            else:
                print(f"Valores dos registers: {result.registers}")
                print(result.registers if 53 < 200 else f'Corrente: {result.registers}')
            b = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.BIG,
                                                   wordorder=Endian.BIG)
            c = b.decode_16bit_int() / 10
            print(f"valor word: {c}")
                # Atualizar ou inserir os dados lidos na tabela
            for i, valor in enumerate(result.registers):
                    atualizar_dados_na_tabela(i, valor)
            # Espera de 5 segundos antes de realizar a próxima leitura
            time.sleep(5)

    except Exception as e:
        print(f"Ocorreu uma exceção: {e}")

    finally:
        # Fechar a conexão
        cliente_tremembe.close()
        

if __name__ == "__main__":
    # Criar tabela no SQL Server
   # criar_tabela_sql_server()
    
    # Executar a leitura Modbus e atualizar/inserir os dados na tabela
    main()

