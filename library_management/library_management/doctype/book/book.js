// frappe.listview_settings['Book'] = {
//     onload: function(listview) {
//         listview.page.add_field({
//             label: 'Search by Title or Author',
//             fieldtype: 'Data',
//             fieldname: 'search_book',
//             onchange: function() {
//                 const value = listview.page.fields_dict.search_book.get_value();
//                 if (value) {
//                     listview.filter_area.add([[["Book", "title", "like", `%${value}%`], "or", ["Book", "author", "like", `%${value}%`]]]);
//                 }
//             }
//         });
//     }
// };
