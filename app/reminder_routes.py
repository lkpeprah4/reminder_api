from flask import Blueprint, jsonify ,request
from .models import db,Reminders
from flask_jwt_extended import  jwt_required,get_jwt_identity
from datetime import datetime

reminder_bp=Blueprint("reminder_bp", __name__ ,url_prefix="/reminders")


@reminder_bp.route("/protect", methods=["GET"])
@jwt_required()
def protect():
    user_id = get_jwt_identity()
    return jsonify({"msg": f"Hello user {user_id}, you are logged in!"}), 200

@reminder_bp.route("/" , methods=["POST"])
@jwt_required()
def create_reminder():
    data=request.get_json()
    message=data.get("message")
    schedule_time_str=data.get("schedule_time")
    repeat_frequency=data.get("repeat_frequency")
    
    user_id = get_jwt_identity()

    try:
     schedule_time = datetime.strptime(schedule_time_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
      return jsonify({"msg": "Invalid datetime format. Use YYYY-MM-DD HH:MM:SS"}), 400


    if not message:
        return jsonify({"msg":"MESSAGE FIELD IS REQUIRED"}),400
    if not schedule_time:
        return jsonify({"msg":"TIME FIELD IS REQUIRED"}),400

    
    new_reminder=Reminders(user_id=user_id,message=message, schedule_time=schedule_time, repeat_frequency=repeat_frequency)
    
    db.session.add(new_reminder)
    db.session.commit()

    return jsonify({
    "msg": "Reminder created successfully",
    "reminder": {
        "id": new_reminder.id,
        "message": new_reminder.message,
        "schedule_time": new_reminder.schedule_time.isoformat(),
        "repeat_frequency": new_reminder.repeat_frequency,
        "user_id": new_reminder.user_id
    }
}), 201


@reminder_bp.route("/", methods=["GET"])
@jwt_required()
def get_reminders():
    user_id=get_jwt_identity()

    all_reminders= Reminders.query.filter_by(user_id=user_id).all()

    results= [
        {
            "id":reminder.id,
            "message":reminder.message,
            "schedule_time":reminder.schedule_time,
            "repeat_frequency":reminder.repeat_frequency,
            "created_at":reminder.created_at,
            "updated_at":reminder.updated_at,
            "user_id":reminder.user_id
        }
        for reminder in all_reminders]
    return jsonify({"REMINDERS":results}),200

@reminder_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_single_reminder(id):
    user_id=get_jwt_identity()

    single_reminder=Reminders.query.filter_by(id=id, user_id=user_id).first()

    if not single_reminder:
        return jsonify({"msg": "Reminder not found"}), 404

    results= [
        {
            "id":single_reminder.id,
            "message":single_reminder.message,
            "schedule_time":single_reminder.schedule_time,
            "repeat_frequency":single_reminder.repeat_frequency,
            "created_at":single_reminder.created_at,
            "updated_at":single_reminder.updated_at,
            "user_id":single_reminder.user_id
        }
        ]
    
    return jsonify({"REMINDER": results}),200

@reminder_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_reminder(id):
    user_id=get_jwt_identity()

    reminder=Reminders.query.filter_by(id=id,user_id=user_id).first()
    if not reminder:
        return jsonify({"msg": "Reminder not found"}), 404

    data = request.get_json()
    message=data.get("message")
    schedule_time=data.get("schedule_time")
    repeat_frequency=data.get("repeat_frequency")

    if message:
        reminder.message = message
    if schedule_time:
        try:
           reminder.schedule_time = datetime.strptime(schedule_time, "%Y-%m-%d %H:%M:%S")
        except:
            return jsonify({"msg": "TIME FORMAT MUST BE YYYY-MM-DD HH:MM:SS"}), 400
    if repeat_frequency:
        reminder.repeat_frequency = repeat_frequency
        
    db.session.commit()

    result = {
        "id": reminder.id,
        "message": reminder.message,
        "schedule_time": reminder.schedule_time.strftime("%Y-%m-%d %H:%M:%S"),
        "repeat_frequency": reminder.repeat_frequency,
        "created_at": reminder.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": reminder.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": reminder.user_id
    }

    return jsonify({"REMINDER_UPDATED": result}), 200

@reminder_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_reminder(id):
    user_id = get_jwt_identity()

    reminder=Reminders.query.filter_by(id=id,user_id=user_id).first()
    if not reminder:
        return jsonify({"msg": "Reminder not found"}), 404
    
    db.session.delete(reminder) 
    db.session.commit()

    return jsonify({"msg":"DELETED SUCESSFULLY"}),200

