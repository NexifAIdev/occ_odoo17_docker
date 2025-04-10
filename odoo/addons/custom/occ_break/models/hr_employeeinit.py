# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import pytz

from collections import defaultdict
from datetime import datetime, timedelta
from operator import itemgetter
from pytz import timezone

from odoo.http import request
from odoo import models, fields, api, exceptions, _
from odoo.addons.resource.models.utils import Intervals
from odoo.osv.expression import AND, OR
from odoo.tools.float_utils import float_is_zero
from odoo.exceptions import AccessError, UserError
from odoo.tools import format_duration, format_time, format_datetime


class HrEmployee(models.Model):
	_inherit = "hr.employee"
	
	# BREAK
	
	# end_lunch = fields.Float(string="End Lunch", tracking=True,default=0.0)

	# ADD START LUNCH TO DISPLAY THE START OF LUNCH
	start_lunch = fields.Float(string="Start Lunch", tracking=True,default=0.0)

	# ADD "IS BREAK" TO DETERMINE IF EMPLOYEE IS ON BREAK
	is_break = fields.Boolean()

	# ADD "IS BREAK DONE" TO CHECK
	is_break_done = fields.Boolean(compute="_check_employee_break")


	# TOTAL DURATION OF BREAK HOURS
	total_break_hours = fields.Float()

	@api.depends('attendance_ids.start_lunch', 'attendance_ids.end_lunch')
	def _check_employee_break(self):
		for rec in self:
			attendance = self.env['hr.attendance'].search([('employee_id', '=', rec.id)], order="id desc", limit=1)

			# print("\n\n\n\nChecking Attendance Here!")
			# print(attendance)
			# print(attendance.end_lunch)
			# print(attendance.check_out)
			if attendance.end_lunch and not attendance.check_out:
				rec.is_break_done = True
			else:
				rec.is_break_done = False


	def _attendance_action_change(self, geo_information=None):

		res = super(HrEmployee, self)._attendance_action_change(geo_information=geo_information)
		attendance = self.env['hr.attendance'].search([('employee_id', '=', self.id)], order="id desc", limit=1)
		break_date = fields.Datetime.now()

		print("get attendance ction change")
		print(attendance)
		print(attendance.start_lunch)
		print(attendance.end_lunch)

		if not attendance.end_lunch and attendance.start_lunch:
			attendance.write({
				'end_lunch': break_date,
				'is_break': False,
			})

			self.is_break = False
			self.start_lunch = 0
			

		return res

	def _break_action_change(self):
		""" Check In/Check Out action
			Check In: create a new attendance record
			Check Out: modify check_out field of appropriate attendance record
		"""
		self.ensure_one()
		break_date = fields.Datetime.now()
		attendance = self.env['hr.attendance'].search([('employee_id', '=', self.id), ('check_out', '=', False)], limit=1)
		# employee = self.env['hr.employee'].search([('id', '=', self.id)], limit=1)
		
		if attendance and not attendance.is_break :
			attendance.write({
				'start_lunch': break_date,
				'is_break': True,
			})

			# Add 8 Hours
			start_lunch = attendance.start_lunch + timedelta(hours=8)
			# Extract the time
			time_value = start_lunch.time()
			# Convert time to float hours (hours + minutes/60 + seconds/3600)
			start_hours = time_value.hour + time_value.minute / 60 + time_value.second / 3600
			print("Starting Hours for Employee: ",start_hours)
			self.start_lunch = start_hours


			

		else:
			attendance.write({
				'end_lunch': break_date,
				'is_break': False,
			})


		return attendance