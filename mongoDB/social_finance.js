var mongoose = require('mongoose');

console.log(process.env.MONGO_URL)

mongoose.connect(process.env.MONGO_URL);

var userSchema = new mongoose.Schema({
    source: String
}, { collection: 'social_finance' }
);

module.exports = { Mongoose: mongoose, UserSchema: userSchema }