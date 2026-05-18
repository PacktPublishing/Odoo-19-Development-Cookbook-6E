import { Plugin } from "@html_editor/plugin";
import { registry } from "@web/core/registry";


class HostelSnippetOptionPlugin extends Plugin {
    static id = "HostelSnippetOption";
    resources = {
        builder_options: {
            template: "my_hostel.HostelSnippetOption",
            selector: ".hostel_snippet",
        },
    };
}

registry.category("builder-plugins").add(HostelSnippetOptionPlugin.id, HostelSnippetOptionPlugin);
