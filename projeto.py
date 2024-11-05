import redis
from datetime import datetime

#conexao com o banco
r = redis.Redis(host='localhost',port=6379, db=0)

def gerarId():
    if not r.exists("tarefa_id"):  
        r.set("tarefa_id", 1)

def pegarId():
    return int(r.get("tarefa_id") or 0)

def incrId():
    r.incr("tarefa_id")

def criarTarefa(titulo,descricao):
    tarefa_id = pegarId()
    data_criacao = datetime.now().strftime('%Y-%m-%d')
    r.hset(tarefa_id, {
        "titulo":titulo,
        "descricao":descricao,
        "data":data_criacao,
        "status":"pendente"
    })
    incrId()
    print(f"Tarefa {titulo} criada com sucesso")

def verTarefa(tarefa_id):
    tarefa = r.hgetall(tarefa_id)
    if tarefa:
        print(f"Usuário {tarefa_id}: {tarefa}")
    else:
        print(f"Tarefa {tarefa_id} não encontrado!")


def exibirTodas():
    tarefas = r.scan_iter()  # Obtém todas as chaves no Redis
    for tarefa in tarefas:
        tarefa_srt = tarefa.decode()  # Converte a chave de bytes para string
        print(f"Tarefa: {tarefa_srt}")  # Imprime a chave (tarefa)

        # Verifica se a chave é um hash
        if r.type(tarefa) == b'hash':
            dado = r.hgetall(tarefa)  # Obtém todos os campos e valores do hash
            # Decodifica as chaves e valores do hash para strings
            dado_decodificado = {k.decode(): v.decode() for k, v in dado.items()}
            print("Dados (hash)") 
            for k, v in dado_decodificado.items():
                print(f"    {k}: {v}\n") 

        # Verifica se a chave é uma string
        elif r.type(tarefa) == b'string':
            value = r.get(tarefa)  # Obtém o valor associado à chave
            print(f"  Dados (string): {value.decode()}")  # Exibe o valor da string

        # Verifica se a chave é uma lista
        elif r.type(tarefa) == b'list':
            value = r.lrange(tarefa, 0, -1)  # Obtém todos os itens da lista
            value_decodificado = [v.decode() for v in value]  # Decodifica os itens para string
            print(f"  Dados (lista): {value_decodificado}")  # Exibe os itens da lista

        # Verifica se a chave é um set
        elif r.type(tarefa) == b'set':
            value = r.smembers(tarefa)  # Obtém todos os membros do set
            value_decodificado = {v.decode() for v in value}  # Decodifica os membros para string
            print(f"  Dados (set): {value_decodificado}")  # Exibe os membros do set

        # Verifica se a chave é um sorted set
        elif r.type(tarefa) == b'zset':
            value = r.zrange(tarefa, 0, -1, withscores=True)  # Obtém os membros e suas pontuações
            value_decodificado = [(v[0].decode(), v[1]) for v in value]  # Decodifica os membros para string
            print(f"  Dados (sorted set): {value_decodificado}")  # Exibe os membros e pontuações do sorted set

        else:
            print("  Tipo de dado desconhecido.")




gerarId()


exibirTodas()

