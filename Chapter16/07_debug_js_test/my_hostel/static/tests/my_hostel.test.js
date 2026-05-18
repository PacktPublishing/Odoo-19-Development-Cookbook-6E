import { expect, test} from "@odoo/hoot";
import { queryAll, queryFirst } from "@odoo/hoot-dom";
import { defineModels, fields, models, mountView} from "@web/../tests/web_test_helpers";


class HostelRoomMember extends models.ServerModel{

    _name = 'hostel.room.member'
    _inherits = {'res.partner': 'partner_id'}
    _description = "Hostel Room member"

    partner_id = fields.Many2one({ relation: "res.partner" ,ondelete:'cascade'})
    date_start = fields.Date()
    date_end = fields.Date()
    member_number = fields.Char()
    date_of_birth = fields.Date()

}


class HostelRoom extends models.ServerModel {
    _name = "hostel.room";

    name = fields.Char({string: "Hostel Name", required:true })
    room_no = fields.Char({string: "Room number", required:true })
    other_info = fields.Text()
    description = fields.Html()
    room_rating = fields.Float()
    member_ids = fields.Many2many({ string: "Members", relation: "hostel.room.member" })
    state = fields.Selection(
    {
        string: "State",
        selection: [
            ["draft", "Unavailable"],
            ["available", "Available"],
            ["closed", "Closed"],
        ],
        default:"draft"
    })
    color = fields.Integer()

    _records = [
        {
            id: 1,
            name: "Hostel Room 01",
            room_no: "101",
            color: 1,
            state:"draft",
        },
        {
            id: 2,
            name: "Hostel Room 02",
            room_no: "102",
            color: 3,
            state:"available",
        },
    ];

    _views = {
        form: /* xml */ `
            <form>
                <header>
                    <button name="make_available" string="Make Available" type="object"/>
                    <button name="make_closed"  string="Make Closed" type="object"/>
                    <field name="state" widget="statusbar"/>
                </header>
                <group>
                    <group>
                        <field name="name"/>
                        <field name="room_no"/>
                        <field name="color" widget="int_color"/>
                    </group>
                    <group>
                        <field name="description"/>
                        <field name="member_ids" widget="many2many_tags"/>
                    </group>
                </group>
            </form>
        `,
    };


}
defineModels([HostelRoom,HostelRoomMember]);


test("MyHostel perform operations", async () => {
    await mountView({
        type: "form",
        resModel: "hostel.room",
        resId: 2,
    });
    const color_pill = ".o_int_color .o_color_pill";
    const colorPills = queryAll(color_pill);
    expect(colorPills.length).toEqual(10.00);
});
