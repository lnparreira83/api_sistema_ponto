from collections import defaultdict

from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import extract

from api_sistema_ponto.models import db_session
from models import ModeloColaborador, ModeloPonto

app = Flask(__name__)
api = Api(app)


class Colaborador(Resource):
    def get(self, colaboradores):
        colaborador = ModeloColaborador.query.filter_by(colaboradores=colaboradores).first()
        try:
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
                'ativo': colaborador.ativo,
                'created_at': str(colaborador.created_at),
                'last_modified_at': str(colaborador.last_modified_at)
            }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'Colaborador não encontrado'
            }
        return response

    def getAll(self):
        colaboradores = ModeloColaborador.query.filter_by()
        colaboradores = list(self.colaboradorToJson(colaborador) for colaborador in colaboradores)
        return {'status': 'success', 'message': 'A lista de colaboradores foi consultada com sucesso',
                'colaboradores': colaboradores}

    def getByCpf(self, cpf):
        colaboradores = ModeloColaborador.query.filter_by(cpf=cpf)
        colaboradores = list(self.colaboradorToJson(colaborador) for colaborador in colaboradores)
        return {'status': 'success', 'message': 'A lista de colaboradores foi consultada com sucesso',
                'colaboradores': colaboradores}

    def getById(self, id):
        if not id:
            return {'status': 'fail', 'message': 'O parametro id é obrigatorio'}, 400
        else:
            try:
                colaborador = ModeloColaborador.query.filter_by(id=id, ativo='SIM').first()
                if colaborador:
                    response_object = {'status': 'success', 'message': 'Consulta realizada com sucesso'}
                    return response_object, 200
                else:
                    return {'status': 'fail', 'message': 'Não existe colaborador ativo associado a este id'}, 400
            except Exception as err:
                return {'status': 'fail', 'message': 'Não foi possivel completar a solicitação'}
            finally:
                db_session.close()

    def post(self, data):
        colaborador = request.json
        colaborador = ModeloColaborador.query.filter_by(cpf=data['cpf'], ativo=True).first()

        if not colaborador:
            colaborador = ModeloColaborador(
                nome=data['nome'],
                cpf=data['cpf'],
                email=data['email'],
                celular=data['celular'],
                empresa=data['empresa'],
                cargo=data['cargo'],
                endereco=data['endereco'],
                cep=data['cep'],
                ativo=True
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
                'ativo': colaborador.ativo,
            }
            return response
        else:
            return {'status': 'fail', 'message': 'Já existe um colaborador ativo com este CPF'}, 400

    def update(self, id):
        if not id:
            return {'status': 'fail', 'message': 'O parâmetro id é obrigatório'}, 400
        else:
            try:
                colaborador = ModeloColaborador.query.filter_by(id=id, ativo=True).first()
                data = request.json

                if not colaborador:
                    return {'status': 'fail', 'message': 'Não existe colaborador associado ao id recebido'}, 400
                else:
                    colaborador.nome = data['nome'] if 'nome' in data else colaborador.nome
                    colaborador.cpf = data['cpf'] if 'cpf' in data else colaborador.cpf
                    colaborador.email = data['email'] if 'email' in data else colaborador.email
                    colaborador.celular = data['celular'] if 'celular' in data else colaborador.celular
                    colaborador.empresa = data['empresa'] if 'empresa' in data else colaborador.empresa
                    colaborador.cargo = data['cargo'] if 'cargo' in data else colaborador.cargo
                    colaborador.endereco = data['endereco'] if 'endereco' in data else colaborador.endereco
                    colaborador.cep = data['cep'] if 'cep' in data else colaborador.cep
                    colaborador.ativo = data['ativo'] if 'ativo' in data else colaborador.ativo

                    try:
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
                            'ativo': colaborador.ativo,
                        }
                        return response

                    except Exception as err:
                        db_session.rollback()
                        return {'status': 'fail', 'message': 'Não foi possível atualizar o colaborador no momento'}, 500
                    finally:
                        db_session.close()
            except Exception as err:
                return {'status': 'fail',
                        'message': 'Não foi possível completar a solicitação no momento, por favor tente novamente mais tarde.'}, 500
            finally:
                db_session.close()

    def delete(self, id):
        if not id:
            return {'status': 'fail', 'message': 'O parâmetro id é obrigatório'}, 400
        else:
            try:
                colaborador = ModeloColaborador.query.filter_by(id=id, ativo=True).first()
                mensagem = 'Colaborador {} excluido com sucesso'.format(colaborador)
                colaborador.delete()
                return {'status': 'sucesso', 'mensagem': mensagem}

            except Exception as err:
                return {'status': 'fail',
                        'message': 'Não foi possível completar a solicitação no momento, por favor tente novamente mais tarde.'}, 500
            finally:
                db_session.close()

    def hard_delete(self, id):
        if not id:
            return {'status': 'fail', 'message': 'O parâmetro id é obrigatório'}, 400
        else:
            try:
                colaborador = ModeloColaborador.query.filter_by(id=id).first()

                if not colaborador:
                    return {'status': 'fail', 'message': 'Não existe usuário associado ao id recebido'}, 400
                else:
                    db_session.delete(colaborador)
                    try:
                        db_session.commit()
                        return {'status': 'success',
                                'message': 'O colaborador foi removido permanente com sucesso.'}, 200
                    except Exception as err:
                        return {'status': 'fail',
                                'message': 'Não foi possível completar a solicitação no momento, por favor tente novamente mais tarde.'}, 500
                    finally:
                        db_session.close()
            except Exception as err:
                return {'status': 'fail',
                        'message': 'Não foi possível completar a solicitação no momento, por favor tente novamente mais tarde.'}, 500
            finally:
                db_session.close()


class Ponto(Resource):
    def get(self):
        ponto = ModeloPonto.query.all()
        response = {
            'id': ponto.id,
            'tipo_de_ponto': ponto.tipo_de_ponto,
            'created_at': str(ponto.created_at),
            'last_modified_at': str(ponto.last_modified_at)
        }
        return response

    def getAll(self):
        pontos = ModeloPonto.query.filter_by()
        pontos = list(self.get() for _ in pontos)
        return {'status': 'success', 'message': 'A lista de pontos foi consultada com sucesso', 'pontos': pontos}

    def report(self, colaborador_id, month):
        if colaborador_id and month:
            pontos = self.getByColaboradorIdAndMonth(colaborador_id, month)

            if not pontos:
                return {'status': 'fail', 'message': 'Não há pontos registrados para este colaborador este mês'}, 200
            aux = []
            days = defaultdict(list)
            for ponto in pontos:
                day = ponto.created_at.day
                days[day].append(ponto)

            report = []
            for day in days:
                ins = list(filter(lambda ponto: ModeloPonto.tipo_de_ponto == 'in', days[day]))
                outs = list(filter(lambda ponto: ModeloPonto.tipo_de_ponto == 'out', days[day]))
                days[day] = 0
                if len(ins) > 0 and len(outs) > 0:
                    if ins[0].created_at < outs[-1].created_at:
                        days[day] = float(str(abs(outs[-1].created_at - ins[0].created_at).total_seconds())) / float(
                            3600)
                report.append({
                    "day": day,
                    "work_hours": round(days[day], 5)
                })
            return {'status': 'success', 'message': 'Relatório de ponto consultado com sucesso.', 'report': report}, 200
        else:
            return {'status': 'fail', 'message': 'Os campos colaborador_id e month são obrigatórios'}

    def getByColaboradorIdAndMonth(self, colaborador_id, month):
        if colaborador_id and month:
            pontos = ModeloPonto.query.filter(ModeloPonto.colaborador_id == colaborador_id,
                                              extract('month', ModeloPonto.created_at) == month).order_by(
                ModeloPonto.created_at).all()
        elif colaborador_id:
            pontos = ModeloPonto.query.filter_by(colaborador_id=colaborador_id).order_by(ModeloPonto.created_at)
        elif month:
            pontos = ModeloPonto.query.filter(extract('month', ModeloPonto.created_at) == month).order_by(
                ModeloPonto.created_at).all()
        else:
            pontos = ModeloPonto.query.filter_by().order_by(ModeloPonto.created_at)

        # pontos = list(self.pontoToJson(ponto) for ponto in pontos)
        return pontos

    def getById(self, id):
        if not id:
            return {'status': 'fail', 'message': 'O parâmetro id é obrigatório'}, 400
        else:
            try:
                ponto = ModeloPonto.query.filter_by(id=id).first()
                print(ponto)
                if ponto:
                    response_object = {'status': 'success', 'message': 'Consulta realizada com sucesso',
                                       'ponto': self.pontoToJson(ponto)}
                    return response_object, 200
                else:
                    return {'status': 'fail', 'message': 'Não existe ponto associado a este id'}, 400
            except Exception as err:
                return {'status': 'fail',
                        'message': 'Não foi possível completar a solicitação no momento, por favor tente novamente '
                                   'mais tarde.',
                        'err': err}, 500
            finally:
                db_session.close()

    def save(self):
        data = request.json
        ponto = ModeloPonto(
            tipo_de_ponto=data['tipo_de_ponto'],
            colaborador_id=data['colaborador_id']
        )
        try:
            ponto.save()
            response = {
                'id': ponto.id,
                'tipo_de_ponto': ponto.tipo_de_ponto,
                'created_at': str(ponto.created_at),
                'last_modified_at': str(ponto.last_modified_at)
            }
            return response

        except Exception as err:
            db_session.rollback()
            return {'status': 'fail', 'message': 'Não foi possível adicionar o ponto no momento'}, 500
        finally:
            db_session.close()

    def update(self, id):
        if not id:
            return {'status': 'fail', 'message': 'O parâmetro id é obrigatório'}, 400
        else:
            try:
                ponto = ModeloPonto.query.filter_by(id=id).first()
                data = request.json

                if not ponto:
                    return {'status': 'fail', 'message': 'Não existe ponto associado ao id recebido'}, 400
                else:
                    ponto.tipo_de_ponto = data['tipo_de_ponto'] if 'tipo_de_ponto' in data else ponto.tipo_de_ponto
                    ponto.colaborador_id = data['colaborador_id'] if 'colaborador_id' in data else ponto.colaborador_id
                    ponto.created_at = data['created_at'] if 'created_at' in data else ponto.created_at
                    ponto.last_modified_at = data[
                        'last_modified_at'] if 'last_modified_at' in data else ponto.last_modified_at

                    try:
                        ponto.save()
                        return {'status': 'success', 'message': 'Ponto atualizado com sucesso'}, 200
                    except Exception as err:
                        db_session.rollback()
                        return {'status': 'fail', 'message': 'Não foi possível atualizar o ponto no momento'}, 500
                    finally:
                        db_session.close()
            except Exception as err:
                return {'status': 'fail',
                        'message': 'Não foi possível completar a solicitação no momento, por favor tente novamente '
                                   'mais tarde.'}, 500
            finally:
                db_session.close()

    def delete(self, id):
        if not id:
            return {'status': 'fail', 'message': 'O parâmetro id é obrigatório'}, 400
        else:
            try:
                ponto = ModeloPonto.query.filter_by().first()

                if not ponto:
                    return {'status': 'fail', 'message': 'Não existe ponto associado ao id recebido'}, 400
                else:
                    try:
                        ponto.delete()
                        return {'status': 'success', 'message': 'O ponto foi removido com sucesso.'}, 200
                    except Exception as err:
                        return {'status': 'fail',
                                'message': 'Não foi possível completar a solicitação no momento, por favor tente novamente mais tarde.'}, 500
                    finally:
                        db_session.close()
            except Exception as err:
                return {'status': 'fail',
                        'message': 'Não foi possível completar a solicitação no momento, por favor tente novamente mais tarde.'}, 500
            finally:
                db_session.close()


api.add_resource(Colaborador, '/colaborador/<int:id>')
api.add_resource(Ponto, '/colaborador/ponto/<int:colaborador_id>/')

if __name__ == '__main__':
    app.run(debug=True)
