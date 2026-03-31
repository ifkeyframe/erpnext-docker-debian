app_name = "printbiz_custom"
app_title = "PrintBiz Custom"
app_publisher = "PrintBiz"
app_description = "Custom app for PrintBiz warehouse and production management"
app_email = "admin@printbiz.local"
app_license = "MIT"
app_version = "0.1.0"

# Required for frappe
required_apps = ["frappe", "erpnext"]

# Fixtures — auto-exported/imported on install and migrate
# These allow customizations to be version-controlled
fixtures = [
    {
        "dt": "Custom Field",
        "filters": [["module", "=", "PrintBiz"]],
    },
    {
        "dt": "Property Setter",
        "filters": [["module", "=", "PrintBiz"]],
    },
]

# -----------------------------------------------
# Hooks for future expansion (currently unused)
# -----------------------------------------------

# doc_events = {
#     "Stock Entry": {
#         "on_submit": "printbiz_custom.printbiz.events.stock_entry.on_submit",
#     },
#     "Sales Order": {
#         "on_submit": "printbiz_custom.printbiz.events.sales_order.on_submit",
#     },
# }

# scheduler_events = {
#     "daily": [
#         "printbiz_custom.printbiz.tasks.daily_stock_report",
#     ],
# }

# override_whitelisted_methods = {}

# jenv = {
#     "methods": [],
# }
