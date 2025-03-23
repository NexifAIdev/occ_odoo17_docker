from odoo import models, fields, api

class HREmployee(models.Model):
    _inherit = "hr.employee"

    system_id = fields.Char("System ID")
    employee_id = fields.Char("Employee ID")
    approver2_id = fields.Many2one('hr.employee', string="Second Approver")
    employee_type2 = fields.Selection(selection=[
        ("rank_and_file","Rank and File"),
        ("manager","Manager"),
        ("officer","Officer"),
        ], string="Employee Type") 
    employment_status = fields.Selection([
        ("regular","Regular"),
        ("maternity","Maternity"),
        ("paternity","Paternity"),
        ("sabbatical","Sabbatical"),
        ("terminated","Terminated"),
        ("resigned","Resigned"),
        ("awol","AWOL"),
        ("probationary","Probationary"),
        ("part_time","Part-time"),
        ("extended_part_time","Extended Part-Time"),
        ("contractual_project_based","Contractual/Project-Based"),
        ("ojt","OJT"),
        ("on_pip","On PIP"),
        ("end_of_contract","End Of Contract"),
        ("ojt_ended","OJT Ended"),           
        ], string ="Employment Status")
    user_type = fields.Selection([
        ("employee","Employee"),
        ("intern_active","Intern(Active)"),
        ("intern_ended","Intern(Ended)"),
    ], string="User Type")
    job_code = fields.Char("Job Code")
    job_grade = fields.Selection([
        ("0","0"),
        ("1","1"),
        ("2","2"),
        ("3","3"),
        ("4","4"),
        ("5","5"),
        ("6","6"),
        ("7","7"),
        ("8","8"),
        ("9","9"),
        ("10","10"),
        ("11","11"),
        ("12","12"),
        ("13","13"),
        ("14","14"),
        ("15","15"),
        ("16","16"),
        ("17","17"),
        ("18","18"),
        ("19","19"),
        ("20","20"),
        ("21","21"),
        ("22","22"),
        ("23","23"),
        ("24","24"),
        ("25","25"),
        ("26","26"),
        ("27","27"),
        ("28","28"),
        ("29","29"),
        ("30","30"),
    ],string="Job Grade")
    client_name = fields.Char("Client Name")
    billability = fields.Selection([
        ("billable","Billable"),
        ("non_billable","Non-Billable")
    ],string="Billability")
    expected_regularization_date = fields.Date("Expected Regularization Date")
    regularization_date = fields.Date("Regularization Date")
    separation_date = fields.Date("Separation Date")
    employee_remarks = fields.Text("Employee Remarks")
    reason_for_leaving = fields.Text("Reason for Leaving")
    biometric_id = fields.Char("Biometric ID")
    approver_id = fields.Many2one("hr.employee", string="Approver")

    #Government Details
    sss_no = fields.Char("SSS No:")
    tin = fields.Char("TIN:")
    philhealth_no = fields.Char("PhilHealth No.:")
    hdmf_no = fields.Char("HDMF No.:")
    prc_license_no = fields.Char("PRC License No.:")
    passport_no = fields.Char("Passport No.:")
    rdo_no = fields.Char("RDO No.:")


    #Emergency Contact Details
    emergency_relation = fields.Char("Relationship")
    emergency_address = fields.Char("Address")

    work_schedule_ids = fields.One2many(
        related='resource_calendar_id.attendance_ids',
        help="Work schedule of the employee")
    
    marital = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('cohabitant', 'Legal Cohabitant'),
        ('widower', 'Widower'),
        ('widowed', 'Widowed'),
        ('divorced', 'Divorced'),
        ('separated','Separated')
    ], string='Marital Status', groups="hr.group_hr_user", default='single', tracking=True)
    employee_type = fields.Selection([
            ('rankandfile', 'Rank and file'),
            ('officer', 'Officer'),
            ('manager', 'Manager'),
            ('employee', 'Employee'),
            ('student', 'Student'),
            ('trainee', 'Trainee'),
            ('contractor', 'Contractor'),
            ('freelance', 'Freelancer'),
        ], string='Employee Type', default='employee', required=True, groups="hr.group_hr_user",
        help="The employee type. Although the primary purpose may seem to categorize employees, this field has also an impact in the Contract History. Only Employee type is supposed to be under contract and will have a Contract History.")
