import { _t } from "@web/core/l10n/translation";
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.MyHostel = publicWidget.Widget.extend({
    selector: '#wrapwrap',
    init() {
        this._super(...arguments);
        alert(_t('Hello world'));
    }
});