import { xml } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { renderToElement } from "@web/core/utils/render";
import { Interaction } from "@web/public/interaction";

export class HostelSnippet extends Interaction {
    static selector = ".hostel_snippet";

    setup() {
        const rowCount = Number.parseInt(this.el.dataset.numberOfHostels || "5", 10);
        this.rows = Number.isNaN(rowCount) ? 5 : rowCount;
        this.hostels = [];
    }

    async willStart() {
        const hostels = await this.waitFor(
            rpc("/hostel_hostel/search_read", {
                fields: ["name", "hostel_code"],
            })
        );
        this.hostels = hostels.slice(0, this.rows);
    }

    start() {
        const tableBody = renderToElement(
            xml`<tbody class="hostel_snippet_rows">
                <t t-foreach="hostels" t-as="hostel" t-key="hostel.hostel_code || hostel.name">
                    <tr>
                        <td t-esc="hostel.name"/>
                        <td t-esc="hostel.hostel_code"/>
                    </tr>
                </t>
            </tbody>`,
            { hostels: this.hostels }
        );
        this.el.querySelector(".hostel_snippet_rows")?.replaceWith(tableBody);
    }
}

registry.category("public.interactions").add("my_hostel.hostel_snippet", HostelSnippet);
