
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { markup } from "@odoo/owl";
import { stepUtils } from "@web_tour/tour_service/tour_utils";

registry.category("web_tour.tours").add('hostel_tour',  {
    url: "/odoo",
    steps: () => [
        stepUtils.showAppsMenuItem(),
        {
            trigger: '.o_app[data-menu-xmlid="my_hostel.hostel_base_menu"]',
            content: markup(_t("Ready to launch your <b>hostel</b>?")),
            tooltipPosition: 'bottom',
            run: "click",
        },
        {
            trigger: '.o_list_button_add',
            content: markup(_t("Let's create new room.")),
            tooltipPosition: "bottom",
            run: "click",
        },
        {
            trigger: '.o_form_button_save',
            content: markup(_t('Save this room record')),
            tooltipPosition: "bottom",
            run: "click",
        },
    ]

});