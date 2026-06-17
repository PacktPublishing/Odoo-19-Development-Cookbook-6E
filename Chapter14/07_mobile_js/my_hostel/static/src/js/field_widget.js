import { Component, onWillStart , onWillRender, useRef} from "@odoo/owl";
import { registry } from "@web/core/registry";
import { renderToElement } from "@web/core/utils/render";
import mobile from "@web_mobile/js/services/core";

export class CategColorField extends Component {
    setup() {
        this.totalColors = [1,2,3,4,5,6];
        this.categInformationPanel = useRef('categInformationPanel');
        onWillStart(() => {
            this.loadCategInformation();
        });
        onWillRender(() => {
            this.loadCategInformation();
        });
        super.setup();
    }
    clickPill(value) {
        if (mobile.methods.showToast) {
            mobile.methods.showToast({ 'message': 'Color changed' });
        }
        this.props.record.update({ [this.props.name]: value });
    }
    categInfo(value){
        this.categInformationPanel.el.replaceChildren((renderToElement("my_hostel.CategInformation",{
            value: value,
            'widget': this
        })));
    }
    async loadCategInformation() {
        var self = this;
        self.categoryInfo = {};
        var resModel = self.env.model.root.resModel;
        var domain = [];
        var fields = ['category'];
        var groupby = ['category'];
        const categInfoPromise = await self.env.services.orm.call(
            resModel,
            "read_group",
            [],
            {
                domain,
                fields,
                groupby,
            }
        );
        categInfoPromise.map((info) => {
            self.categoryInfo[info.category] = info.category_count;
        });
    }
}
CategColorField.template = "CategColorField";
CategColorField.supportedTypes = ["integer"];
registry.category("fields").add("category_color", {
    component: CategColorField,
});

