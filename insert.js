/** @file insert.js */

/*
 *    Copyright (C) 2012 10gen Inc.
 *
 *    This program is free software: you can redistribute it and/or  modify
 *    it under the terms of the GNU Affero General Public License, version 3,
 *    as published by the Free Software Foundation.
 *
 *    This program is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU Affero General Public License for more details.
 *
 *    You should have received a copy of the GNU Affero General Public License
 *    along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

load("perfbench/namespace.js");
load("perfbench/utils.js");

mongo.namespace("mongo.benchmark.insert");

//Create options structure with some basic options
mongo.benchmark.insert.options = {
    name : "insert",
    description : { info : "insert new documents to the database" },
    Date : Date(),
    trials : []
};

// Add some more options. This method will either pick the default test parameters or from extra 
// options passed from the command line 
mongo.benchmark.insert.options = mongo.benchmark.utils.
                                           addMoreOptions(mongo.benchmark.insert.options);


// Add buildinfo 
mongo.benchmark.insert.options.buildInfo = mongo.benchmark.utils.buildInfo(
                                              mongo.benchmark.insert.options.testServerInfo.hostname);

mongo.benchmark.insert.doc =  {  
     "blob" : "MongoDB is an open source document-oriented " +
              "database system designed with scalability and developer.",
     "nestedDoc" : {
               "Firstname" : "David",
               "Lastname" : "Smith",
               "Address" : {
                    "Street" : "5th Av",
                    "City" : "New York"
               }
     },
     "list" : [
                "mongo new york city",
                "mongo new york city",
                "mongo new york city",
                "mongo new york city",
                "mongo new york city",
                "mongo new york city",
                "mongo new york city",
                "mongo new york city",
                "mongo new york city",
                "mongo new york city"
              ],
     "counter" : 0
};

mongo.benchmark.insert.generateOps = function() {
    
    var io = mongo.benchmark.insert.options;
    var numDocsInDB = mongo.benchmark.utils.findNumOfDocsInDB(io.testServerInfo.hostname,
                                                              io.dbprefix);
    var insertOps = [];
    // Generate ops evenly spread across dbs
    for (var i = 0; i < io.numberDatabases; i++) {
        var ns = io.dbprefix + i + ".sampledata";
        insertOps.push({ op : "insert", ns : ns, doc : mongo.benchmark.insert.doc, safe : true })
    }
    return { insertOps: insertOps };
}();


mongo.benchmark.insert.run = function() {
    
    var io = mongo.benchmark.insert.options;
    var mbrd = mongo.benchmark.result.defaults;

    if (mbrd.saveResult == "yes") {
        var conn = new Mongo(mbrd.resultServerInfo.hostname);
        var experimentResult = mongo.benchmark.utils.insert(conn, io);
    }
    
    for (var i = 0; i < io.numTrials; i++) {
        result = benchRun( { ops : mongo.benchmark.insert.generateOps.insertOps,
                             seconds : io.numSeconds,
                             parallel : io.numThreads,
                             host : io.testServerInfo.hostname } );
        
        if (mbrd.saveResult == "yes") {
            var query = { _id : experimentResult.Id };
            printjson(query);
            experimentResult.addToTrials(conn, query, result);
        }
        else {
            printjson(result);
        }
    }
};

// Run the insert test
mongo.benchmark.insert.run();

