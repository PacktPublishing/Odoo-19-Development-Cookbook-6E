const { Component, mount, xml , whenReady, useState } = owl;

console.log("Load component......");

class MyComponent extends Component {
    static template = xml`
        <div class="bg-info text-white text-center p-3">
            <i class="fa fa-arrow-left p-1"
               style="cursor: pointer;"
               t-on-click="onPrevious"> </i>
            <b t-esc="messageList[Math.abs(state.currentIndex%4)]"/>
            <i class="fa fa-arrow-right p-1"
               style="cursor: pointer;"
               t-on-click="onNext"> </i>
            <i class="fa fa-close p-1 float-end"
               style="cursor: pointer;" 
               t-on-click="onRemove"> </i>
        </div>`
    setup() {
        this.messageList = [
            'Hello World',
            'Welcome to Odoo',
            'Odoo is awesome',
            'You are awesome too'
        ];
        this.state = useState({ currentIndex: 0 });
    }
    onRemove(ev) {
        ev.target.closest('div').remove();
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

