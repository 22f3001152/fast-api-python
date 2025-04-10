db = db.getSiblingDB('admin');

db.createUser({
  user: "staff",
  pwd: "password",
  roles: [
    {
      role: "readWrite",
      db: "staff_db"
    }
  ]
});

db = db.getSiblingDB('staff_db');
db.createCollection('course_collection');