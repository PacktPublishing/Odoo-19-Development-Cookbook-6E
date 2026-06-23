const { 
    Component,
    mount,
    xml,
    useState,
    whenReady,
    onWillStart,
    onWillRender,
    onRendered,
    onMounted,
    onWillUpdateProps,
    onWillPatch,
    onPatched,
    onWillUnmount,
    onWillDestroy,
    onError,
} = owl;

console.log("Load component......");

class MyComponent extends Component {
    static template = xml`
        <div class="bg-info text-white text-center p-3">
            <i class="fa fa-arrow-left p-1"
               style="cursor: pointer;"
               t-on-click="onPrevious"> </i>
            <b t-esc="messageList[((state.currentIndex % messageList.length) + messageList.length) % messageList.length]"/>
            <i class="fa fa-arrow-right p-1"
               style="cursor: pointer;"
               t-on-click="onNext"> </i>
            <i class="fa fa-close p-1 float-end"
               style="cursor: pointer;" 
               t-on-click="onRemove"> </i>
        </div>`
    setup() {
        this.messageList = [
            "Hello World",
            "Welcome to Odoo",
            "Odoo is awesome",
            "You are awesome too"
        ];
        this.state = useState({ currentIndex: 0 });
        onWillStart(() => {
            console.log("CALLED: onWillStart");
        });
        onWillRender(() => {
            console.log("CALLED: onWillRender");
        });
        onRendered(() => {
            console.log("CALLED: onRendered");
        });
        onMounted(() => {
            console.log("CALLED: onMounted");
        });
        onWillUpdateProps(() => {
            console.log("CALLED: onWillUpdateProps");
        });
        onWillPatch(() => {
            console.log("CALLED: onWillPatch");
        });
        onPatched(() => {
            console.log("CALLED: onPatched");
        });
        onWillUnmount(() => {
            console.log("CALLED: onWillUnmount");
        });
        onWillDestroy(() => {
            console.log("CALLED: onWillDestroy");
        });
        onError(() => {
            console.log("CALLED: onError");
        });
    }
    onRemove(ev) {
        ev.target.closest("div").remove();
    }
    onNext(ev) {
        this.state.currentIndex++;
    }
    onPrevious(ev) {
        this.state.currentIndex--;
    }
}

whenReady().then(() => {
    mount(MyComponent, document.body);
});
