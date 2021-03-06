"""The meetup routes"""

from flask import jsonify, request , make_response , abort
from app.admin.models import MeetupModel, MEETUPS_LEN
from app.api.v1 import path_1 

@path_1.route("/meetups", methods=['POST'])
def admin_create_meetup():
    """
    POST a meetup : POST admin/meetups
    """
    try:
        topic = request.get_json()['topic']
        happenningOn = request.get_json()['happenningOn']
        location = request.get_json()['location']
        images = request.get_json()['images']
        tags = request.get_json()['tags']

#return error message with the corresponding status code
    except:
        return jsonify({'status':400,
                        'error': 'Check the json keys you have used very well'}), 400

    if not topic:
        return jsonify({'status':400, 'error':'Provide the topic field'}), 400
    if not happenningOn:
        return jsonify({'status':400, 'error':'provide the meetup date'}), 400

    if not location:
        return jsonify({'status':400, 'error':'provide the location'}), 400

    if not tags:
        return jsonify({'status':400, 'error':'provide the tags'}), 400

    meetup = MeetupModel(
        topic=topic,
        happenningOn=happenningOn,
        location=location,
        images=images,
        tags=tags
    )
    meetup.save_meetup_record()

    #return a jsonify string with an OK status
    return jsonify({"status": 201,
                    "data": [{"topic": topic,
                              "location": location,
                              "happenningOn": happenningOn,
                              "images": images,
                              "tags": tags}]}), 201

#user gets a specific meetup record
@path_1.route("/meetups/<int:meetup_id>", methods=["GET"])
def get_specific_meetup(meetup_id):
    """
     Get a speific meetup record
    """
    meetup = MeetupModel.get_specific_meetup(meetup_id)
    if meetup:
        return jsonify({"status": 200, "data": meetup}), 200
    return jsonify({"status": 404, "data": "Meetup not found"}), 404

#User get all upcoming meetup records
@path_1.route("/meetups/upcoming", methods=["GET"])
def get_all_upcoming_meetups():
    meetups = MeetupModel.get_all_upcoming_meetups()

    if meetups:
        return jsonify({"status": 200, "data": meetups}), 200
    return jsonify({
        "status": 404,
        "error": "No upcoming meetups available."
    }), 404

#user respond to a meetup request
@path_1.route("/meetups/<int:meetup_id>/rsvps/<resp>", methods=['POST'])
def meetup_rsvp(meetup_id, resp):
    """
    A user can respond to a meetup rsvp
    """
    if resp not in ["yes", "no", "maybe"]:
        return jsonify({
            'status':400,
            'error':'Response should be either yes, no or maybe'}), 400

    meetup = MeetupModel.get_specific_meetup(meetup_id)
    if not meetup:
        return jsonify({
            'status': 404,
            'error':'Meetup with id {} not found'.format(meetup_id)}), 404

    meetup = meetup[0]
    return jsonify({'status':200, 'data':[{'meetup':meetup_id,
                                           'topic':meetup['topic'],
                                           'Attending':resp}]}), 200 
#admin delete meetup
@path_1.route("/meetups/<int:meetup_id>", methods=['DELETE'])
def admin_delete_a_meetup(meetup_id):
    deleted = MeetupModel.delete_specific_meetup(meetup_id)
    if deleted:
        return jsonify({'status': 200, 'data':"Deleted successfully"}), 200
    return jsonify({'status': 404, 'data':"Meetup with id {} not found".format(meetup_id)}), 404