from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.item import Item

items_bp = Blueprint("items", __name__)

@items_bp.route("", methods=["GET"])
@jwt_required()
def get_items():
    items = Item.query.filter_by(user_id=int(get_jwt_identity())).all()
    return jsonify([i.to_dict() for i in items]), 200

@items_bp.route("/<int:item_id>", methods=["GET"])
@jwt_required()
def get_item(item_id):
    item = Item.query.filter_by(id=item_id, user_id=int(get_jwt_identity())).first_or_404()
    return jsonify(item.to_dict()), 200

@items_bp.route("", methods=["POST"])
@jwt_required()
def create_item():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Le champ 'name' est requis"}), 400
    item = Item(name=data["name"], description=data.get("description"),
                price=data.get("price", 0.0), user_id=int(get_jwt_identity()))
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

@items_bp.route("/<int:item_id>", methods=["PUT"])
@jwt_required()
def update_item(item_id):
    item = Item.query.filter_by(id=item_id, user_id=int(get_jwt_identity())).first_or_404()
    data = request.get_json()
    item.name = data.get("name", item.name)
    item.description = data.get("description", item.description)
    item.price = data.get("price", item.price)
    item.in_stock = data.get("in_stock", item.in_stock)
    db.session.commit()
    return jsonify(item.to_dict()), 200

@items_bp.route("/<int:item_id>", methods=["DELETE"])
@jwt_required()
def delete_item(item_id):
    item = Item.query.filter_by(id=item_id, user_id=int(get_jwt_identity())).first_or_404()
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Supprimé"}), 200
