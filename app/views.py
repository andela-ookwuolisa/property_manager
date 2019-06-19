from flask import request, session, jsonify
from app import my_app, db
from .models import User, Owner, Tenant, Property
from .utils import login_required, ValidationError


def check_instance(Obj, obj_id, name):
    obj = db.query(Obj).filter(Obj.id == obj_id).first()
    if not obj:
        err = f"No {name} with the id {obj_id}"
        raise ValidationError(err)
    return obj


@my_app.route("/")
def index():
    data = "Welcome to property manager API"
    return jsonify({"message": "success", "data": data}), 200


@my_app.route("/login", methods=["POST"])
def login():
    query = db.query(User).filter(User.username == request.form.get("username"))
    user = query.first()
    if user and user.check_password(request.form.get("password")):
        session["username"] = request.form.get("username")
        return jsonify({"message": "log in successful"}), 200
    else:
        logout()
        return jsonify({"message": "invalid username or password"}), 401


@my_app.route("/register", methods=["POST"])
def register():
    user = User(
        first_name=request.form.get("first_name"),
        last_name=request.form.get("last_name"),
        username=request.form.get("username"),
    )
    try:
        user.set_password(request.form.get("password"))
        user.save()
    except ValidationError as e:
        err = e.message
        return jsonify({"message": "error", "err": err}), 400
    return jsonify({"message": "Registered successfully"}), 201


@my_app.route("/logout")
def logout():
    session.pop("username", None)
    return jsonify({"message": "Log out successful"}), 200


@my_app.route("/user", methods=["GET", "POST"])
@login_required
def user():
    if request.method == "GET":
        users_obj = db.query(User)
        users = [user.as_dict() for user in users_obj]
        return jsonify({"message": "success", "users": users}), 200

    if request.method == "POST":
        username = request.form.get("username")
        user = User(
            first_name=request.form.get("first_name"),
            last_name=request.form.get("last_name"),
            username=username,
        )

        user.set_password(request.form.get("password"))
        try:
            user.save()
        except ValidationError as e:
            err = e.message
            return jsonify({"message": "error", "error": err}), 400
        user = db.query(User).filter(User.username == username).first()
        return jsonify({"message": "success", "user": user.as_dict()}), 200


@my_app.route("/owner", methods=["GET", "POST"])
@login_required
def owner():
    if request.method == "GET":
        owners_obj = db.query(Owner)
        owners = [owner.as_dict() for owner in owners_obj]
        return jsonify({"message": "success", "owners": owners}), 200

    if request.method == "POST":
        user_id = request.form.get("user_id")
        try:
            check_instance(User, user_id, "user")
            owner = Owner(user_id=user_id)
            owner.save()
        except ValidationError as e:
            err = e.message
            return jsonify({"message": "error", "error": err}), 400

        owner = db.query(Owner).order_by(Owner.id.desc()).first()
        return jsonify({"message": "success", "owner": owner.as_dict()}), 200


@my_app.route("/tenant", methods=["GET", "POST", "PUT", "DELETE"])
@login_required
def tenant():
    user_id = request.form.get("user_id")
    property_id = request.form.get("property_id")
    tenant_id = request.form.get("tenant_id")

    if request.method == "GET":
        tenants_obj = db.query(Tenant)
        tenants = [tenant.as_dict() for tenant in tenants_obj]
        return jsonify({"message": "success", "tenants": tenants}), 200

    elif request.method == "POST":
        try:
            check_instance(User, user_id, "user")
            check_instance(Property, property_id, "property")
            tenant = Tenant(user_id=user_id, property_id=property_id)
            tenant.save()
        except ValidationError as e:
            err = e.message
            return jsonify({"message": "error", "error": err}), 400
        tenant = db.query(Tenant).order_by(Tenant.id.desc()).first()
        return jsonify({"message": "success", "tenant": tenant.as_dict()}), 200

    elif request.method == "PUT":

        try:
            tenant = check_instance(Tenant, tenant_id, "tenant")
            check_instance(Property, property_id, "property")
            tenant.property_id = property_id
            tenant.save()
        except ValidationError as e:
            err = e.message
            return jsonify({"message": "error", "error": err}), 400
        tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        return jsonify({"message": "Success", "properties": tenant.as_dict()}), 201

    elif request.method == "DELETE":
        try:
            tenant.delete()
        except ValidationError as e:
            return jsonify({"message": "error", "error": e}), 400
        return jsonify({"message": "Success"}), 201


@my_app.route("/properties", methods=["GET", "POST", "PUT", "DELETE"])
@login_required
def properties():
    property_id = request.form.get("property_id")
    property_type = request.form.get("property_type")
    owner_id = request.form.get("owner_id")
    property_name = request.form.get("property_name")
    location = request.form.get("location")

    if request.method == "GET":
        properties_obj = db.query(Property)
        properties = [property_.as_dict() for property_ in properties_obj]
        return jsonify({"message": "success", "properties": properties}), 200

    elif request.method == "POST":
        try:
            check_instance(Owner, owner_id, "owner")
            property_ = Property(
                property_type=property_type,
                owner_id=owner_id,
                property_name=property_name,
                location=location,
            )
            property_.save()
        except ValidationError as e:
            err = e.message
            return jsonify({"message": "error", "error": err}), 400
        property_ = db.query(Property).order_by(Property.id.desc()).first()
        return jsonify({"message": "Success", "properties": property_.as_dict()}), 201

    elif request.method == "PUT":
        try:
            property_ = check_instance(Property, property_id, "property")
            if property_type:
                property_.property_type = property_type
            if owner_id:
                check_instance(Owner, owner_id, "owner")
                property_.owner_id = owner_id
            if location:
                property_.location = location
            if property_name:
                property_.property_name = property_name
            property_.save()
        except ValidationError as e:
            err = e.message
            return jsonify({"message": "error", "error": err}), 400
        property_ = db.query(Property).filter(Property.id == property_id).first()
        return jsonify({"message": "Success", "properties": property_.as_dict()}), 201

    elif request.method == "DELETE":
        try:
            property_ = check_instance(Property, property_id, "property")
            property_.delete()
        except ValidationError as e:
            err = e.message
            return jsonify({"message": "error", "error": err}), 400
        return jsonify({"message": "Success"}), 201


@my_app.route("/properties/<property_id>", methods=["GET"])
@login_required
def get_tenants(property_id):
    property_ = db.query(Property).filter(Property.id == property_id).first()
    property_details = property_.as_dict()
    property_details["tenants"] = [tenant.as_dict() for tenant in property_.tenants]
    return jsonify({"message": "Success", "properties": property_details}), 200
