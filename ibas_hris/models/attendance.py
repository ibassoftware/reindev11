
from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
import pytz



class ibas_attendance(models.Model):
    _inherit = 'hr.attendance'

    is_workday = fields.Boolean(compute='_compute_is_workday', string='Is Work Day?', store=True)
    grace_period = fields.Integer(string='Grace Period in Minutes', default=10)
    is_tardy = fields.Boolean(compute='_compute_is_tardy', string='Is Tardy')
    late_in_float = fields.Float(string='Lates')
    workday = fields.Datetime(string='Date Today', readonly=True)

    @api.onchange('employee_id','check_in')
    def _onchange_employee_id(self):
         for rec in self:
            if (rec.employee_id is not False):
                if (rec.employee_id.work_sched is not False):
                    dow = fields.Date.from_string(rec.check_in).weekday()
                    cnts = rec.employee_id.work_sched.attendance_ids.search([("dayofweek","=",dow),
                    ("calendar_id","=",rec.employee_id.work_sched.id)])
                    # raise Warning(_(cnts))
                    if (cnts):
                        splitTime = str(cnts[0].hour_from).split(".")
                        myHour = int(splitTime[0]) - 8
                        if (len(str(splitTime[1])) <= 1):
                            splitTime[1] = splitTime[1] + "0"
                        myMinute = int((float(splitTime[1]) / 100) * 60 )

                        tz = pytz.timezone('Asia/Manila')
                        check_in = fields.Datetime.from_string(rec.check_in)
                        year = check_in.year
                        month = check_in.month
                        day = check_in.day
        
                        
                        myworkday = datetime(year,month,day,myHour,myMinute,0,0,pytz.UTC)
                        lapse =  fields.Datetime.from_string(rec.check_in).astimezone(pytz.UTC) - myworkday
                        if (lapse.total_seconds() > 0 ):
                            rec.late_in_float = (lapse.total_seconds() / 60)
                            rec.is_tardy = True 
                        rec.workday = myworkday
                    

  
    
    @api.depends('employee_id', 'check_in')
    def _compute_is_tardy(self):
        for rec in self:
            if (rec.employee_id is not False):
                if (rec.employee_id.resource_calendar_id is not False):
                    dow = fields.Date.from_string(rec.check_in).weekday()
                    cnts = rec.employee_id.resource_calendar_id.attendance_ids.search([("dayofweek","=",dow)])
                    # if (cnts):
                        # raise Warning(_(cnts[0].hour_from))
                        # splitTime = str(cnts[0].hour_from).split(".")
                        # myHour = int(splitTime[0]) - 7
                        # myMinute = int(splitTime[1])
                        # myWD = datetime.today().replace(hour=myHour,minute=myMinute,second=0)
                        # rec.workday = myWD
                        # myDate = fields.Datetime.from_string(rec.check_in)
                        
                        # workdate= fields.Datetime.from_string(rec.check_in).replace(hour=myHour)
                        # if (workdate <= myDate):
                        #     rec.late_in_float = (workdate - myDate).total_seconds()

    
   
    
    @api.depends('employee_id', 'check_in')
    def _compute_is_workday(self):
        for rec in self:
            if (rec.employee_id is not False):
                if (rec.employee_id.resource_calendar_id is not False):
                    dow = fields.Date.from_string(rec.check_in).weekday()
                    cnt = rec.employee_id.resource_calendar_id.attendance_ids.search_count([("dayofweek","=",dow)])
                    if (cnt != 0):
                        rec.is_workday = True
        
        return False