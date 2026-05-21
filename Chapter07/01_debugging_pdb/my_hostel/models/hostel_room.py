# -*- coding: utf-8 -*-
import logging
import base64
from odoo import models, fields, api, exceptions

_logger = logging.getLogger(__name__)


class HostelRoom(models.Model):
    _name = "hostel.room"
    _description = "Hostel Room"

    # =========================
    # FIELDS
    # =========================
    name = fields.Char(string="Room Name", required=True)
    room_no = fields.Char(string="Room Number", required=True)
    description = fields.Html(string="Description")
    other_info = fields.Text(string="Other Info")
    room_rating = fields.Float(string="Rating")
    state = fields.Selection(
        [("draft", "Unavailable"), ("available", "Available"), ("closed", "Closed")],
        default="draft",
        string="Status",
    )

    # =========================
    # EXPORT METHOD (ATTACHMENT)
    # =========================
    def export_available_rooms(self):
        _logger.info("Starting export of available hostel rooms")
        # Fetch available rooms
        rooms = self.search([("state", "=", "available")])
        _logger.debug("Found %d available rooms", len(rooms))

        try:
            content = ""

            for room in rooms:
                _logger.debug(
                    "Writing Room: %s | Number: %s | Rating: %s",
                    room.name,
                    room.room_no,
                    room.room_rating,
                )

                content += "%s\t%s\t%f\n" % (
                    room.name,
                    room.room_no,
                    room.room_rating or 0.0,
                )

            # Convert to binary
            file_data = base64.b64encode(content.encode())

            # Create attachment
            attachment = self.env["ir.attachment"].create(
                {
                    "name": "available_rooms.txt",
                    "type": "binary",
                    "datas": file_data,
                    "res_model": "hostel.room",
                    "res_id": self.id if self else False,
                    "mimetype": "text/plain",
                }
            )

            _logger.info("Attachment created: ID %s", attachment.id)

            # Return download action
            return {
                "type": "ir.actions.act_url",
                "url": "/web/content/%s?download=true" % attachment.id,
                "target": "self",
            }

        except Exception as e:
            _logger.exception("Error while exporting rooms")
            raise exceptions.UserError("Unable to export room data!")
