/** @file insert.js */
/*
 * Copyright 2012 10gen, Inc.

 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 * 
 *  http://www.apache.org/licenses/LICENSE-2.0
 * 
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
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
                                              mongo.benchmark.insert.options.databaseURL);

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
    var numDocsInDB = mongo.benchmark.utils.findNumOfDocsInDB(io.databaseURL,
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
    var mbu = mongo.benchmark.utils;
    
    if (io.saveResult == "yes") {
        var conn = new Mongo(io.resultURL);
        io = mbu.addOptionsFromDB(conn, io);
        var experimentResult = mongo.benchmark.utils.insert(conn, io);
    }
    
    for (var i = 0; i < io.numTrials; i++) {
        result = benchRun( { ops : mongo.benchmark.insert.generateOps.insertOps,
                             seconds : io.numSeconds,
                             parallel : io.numThreads,
                             host : io.databaseURL } );
        
        if (io.saveResult == "yes") {
            var query = { _id : experimentResult.Id };
            experimentResult.addToTrials(conn, query, result);
        }
        else {
            printjson(result);
        }
    }
};

// Run the insert test
mongo.benchmark.insert.run();

