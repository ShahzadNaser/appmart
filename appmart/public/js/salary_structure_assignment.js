frappe.ui.form.on('Salary Structure Assignment', {
    refresh:function(frm) {
        frm.set_query('salary_component', 'employee_salary_components', function() {
            if(!frm.doc.salary_structure) {
                frappe.throw(__('Please set Salary Structure'));
            }
            return {
                query: 'appmart.overrides.controllers.salary_structure_assignment.get_components',
                filters: {
                    salary_structure: frm.doc.salary_structure
                }
            };
        });
    }
});