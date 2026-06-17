const {  Component, mount, xml, whenReady } = owl;

console.log("Load component......");

class MyComponent extends Component {
    static template = xml`
        <div class="bg-info text-white text-center p-3">
            <b> Welcome To Odoo </b>
            <i class="fa fa-close p-1 float-end"
               style="cursor: pointer;"
               t-on-click="onRemove"> </i>
        </div>`
    onRemove(ev) {
        ev.target.closest('div').remove();
    }
}

whenReady().then(() => {
    mount(MyComponent, document.body);
});

