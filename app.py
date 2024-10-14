from flask import Flask, request, jsonify
import mysql.connector


app = Flask(__name__)

DB_NOME = "mydb"
DB_USUARIO = "root"
DB_SENHA = "Rafael@2003"
DB_HOST = "localhost"
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


# CRUD para tabela de combustível
@app.route('/combustivel', methods=['POST'])
def criar_combustivel():
    data = request.json
    conn = abrirConexao()
    if conn is None:
        return jsonify({'message': 'Erro ao conectar com o banco de dados.'}), 500
    cur = conn.cursor()
    try:
        cur.execute(""" 
        INSERT INTO combustivel (id_combustivel, nome, tipo, preco_litro, data_ajuste_preco, reservatorio_id_reservatorio) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (data['id_combustivel'], data['nome'], data['tipo'], data['preco_litro'], data['data_ajuste_preco'], data['reservatorio_id_reservatorio']))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Erro ao criar combustível.', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'id': data['id_combustivel']}), 201

@app.route('/combustivel', methods=['GET'])
def leitura_combustivel():
    conn = abrirConexao()
    if conn is None:
        return jsonify({'message': 'Erro ao conectar com o banco de dados.'}), 500
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM combustivel;')
        combustiveis = cur.fetchall()
    except Exception as e:
        return jsonify({'message': 'Erro ao obter combustíveis.', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify(combustiveis)

@app.route('/combustivel/<int:id>', methods=['PUT'])
def atualizar_combustivel(id):
    data = request.json
    conn = abrirConexao()
    if conn is None:
        return jsonify({'message': 'Erro ao conectar com o banco de dados.'}), 500
    cur = conn.cursor()
    try:
        cur.execute(""" 
        UPDATE combustivel SET nome = %s, tipo = %s, preco_litro = %s, data_ajuste_preco = %s, reservatorio_id_reservatorio = %s 
        WHERE id_combustivel = %s
        """, (data['nome'], data['tipo'], data['preco_litro'], data['data_ajuste_preco'], data['reservatorio_id_reservatorio'], id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Erro ao atualizar combustível.', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'message': 'Combustível atualizado com sucesso.'})

@app.route('/combustivel/<int:id>', methods=['DELETE'])
def deletar_combustivel(id):
    conn = abrirConexao()
    if conn is None:
        return jsonify({'message': 'Erro ao conectar com o banco de dados.'}), 500
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM combustivel WHERE id_combustivel = %s;', (id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Erro ao deletar combustível.', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'message': 'Combustível deletado com sucesso.'})

# CRUD para tabela de bomba
@app.route('/bomba', methods=['POST'])
def criar_bomba():
    data = request.json
    conn = abrirConexao()
    if conn is None:
        return jsonify({'message': 'Erro ao conectar com o banco de dados.'}), 500
    cur = conn.cursor()
    try:
        cur.execute(""" 
        INSERT INTO bomba (id_bomba, volume_distribuido, data_proxima_manutenca, data_ultima_manutencao) 
        VALUES (%s, %s, %s, %s)
        """, (data['id_bomba'], data['volume_distribuido'], data['data_proxima_manutenca'], data['data_ultima_manutencao']))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Erro ao criar bomba.', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'id': data['id_bomba']}), 201

@app.route('/bomba', methods=['GET'])
def leitura_bombas():
    conn = abrirConexao()
    if conn is None:
        return jsonify({'message': 'Erro ao conectar com o banco de dados.'}), 500
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM bomba;')
        bombas = cur.fetchall()
    except Exception as e:
        return jsonify({'message': 'Erro ao obter bombas.', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify(bombas)

@app.route('/bomba/<int:id>', methods=['PUT'])
def atualizar_bomba(id):
    data = request.json
    conn = abrirConexao()
    if conn is None:
        return jsonify({'message': 'Erro ao conectar com o banco de dados.'}), 500
    cur = conn.cursor()
    try:
        cur.execute(""" 
        UPDATE bomba SET volume_distribuido = %s, data_proxima_manutenca = %s, data_ultima_manutencao = %s 
        WHERE id_bomba = %s
        """, (data['volume_distribuido'], data['data_proxima_manutenca'], data['data_ultima_manutencao'], id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Erro ao atualizar bomba.', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'message': 'Bomba atualizada com sucesso.'})

@app.route('/bomba/<int:id>', methods=['DELETE'])
def deletar_bomba(id):
    conn = abrirConexao()
    if conn is None:
        return jsonify({'message': 'Erro ao conectar com o banco de dados.'}), 500
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM bomba WHERE id_bomba = %s;', (id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Erro ao deletar bomba.', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'message': 'Bomba deletada com sucesso.'})

# CRUD para tabela de abastece
@app.route('/abastece', methods=['POST'])
def criar_abastece():
    data = request.json
    conn = abrirConexao()
    if conn is None:
        return jsonify({'message': 'Erro ao conectar com o banco de dados.'}), 500
    cur = conn.cursor()
    try:
        cur.execute(""" 
        INSERT INTO abastece (combustivel_id_combustivel, bomba_id_bomba, status, data_abastecimento, id_abastece) 
        VALUES (%s, %s, %s, %s, %s)
        """, (data['combustivel_id_combustivel'], data['bomba_id_bomba'], data['status'], data['data_abastecimento'], data['id_abastece']))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Erro ao criar abastece.', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'id': data['id_abastece']}), 201

@app.route('/abastece', methods=['GET'])
def leitura_abastece():
    conn = abrirConexao()
    if conn is None:
        return jsonify({'message': 'Erro ao conectar com o banco de dados.'}), 500
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM abastece;')
        abastecimentos = cur.fetchall()
    except Exception as e:
        return jsonify({'message': 'Erro ao obter abastecimentos.', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify(abastecimentos)

@app.route('/abastece/<string:id>', methods=['PUT'])
def atualizar_abastece(id):
    data = request.json
    conn = abrirConexao()
    if conn is None:
        return jsonify({'message': 'Erro ao conectar com o banco de dados.'}), 500
    cur = conn.cursor()
    try:
        cur.execute(""" 
        UPDATE abastece SET combustivel_id_combustivel = %s, bomba_id_bomba = %s, status = %s, data_abastecimento = %s 
        WHERE id_abastece = %s
        """, (data['combustivel_id_combustivel'], data['bomba_id_bomba'], data['status'], data['data_abastecimento'], id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Erro ao atualizar abastece.', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'message': 'Abastece atualizado com sucesso.'})

@app.route('/abastece/<string:id>', methods=['DELETE'])
def deletar_abastece(id):
    conn = abrirConexao()
    if conn is None:
        return jsonify({'message': 'Erro ao conectar com o banco de dados.'}), 500
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM abastece WHERE id_abastece = %s;', (id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Erro ao deletar abastece.', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'message': 'Abastece deletado com sucesso.'})

if __name__ == '__main__':
    app.run(debug=True)
