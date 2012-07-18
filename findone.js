/** @file findOne.js */

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

mongo.namespace("mongo.benchmark.findOne");

// Create options structure with some basic options
mongo.benchmark.findOne.options = {
    name : "findOne",
    description : { info : "findOne - 3/4 operations are reads on _id and 1/4 operations" +
    		               " are range queries on indexed field" },
    Date : Date(),
    trials : []
};

// Add some more options. This method will either pick the default test parameters or from extra 
// options passed from the command line 
mongo.benchmark.findOne.options = mongo.benchmark.utils.
                                           addMoreOptions(mongo.benchmark.findOne.options);


// Add buildinfo 
mongo.benchmark.findOne.options.buildInfo = mongo.benchmark.utils.buildInfo(
                                              mongo.benchmark.findOne.options.databaseURL);

mongo.benchmark.findOne.generateOps = function() {
    
    var fo = mongo.benchmark.findOne.options;
    var numDocsInDB = mongo.benchmark.utils.findNumOfDocsInDB(fo.databaseURL,
                                                              fo.dbprefix);
    
    var queryOnId = { _id : { "#RAND_INT" : [0, numDocsInDB] } };
    var rangeQuery = { blob : { $gt: " ", $lt: "mongo new" } };
    var findOneOps = [];
    for (var i = 0; i < fo.numberDatabases; i++) {
        var ns = fo.dbprefix + i + ".sampledata";
        findOneOps.push({ op : "findOne", ns : ns, query : queryOnId })
        findOneOps.push({ op : "findOne", ns : ns, query : rangeQuery })
        findOneOps.push({ op : "findOne", ns : ns, query : queryOnId })
        findOneOps.push({ op : "findOne", ns : ns, query : queryOnId })
    }
    return { findOneOps: findOneOps };
}();


mongo.benchmark.findOne.run = function() {
    
    var fo = mongo.benchmark.findOne.options;
    var mbrd = mongo.benchmark.result.defaults;
    var mbu = mongo.benchmark.utils;
    
    if (fo.saveResult == "yes") {
        var conn = new Mongo(fo.resultURL);
        fo = mbu.addOptionsFromDB(conn, fo);
        var experimentResult = mongo.benchmark.utils.insert(conn, fo);
    }
  
    for (var i = 0; i < fo.numTrials; i++) {
        result = benchRun( { ops : mongo.benchmark.findOne.generateOps.findOneOps,
                             seconds : fo.numSeconds,
                             parallel : fo.numThreads,
                             host : fo.databaseURL } );
        
        if (fo.saveResult == "yes") {
            var query = { _id : experimentResult.Id };
            experimentResult.addToTrials(conn, query, result);
        }
        else {
            printjson(result);
        }
    }
};

// Run the findOne test
mongo.benchmark.findOne.run();

