#
#    Copyright (C) 2020-2030 Thorium Corp FP <help@thoriumcorp.website>
#

import base64
import datetime
import sched
import time
import pytz
import threading
from werkzeug import urls

from odoo import models, fields, api, tools, SUPERUSER_ID, _
from odoo.modules import get_module_resource
from odoo.osv.expression import get_unaccent_wrapper
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta, date
from odoo.exceptions import UserError, ValidationError

#+++++++++++++++++++++++++++++++++++++ incorporated from res.partner ++++++++++++++++++++++++++++++

# Global variables used for the warning fields declared on the thoriumcorp.scada.web
# in the following modules : 
WARNING_MESSAGE = [
                   ('no-message','No Message'),
                   ('warning','Warning'),
                   ('block','Blocking Message')
                   ]
WARNING_HELP = 'Selecting the "Warning" option will notify user with the message, Selecting "Blocking Message" will throw an exception with the message and block the flow. The Message has to be written in the next field.'


ADDRESS_FIELDS = ('ipaddress', 'port', 'dispositive_id')
@api.model
def _lang_get(self):
    return self.env['res.lang'].get_installed()


# put POSIX 'Etc/*' entries at the end to avoid confusing users - see bug 1086728
_tzs = [(tz, tz) for tz in sorted(pytz.all_timezones, key=lambda tz: tz if not tz.startswith('Etc/') else '_')]
def _tz_get(self):
    return _tzs

def timer():
    now = time.localtime(time.time())
    return now[5]

RUN = False 

ESTATUS = "Detenido"

def tarea(comienzo, nombre):
    ahora = time.time()
    diferencia = int(ahora - comienzo)
    if RUN:
        ESTATUS = "Corriendo Tarea " + nombre 
#        print('MOMENTO :', int(ahora),'Diferencia:', diferencia, 'segundos','Tarea:', nombre)
    time.sleep(0.5)
    programador.enter(1, 1, tarea, (comienzo, nombre))

programador = sched.scheduler(time.time, time.sleep)

#class DataModel(models.Model):

#class DataMemory(model.Model):

#class EventsAndAlarms(model.Model):

#class History(model.Model):

#class Protocols(model.Model):

#class ScadaWeb(models.Model):

class ScadaWebPruebas(models.Model):
    _description = 'SCADA Web Pruebas'
    _name = 'scada.web.pruebas'


    comienzo = time.time()

    programador.enter(1, 1, tarea, (comienzo, 'TAREA_1'))
#    programador.enter(2, 1, tarea, (comienzo, 'TAREA_2'))
#    programador.enter(3, 1, tarea, (comienzo, 'TAREA_3'))

#    programador.run()

    datetime = fields.Datetime.now()
    scada_web_test_id = fields.Many2one(string='Test to SCADA Web ID', default= 'SW-TST'+datetime.strftime('%Y%m%d%H%M%S'), readonly=True, index=True)

    minutes = fields.Integer(string='Minuto de corrida actual:', readonly=True, value = 0)
    current_sec = fields.Datetime('Segundos transcurridos:', readonly=True,)
    status = fields.Char(string='Estado del SCADA:',help='Estado actual del SCADA', readonly=True, value = ESTATUS, required=True,)
    run = fields.Boolean(string='Correr prueba:', default=False, value = RUN)

    @api.model
    def create(self, vals):
        self.datetime = datetime.now()
        vals['scada_web_test_id'] = 'SW-TST' + datetime.strftime('%Y%m%d%H%M%S')
        self.status = ESTATUS
        self.minutes = 0
        self.current_sec = datetime.now()
        return super(ScadaWebPruebas, self).create(vals)

    @api.onchange('run')
    def on_change_run(self):
        if not self.run:
            RUN = False
            ESTATUS = "Suspedido"
            return False
        RUN = True
        ESTATUS = "Corriendo"
        self.comienzo = time.time()
        self.run= RUN
        self.current_sec = datetime.now()
        self.minutes = 0
        self.status = ESTATUS
        programador.run()




