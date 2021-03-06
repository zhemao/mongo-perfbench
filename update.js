/** @file update.js */
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

mongo.namespace("mongo.benchmark.update");


//Create options structure with some basic options
mongo.benchmark.update.options = {
  name : "update",
  description : { info : "updates such that document grows" },
  Date : Date(),
  trials : []
};

//Add some more options. This method will either pick the default test parameters or from extra 
//options passed from the command line 
mongo.benchmark.update.options = mongo.benchmark.utils.
                                         addMoreOptions(mongo.benchmark.update.options);


//Add buildinfo 
mongo.benchmark.update.options.buildInfo = mongo.benchmark.utils.buildInfo(
                                    mongo.benchmark.update.options.databaseURL);

mongo.benchmark.update.generateOps = function() {

    var uo = mongo.benchmark.update.options;
    
    var numDocsInDB = mongo.benchmark.utils.findNumOfDocsInDB(uo.databaseURL,
                                                              uo.dbprefix);

    var query = { _id : { "#RAND_INT" : [0, numDocsInDB] } };
    var updateOp = { $pushAll : { list : ["mongo san francisco",
                                          "mongo tokyo",
                                          "mongo paris",
                                          "mongo london",
                                          "mongo sydney"]} };
    var updateOps = [];
    // Generate ops evenly spread across dbs
    for (var i = 0; i < uo.numberDatabases; i++) {
        var ns = uo.dbprefix + i + ".sampledata";
        updateOps.push({ op : "update", ns : ns, query : query, update : updateOp })
    }
    return { updateOps: updateOps };
}();


mongo.benchmark.update.run = function() {
    
    var uo = mongo.benchmark.update.options;
    var mbrd = mongo.benchmark.result.defaults;
    var mbu = mongo.benchmark.utils;
    
    if (uo.saveResult == "yes") {
        var conn = new Mongo(uo.resultURL);
        uo = mbu.addOptionsFromDB(conn, uo);
        var experimentResult = mongo.benchmark.utils.insert(conn, uo);
    }
    

    for (var i = 0; i < uo.numTrials; i++) {
        result = benchRun( { ops : mongo.benchmark.update.generateOps.updateOps,
                             seconds : uo.numSeconds,
                             parallel : uo.numThreads,
                             host : uo.databaseURL } );
        
        if (uo.saveResult == "yes") {
            var query = { _id : experimentResult.Id };
            experimentResult.addToTrials(conn, query, result);
        }
        else {
            printjson(result);
        }
    }    
};

// Run the update test
mongo.benchmark.update.run();

