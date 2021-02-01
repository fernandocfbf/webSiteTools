var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var cors = require('cors')
require('dotenv').config()

var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');

const port = process.env.PORT || 3003


var app = express();


// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use(cors())
app.use(logger('dev'));
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ limit: "50mb", extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/users', usersRouter);


app.get('/', (req, res) => {
  res.send("API funcionando")
})

app.listen(port, () => {
  console.log("Backend is running on port ", port)

  if (process.env.NODE_ENV === undefined) {
    console.log("Environment: development")
  } else {
    console.log("Environment: production")
  }

})

module.exports = app;
