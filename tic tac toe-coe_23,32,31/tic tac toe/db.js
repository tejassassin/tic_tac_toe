var mysql = require('mysql');

var con = mysql.createConnection({
  host: "localhost",
  user: "nodeuser",
  password: "nodeuser@1234",
  database: "tictactoe"
});

con.connect(function(err) {
  if (err) throw err;
  con.query("SELECT * FROM moves", function (err, result, fields) {
    if (err) throw err;
    console.log(result);
  });
});