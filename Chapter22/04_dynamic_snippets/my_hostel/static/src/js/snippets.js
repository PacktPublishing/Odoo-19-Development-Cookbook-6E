import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.HostelSnippet = publicWidget.Widget.extend({
    selector: '.hostel_snippet',
    disabledInEditableMode: false,
    start: async function () {
        var self = this;
        var rows = this.$el[0].dataset.numberOfRooms || '5';
        self.$el.find('td').parents('tr').remove();
        const hostels = await rpc("/hostel_hostel/search_read", {
            fields: ['name', 'hostel_code'],
        });
        for (const hostel of hostels) {
            self.$el.append(
                $('<tr />').append(
                    $('<td />').text(hostel.name),
                    $('<td />').text(hostel.hostel_code)
                )
            );
        }
    }
});