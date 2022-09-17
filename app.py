from collections import defaultdict

from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import extract

from models import db_session
from models import ModeloColaborador, ModeloPonto

app = Flask(__name__)
api = Api(app)


class Colaborador(Resource):
    def get(self, id):
        colaboradores = ModeloColaborador.query.filter_by(
            id=id).first()
        try:
            response = {
                'id': colaboradores.id,
                'nome': colaboradores.nome,
                'cpf': colaboradores.cpf,
                'email': colaboradores.email,
                'celular': colaboradores.celular,
                'empresa': colaboradores.empresa,
                'cargo': colaboradores.cargo,
                'endereco': colaboradores.endereco,
                'cep': colaboradores.cep,
                'ativo': colaboradores.ativo,
            }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'Colaborador não encontrado'
            }
        return response

    def put(self, id):
        colaboradores = ModeloColaborador.query.filter_by(
            id=id).first()
        dados = request.json

        if 'id' in dados:
            colaboradores.id = dados['id']

        if 'nome' in dados:
            colaboradores.nome = dados['nome']

        if 'cpf' in dados:
            colaboradores.cpf = dados['cpf']

        if 'email' in dados:
            colaboradores.email = dados['email']

        if 'celular' in dados:
            colaboradores.celular = dados['celular']

        if 'empresa' in dados:
            colaboradores.empresa = dados['empresa']

        if 'cargo' in dados:
            colaboradores.cargo = dados['cargo']

        if 'endereco' in dados:
            colaboradores.endereco = dados['endereco']

        if 'cep' in dados:
            colaboradores.cep = dados['cep']

        if 'ativo' in dados:
            colaboradores.ativo = dados['ativo']

        colaboradores.save()
        response = {
            'id': colaboradores.id,
            'nome': colaboradores.nome,
            'cpf': colaboradores.cpf,
            'email': colaboradores.email,
            'celular': colaboradores.celular,
            'empresa': colaboradores.empresa,
            'cargo': colaboradores.cargo,
            'endereco': colaboradores.endereco,
            'cep': colaboradores.cep,
            'ativo': colaboradores.ativo
        }

        return response

    def delete(self, id):
        colaboradores = ModeloColaborador.query.filter_by(id=id).first()
        mensagem = 'Colaborador {} excluido com sucesso'.format(colaboradores)
        colaboradores.delete()
        return {'status': 'sucesso', 'mensagem': mensagem}


class ListaColaborador(Resource):

    def get(self):
        colaborador = ModeloColaborador.query.all()
        response = [{
            'id': i.id,
            'nome': i.nome,
            'cpf': i.cpf,
            'email': i.email,
            'celular': i.celular,
            'empresa': i.empresa,
            'cargo': i.cargo,
            'endereco': i.endereco,
            'cep': i.cep,
            'ativo': i.ativo

        } for i in colaborador]
        return response

    def post(self):
        dados = request.json
        retorno = []
        retorno.append(- dados['id'])
        for i in range (0,int(dados['id'])):
            retorno.append(dados['nome'])
        colaborador = ModeloColaborador(
            nome=dados['nome'],
            cpf=dados['cpf'],
            email=dados['email'],
            celular=dados['celular'],
            empresa=dados['empresa'],
            cargo=dados['cargo'],
            endereco=dados['endereco'],
            cep=dados['cep'],
            ativo=dados['ativo']
        )

        colaborador.save()
        response = {
            'id': colaborador.id,
            'nome': colaborador.nome,
            'cpf': colaborador.cpf,
            'email': colaborador.email,
            'celular': colaborador.celular,
            'empresa': colaborador.empresa,
            'cargo': colaborador.cargo,
            'endereco': colaborador.endereco,
            'cep': colaborador.cep,
            'ativo': colaborador.ativo
        }
        return response


api.add_resource(Colaborador, '/colaborador/<int:id>/')
api.add_resource(ListaColaborador, '/listacolaborador/')

if __name__ == '__main__':
    app.run(debug=True)
