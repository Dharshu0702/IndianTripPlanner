"""Email notification service using Flask-Mail."""

from flask import current_app
from flask_mail import Message

from app import mail


def send_booking_notification_to_admin(booking, trip, user):
    """Send email to admin when a new booking is created."""
    try:
        admin_email = current_app.config.get("ADMIN_EMAIL", "")
        if not admin_email:
            current_app.logger.warning("ADMIN_EMAIL not configured, skipping notification")
            return False

        destination = trip["destination"]
        msg = Message(
            subject=f"🆕 New Booking Request - {destination['place']}, {destination['state']}",
            recipients=[admin_email],
        )

        msg.html = f"""
        <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #4F46E5, #7C3AED); padding: 30px; border-radius: 12px 12px 0 0;">
                <h1 style="color: white; margin: 0; font-size: 24px;">🏖️ India Smart Trip Planner</h1>
                <p style="color: #E0E7FF; margin: 5px 0 0;">New Booking Request</p>
            </div>

            <div style="background: #f8f9fa; padding: 25px; border: 1px solid #e0e0e0;">
                <h2 style="color: #1a1a2e; margin-top: 0;">Booking Details</h2>

                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="padding: 8px 0; color: #666; width: 40%;">👤 Traveler</td>
                        <td style="padding: 8px 0; font-weight: 600;">{user['name']} ({user['email']})</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #666;">📍 Origin</td>
                        <td style="padding: 8px 0; font-weight: 600;">{trip['origin_location'].get('address', 'N/A')}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #666;">🎯 Destination</td>
                        <td style="padding: 8px 0; font-weight: 600;">{destination['place']}, {destination['state']}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #666;">👥 Travelers</td>
                        <td style="padding: 8px 0; font-weight: 600;">{trip['inputs']['travelers']}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #666;">📅 Days</td>
                        <td style="padding: 8px 0; font-weight: 600;">{trip['inputs']['days']}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #666;">🏷️ Plan</td>
                        <td style="padding: 8px 0; font-weight: 600;">{booking['selected_plan'].get('plan_name', 'N/A')}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #666;">💰 Total Cost</td>
                        <td style="padding: 8px 0; font-weight: 600; color: #059669;">
                            ₹{booking['selected_plan'].get('total_cost', 0):,.0f}
                        </td>
                    </tr>
                </table>

                <div style="margin-top: 20px; padding: 15px; background: #FFF3CD; border-radius: 8px; border-left: 4px solid #FFC107;">
                    <p style="margin: 0; color: #856404;">
                        ⏳ <strong>Action Required:</strong> Please review and approve/reject this booking from the admin dashboard.
                    </p>
                </div>
            </div>

            <div style="background: #1a1a2e; padding: 15px; border-radius: 0 0 12px 12px; text-align: center;">
                <p style="color: #888; margin: 0; font-size: 12px;">India Smart Trip Planner — AI-powered travel planning</p>
            </div>
        </div>
        """

        mail.send(msg)
        current_app.logger.info(f"Booking notification sent to {admin_email}")
        return True

    except Exception as e:
        current_app.logger.error(f"Failed to send booking email: {e}")
        return False


def send_booking_status_update(user_email, user_name, booking, trip, status):
    """Send email to user when booking status is updated."""
    try:
        destination = trip["destination"]
        status_emoji = "✅" if status == "approved" else "❌"
        status_color = "#059669" if status == "approved" else "#DC2626"
        status_text = "Approved" if status == "approved" else "Rejected"

        msg = Message(
            subject=f"{status_emoji} Booking {status_text} - {destination['place']}, {destination['state']}",
            recipients=[user_email],
        )

        msg.html = f"""
        <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #4F46E5, #7C3AED); padding: 30px; border-radius: 12px 12px 0 0;">
                <h1 style="color: white; margin: 0; font-size: 24px;">🏖️ India Smart Trip Planner</h1>
                <p style="color: #E0E7FF; margin: 5px 0 0;">Booking Status Update</p>
            </div>

            <div style="background: #f8f9fa; padding: 25px; border: 1px solid #e0e0e0;">
                <h2 style="color: #1a1a2e; margin-top: 0;">Hello {user_name}! 👋</h2>

                <div style="text-align: center; padding: 20px; margin: 15px 0; background: white; border-radius: 12px; border: 2px solid {status_color};">
                    <p style="font-size: 48px; margin: 0;">{status_emoji}</p>
                    <h3 style="color: {status_color}; margin: 10px 0 5px;">Booking {status_text}</h3>
                    <p style="color: #666; margin: 0;">
                        {destination['place']}, {destination['state']}
                    </p>
                </div>

                <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
                    <tr>
                        <td style="padding: 8px 0; color: #666;">🏷️ Plan</td>
                        <td style="padding: 8px 0; font-weight: 600;">{booking['selected_plan'].get('plan_name', 'N/A')}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #666;">💰 Total</td>
                        <td style="padding: 8px 0; font-weight: 600;">₹{booking['selected_plan'].get('total_cost', 0):,.0f}</td>
                    </tr>
                </table>

                {"<p style='margin-top: 15px; color: #666;'><strong>Admin Notes:</strong> " + booking.get('admin_notes', '') + "</p>" if booking.get('admin_notes') else ""}

                {"<p style='margin-top: 15px;'>🎉 Your trip is confirmed! You can download your detailed itinerary PDF from the app.</p>" if status == "approved" else "<p style='margin-top: 15px;'>We're sorry your booking wasn't approved this time. Please try modifying your plan or contact support.</p>"}
            </div>

            <div style="background: #1a1a2e; padding: 15px; border-radius: 0 0 12px 12px; text-align: center;">
                <p style="color: #888; margin: 0; font-size: 12px;">India Smart Trip Planner — AI-powered travel planning</p>
            </div>
        </div>
        """

        mail.send(msg)
        current_app.logger.info(f"Status update email sent to {user_email}")
        return True

    except Exception as e:
        current_app.logger.error(f"Failed to send status email: {e}")
        return False
