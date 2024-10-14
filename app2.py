from flask import Flask, request, jsonify
import mysql.connector


app = Flask(__name__)

DB_NOME = "mysql"
DB_USUARIO = "root"
DB_SENHA = "Rafael@2003"
DB_HOST = "Mysql@localhost:3306"
DB_PORT = "3306"

def abrirConexao():
    try:
        conn = mysql.connector.connect(
            database=DB_NOME,
            user=DB_USUARIO,
            password=DB_SENHA,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Banco de dados conectado com sucesso.")
        return conn
    except Exception as error:
        print(f"Erro ao conectar com Banco de Dados: {error}")
        return None


@app.route('/produto', methods=['POST'])
def criar_produto():
    data = request.json
    print("Dados recebidos:", data)
    conn = abrirConexao()
    if conn is None:
        return jsonify({'message': 'Erro ao conectar com o banco de dados.'}), 500
    cur = conn.cursor()
    try:
        cur.execute("""
        INSERT INTO posto.produto (id_produto, nome, descricao, tipo, preco_final, estoque_id_estoque) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (data['id_produto'], data['nome'], data['descricao'], data['tipo'], data['preco_final'], data['estoque_id_estoque']))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Erro ao criar produto.', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'id': data['id_produto']}), 201

@app.route('/produto', methods=['GET'])
def leitura_produtos():
    conn = abrirConexao()
    if conn is None:
        return jsonify({'message': 'Erro ao conectar com o banco de dados.'}), 500
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM posto.produto;')
        produtos = cur.fetchall()
    except Exception as e:
        return jsonify({'message': 'Erro ao obter produtos.', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify(produtos)

@app.route('/produto/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    data = request.json
    conn = abrirConexao()
    if conn is None:
        return jsonify({'message': 'Erro ao conectar com o banco de dados.'}), 500
    cur = conn.cursor()
    try:
        cur.execute("""
        UPDATE posto.produto SET nome = %s WHERE id_produto = %s
        """, (data['nome'], id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Erro ao atualizar produto.', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'message': 'Produto atualizado com sucesso.'})

@app.route('/produto/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    conn = abrirConexao()
    if conn is None:
        return jsonify({'message': 'Erro ao conectar com o banco de dados.'}), 500
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM posto.produto WHERE id_produto = %s;', (id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Erro ao deletar produto.', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'message': 'Produto deletado com sucesso.'})


# CRUD para tabela de estoque (similar ao produto)
@app.route('/estoque', methods=['POST'])
def criar_estoque():
    data = request.json
    conn = abrirConexao()
    if conn is None:
        return jsonify({'message': 'Erro ao conectar com o banco de dados.'}), 500
    cur = conn.cursor()
    try:
        cur.execute("""
        INSERT INTO posto.estoque (id_estoque, quantidade_disponivel) 
        VALUES (%s, %s)
        """, (data['id_estoque'], data['quantidade_disponivel']))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Erro ao criar estoque.', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'id': data['id_estoque']}), 201

@app.route('/estoque', methods=['GET'])
def leitura_estoque():
    conn = abrirConexao()
    if conn is None:
        return jsonify({'message': 'Erro ao conectar com o banco de dados.'}), 500
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM posto.estoque;')
        estoques = cur.fetchall()
    except Exception as e:
        return jsonify({'message': 'Erro ao obter estoques.', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify(estoques)

@app.route('/estoque/<int:id>', methods=['PUT'])
def atualizar_estoque(id):
    data = request.json
    conn = abrirConexao()
    if conn is None:
        return jsonify({'message': 'Erro ao conectar com o banco de dados.'}), 500
    cur = conn.cursor()
    try:
        cur.execute("""
        UPDATE posto.estoque SET quantidade_disponivel = %s WHERE id_estoque = %s
        """, (data['quantidade_disponivel'], id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Erro ao atualizar estoque.', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'message': 'Estoque atualizado com sucesso.'})

@app.route('/estoque/<int:id>', methods=['DELETE'])
def deletar_estoque(id):
    conn = abrirConexao()
    if conn is None:
        return jsonify({'message': 'Erro ao conectar com o banco de dados.'}), 500
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM posto.estoque WHERE id_estoque = %s;', (id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Erro ao deletar estoque.', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'message': 'Estoque deletado com sucesso.'})

# Terceira tabela 

if __name__ == '__main__':
    app.run(host='localhost', port=3000)
