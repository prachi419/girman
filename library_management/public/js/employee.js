frappe.ui.form.on('Employee', {
    refresh: function(frm) {
        if(frm.doc.relieving_date) {
            frm.add_custom_button(__('Experience Letter'), function() {
                
                // Dynamically load jsPDF if not already loaded
                if (typeof window.jspdf === "undefined") {
                    let script = document.createElement('script');
                    script.src = "https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js";
                    script.onload = generatePDF; // call generatePDF after jsPDF loads
                    document.head.appendChild(script);
                } else {
                    generatePDF();
                }

                function generatePDF() {
                    const { jsPDF } = window.jspdf;
                    const doc = new jsPDF();

                    const employee_name = frm.doc.employee_name || frm.doc.name;
                    const joining_date = frm.doc.date_of_joining || 'N/A';
                    const relieving_date = frm.doc.relieving_date;
                    const designation = frm.doc.designation || 'N/A';
                    const company_name = frappe.boot.sysdefaults.company || 'Your Company';

                    let content = `
Experience Letter

This is to certify that ${frm.doc.employee_name} was employed with us from
${frm.doc.date_of_joining} to ${frm.doc.relieving_date}.

During this period, ${frm.doc.employee_name} worked as ${frm.doc.designation}
and contributed sincerely to the organization.

We wish ${frm.doc.employee_name} all the best for future endeavors.
`;

                    doc.text(content, 20, 30);
                    doc.save(`${employee_name}_Experience_Letter.pdf`);
                }
            });
        }
    }
});
