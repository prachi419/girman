frappe.listview_settings['Book'] = {
    onload(listview) {
       
        listview.page.add_inner_button('Import Books from API', () => {
            frappe.prompt([
                {
                    fieldtype: 'Data',
                    label: 'Title Filter',
                    fieldname: 'title_filter'
                },
                {
                    fieldtype: 'Int',
                    label: 'Number of Books',
                    fieldname: 'total_books',
                    default: 20
                }
            ], (values) => {
                frappe.call({
                    method: 'library_management.library_management.api.book_import.import_books_from_api',
                    args: {
                        title_filter: values.title_filter,
                        total_books: values.total_books
                    },
                    callback(r) {
                        frappe.msgprint(r.message);
                        listview.refresh();
                    }
                });
            }, 'Import Books', 'Import');
        });
    }
};
