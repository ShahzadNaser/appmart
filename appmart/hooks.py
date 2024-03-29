from . import __version__ as app_version

app_name = "appmart"
app_title = "Appmart"
app_publisher = "Shahzad Naser"
app_description = "appmart"
app_email = "shahzadnaser1122@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/appmart/css/appmart.css"
# app_include_js = "/assets/appmart/js/appmart.js"

# include js, css files in header of web template
# web_include_css = "/assets/appmart/css/appmart.css"
# web_include_js = "/assets/appmart/js/appmart.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "appmart/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Salary Structure Assignment" : "public/js/salary_structure_assignment.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "appmart.utils.jinja_methods",
#	"filters": "appmart.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "appmart.install.before_install"
# after_install = "appmart.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "appmart.uninstall.before_uninstall"
# after_uninstall = "appmart.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "appmart.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes
override_doctype_class = {
	"Salary Slip": "appmart.overrides.controllers.salary_slip.CustomSalarySlip",
	"Payroll Entry": "appmart.overrides.controllers.payroll_entry.CustomPayrollEntry",
}
# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Salary Structure Assignment": {
		"before_save": "appmart.overrides.controllers.salary_structure_assignment.before_save",
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"appmart.tasks.all"
#	],
#	"daily": [
#		"appmart.tasks.daily"
#	],
#	"hourly": [
#		"appmart.tasks.hourly"
#	],
#	"weekly": [
#		"appmart.tasks.weekly"
#	],
#	"monthly": [
#		"appmart.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "appmart.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "appmart.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "appmart.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"appmart.auth.validate"
# ]
