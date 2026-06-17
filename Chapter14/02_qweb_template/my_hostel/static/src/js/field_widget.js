import { Component,useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { renderToElement } from "@web/core/utils/render";

export class CategColorField extends Component {
    setup() {
        this.totalColors = [1,2,3,4,5,6];
        this.categInformationPanel = useRef('categInformationPanel');
        super.setup();
    }
    clickPill(value) {
        this.props.record.update({ [this.props.name]: value });
    }
    categInfo(value){
        this.categInformationPanel.el.replaceChildren((renderToElement("my_hostel.CategInformation",{
            value: value,
            'widget': this
        })));
    }
}
CategColorField.template = "CategColorField";
CategColorField.supportedTypes = ["integer"];
registry.category("fields").add("category_color", {
    component: CategColorField,
});

