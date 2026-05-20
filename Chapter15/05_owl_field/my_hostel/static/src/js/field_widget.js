import { Component, onWillStart , onWillRender} from "@odoo/owl";
import { registry } from "@web/core/registry";

class ColorPill extends Component {
    static template = 'OWLColorPill';
    pillClicked() {
        this.props.onClickColorUpdated(this.props.color);
    }
}

export class OWLCategColorField extends Component {
    static supportedFieldTypes = ["integer"];
    static template = "OWLFieldColorPills";
    static components = { ColorPill };
    setup() {
        this.totalColors = [1,2,3,4,5,6];
        this.categoryInfo = {};
        onWillStart(async() => {
            await this.loadCategInformation();
        });
    }
    colorUpdated(value) {
        this.props.record.update({ [this.props.name]: value });
    }
    async loadCategInformation() {
        const self = this;
        const resModel = self.env.model.root.resModel;
        const categInfoPromise = await self.env.services.orm.call(
            resModel,
            "web_read_group",
            [],
            {
                domain: [],
                aggregates: ["__count"], 
                groupby: ["category"],
            }
        );
        const groups = categInfoPromise.groups;
        groups.forEach((group) => {
            self.categoryInfo[group.category] = group.__count;
        });
    }
}

registry.category("fields").add("category_color", {
    component: OWLCategColorField,
});
