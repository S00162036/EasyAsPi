var Connection = require('tedious').Connection;
var Request = require('tedious').Request;


//Take input from commandline - Python execution
var Input = parseInt(process.argv[2])
console.log(Input)

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
           queryDatabase(Input)
       }
   }
 );

function queryDatabase(Input)
   { console.log('Reading rows from the Table...' + Input);

       // Read all rows from table
     request = new Request(
          "Insert into CoinTable values ('" + Input + "', 23, 6, 2)",
             function(err, rowCount, rows) 
                {
                    console.log(rowCount + ' row(s) returned');
                    process.exit();
                }
            );

     request.on('row', function(columns) {
        columns.forEach(function(column) {
            console.log("%s\t%s", column.metadata.colName, column.value);
         });
             });
     connection.execSql(request);
   }