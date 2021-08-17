##############################################################################
#
#    Copyright (C) 2020-2030 Thorium Corp FP <help@thoriumcorp.website>
#
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import MissingError
import requests
import json
import datetime


# __all__ = ['CreateScadaTestOrderInit', 'CreateScadaTestOrder', 'RequestTest',
#     'RequestOperatorScadaTestStart', 'RequestOperatorScadaTest']


# class CreateScadaTestOrderInit(ModelView):
#     'Create Test Report Init'
#     _name = 'thoriumcorp.scada.test.create.init'


class CreateScadaTestOrder(models.TransientModel):
    _name = 'thoriumcorp.scada.test.create'
    _description = 'Create Scada Test Report'

    start = StateView('thoriumcorp.scada.test.create.init',
        'thoriumcorp_scada.view_scada_make_test', [
            Button('Cancel', 'end', 'thorium-cancel'),
            Button('Create Test Order', 'create_scada_test', 'thorium-ok', True),
            ])

    create_scada_test = StateTransition()

    def transition_create_scada_test(self):
        TestRequest = Pool().get('thoriumcorp.operator.scada.test')
        Scada = Pool().get('thoriumcorp.scada')

        tests_report_data = []

        tests = TestRequest.browse(Transaction().context.get('active_ids'))

        for scada_test_order in tests:

            test_cases = []
            test_report_data = {}

            if scada_test_order.state == 'ordered':
                self.raise_user_error(
                    "The Scada test order is already created")

            test_report_data['test'] = scada_test_order.name.id
            test_report_data['operator'] = scada_test_order.operator_id.id
            if scada_test_order.doctor_id:
                test_report_data['requestor'] = scada_test_order.doctor_id.id
            test_report_data['date_requested'] = scada_test_order.date
            test_report_data['request_order'] = scada_test_order.request

            for critearea in scada_test_order.name.critearea:
                test_cases.append(('create', [{
                        'name': critearea.name,
                        'sequence': critearea.sequence,
                        'lower_limit': critearea.lower_limit,
                        'upper_limit': critearea.upper_limit,
                        'normal_range': critearea.normal_range,
                        'units': critearea.units and critearea.units.id,
                    }]))
            test_report_data['critearea'] = test_cases

            tests_report_data.append(test_report_data)

        Scada.create(tests_report_data)
        TestRequest.write(tests, {'state': 'ordered'})

        return 'end'


class RequestTest(ModelView):
    'Request - Test'
    _name = 'thoriumcorp.request-test'
    _table = 'thoriumcorp_request_test'

    request = fields.Many2One('thoriumcorp.operator.scada.test.request.start',
        'Request', required=True)
    test = fields.Many2One('thoriumcorp.scada.test_type', 'Test', required=True)


class RequestOperatorScadaTestStart(ModelView):
    'Request Operator Scada Test Start'
    _name = 'thoriumcorp.operator.scada.test.request.start'

    date = fields.DateTime('Date')
    operator = fields.Many2One('thoriumcorp.operator', 'Operator', required=True)
    admin = fields.Many2One('thoriumcorp.operador', 'Admin',
        help="Doctor who Request the scada tests.")
    tests = fields.Many2Many('thoriumcorp.request-test', 'request', 'test',
        'Tests', required=True)
    urgent = fields.Boolean('Urgent')

    @staticmethod
    def default_date():
        return datetime.now()

    @staticmethod
    def default_operator():
        if Transaction().context.get('active_model') == 'thoriumcorp.operator':
            return Transaction().context.get('active_id')

    @staticmethod
    def default_doctor():
        pool = Pool()
        ThroriumOperator= pool.get('thoriumcorp.throriumprofessional')
        hp = ThroriumOperator.get_thoriumcorp_professional()
        if not hp:
            RequestOperatorScadaTestStart.raise_user_error(
                "No medical professional associated to this user !")
        return hp

class RequestOperatorScadaTest(models.TransientModel):
    _name = 'thoriumcorp.operator.scada.test.request'
    _description = 'Request Operator Scada Test'

    start = StateView('thoriumcorp.operator.scada.test.request.start',
        'thoriumcorp_scada.operator_scada_test_request_start_view_form', [
            Button('Cancel', 'end', 'thorium-cancel'),
            Button('Request', 'request', 'thorium-ok', default=True),
            ])
    request = StateTransition()

    def transition_request(self):
        OperatorScadaTest = Pool().get('thoriumcorp.operator.scada.test')
        Sequence = Pool().get('ir.sequence')
        Config = Pool().get('thoriumcorp.sequences')

        config = Config(1)
        request_number = Sequence.get_id(config.scada_request_sequence.id)
        scada_tests = []
        for test in self.start.tests:
            scada_test = {}
            scada_test['request'] = request_number
            scada_test['name'] = test.id
            scada_test['operator_id'] = self.start.operator.id
            if self.start.doctor:
                scada_test['doctor_id'] = self.start.doctor.id
            scada_test['date'] = self.start.date
            scada_test['urgent'] = self.start.urgent
            scada_tests.append(scada_test)
        OperatorScadaTest.create(scada_tests)

        return 'end'

