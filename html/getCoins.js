//var requirejs = require('requirejs');

requirejs.config({
    nodeRequire: require
});

define(function (require) {
    	var Connection = require('tedious').Connection;
	var Request = require('tedious').Request;
});

//var Connection = requirejs('tedious').Connection;
//var Request = requirejs('tedious').Request;

// Create connection to database
var config = 
   {
     userName: 'easyaspi',
     password: 'joshKeithglenn0',
     server: 'easyaspi2.database.windows.net',
     options: 
        {
           database: 'EasyAsPi'
           , encrypt: true
        }
   }
var connection = new Connection(config);

// Attempt to connect and execute queries if connection goes through
connection.on('connect', function(err) 
   {
     if (err) 
       {
          console.log(err)
       }
    else
       {
       console.log("Inside else")
           getTwo()
           getOne()
           getFifty()
           getTwenty()
           getTen()
       }
   }
 );

function getTwo()
   { console.log('Reading rows from the Table...');

       // Read all rows from table
     request = new Request(
          "SELECT Count(*) From CoinTable Where Value = 2",
             function(err, rowCount, rows) 
                {
                    console.log(rowCount + ' row(s) returned');
                    process.exit();
                }
            );
	$("#2Count").text(request)
     /*request.on('row', function(columns) {
        columns.forEach(function(column) {
            console.log("%s\t%s", column.metadata.colName, column.value);
         });
             });*/
     connection.execSql(request);
   }
   
function getOne()
   { console.log('Reading rows from the Table...');

       // Read all rows from table
     request = new Request(
          "SELECT Count(*) From CoinTable Where Value = 1",
             function(err, rowCount, rows) 
                {
                    console.log(rowCount + ' row(s) returned');
                    process.exit();
                }
            );
	$("#1Count").text(request)
     /*request.on('row', function(columns) {
        columns.forEach(function(column) {
            console.log("%s\t%s", column.metadata.colName, column.value);
         });
             });*/
     connection.execSql(request);
   }
   
function getFifty()
   { console.log('Reading rows from the Table...');

       // Read all rows from table
     request = new Request(
          "SELECT Count(*) From CoinTable Where Value = .5",
             function(err, rowCount, rows) 
                {
                    console.log(rowCount + ' row(s) returned');
                    process.exit();
                }
            );
	$("#50Count").text(request)
     /*request.on('row', function(columns) {
        columns.forEach(function(column) {
            console.log("%s\t%s", column.metadata.colName, column.value);
         });
             });*/
     connection.execSql(request);
   }
   
function getTwenty()
   { console.log('Reading rows from the Table...');

       // Read all rows from table
     request = new Request(
          "SELECT Count(*) From CoinTable Where Value = .2",
             function(err, rowCount, rows) 
                {
                    console.log(rowCount + ' row(s) returned');
                    process.exit();
                }
            );
	$("#20Count").text(request)
     /*request.on('row', function(columns) {
        columns.forEach(function(column) {
            console.log("%s\t%s", column.metadata.colName, column.value);
         });
             });*/
     connection.execSql(request);
   }
   
function getTen()
   { console.log('Reading rows from the Table...');

       // Read all rows from table
     request = new Request(
          "SELECT Count(*) From CoinTable Where Value = .1",
             function(err, rowCount, rows) 
                {
                    console.log(rowCount + ' row(s) returned');
                    process.exit();
                }
            );
	$("#10Count").text(request)
     /*request.on('row', function(columns) {
        columns.forEach(function(column) {
            console.log("%s\t%s", column.metadata.colName, column.value);
         });
             });*/
     connection.execSql(request);
   }
   