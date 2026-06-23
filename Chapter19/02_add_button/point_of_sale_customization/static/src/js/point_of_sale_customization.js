import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";

patch(ControlButtons.prototype, {
    async clickCustomDiscount() {
        const order = this.pos.getOrder();
        let selected_orderline = order.getSelectedOrderline();
        if (selected_orderline) {
            selected_orderline.setDiscount(5);
        }
    }
});

