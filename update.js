/** @file update.js */

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
                                    mongo.benchmark.update.options.testServerInfo.hostname);

mongo.benchmark.update.generateOps = function() {

    var uo = mongo.benchmark.update.options;
    
    var numDocsInDB = mongo.benchmark.utils.findNumOfDocsInDB(uo.testServerInfo.hostname,
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
    
    if (mbrd.saveResult == "yes") {
        var conn = new Mongo(mbrd.resultServerInfo.hostname);
        var experimentResult = mongo.benchmark.utils.insert(conn, uo);
    }
    

    for (var i = 0; i < uo.numTrials; i++) {
        result = benchRun( { ops : mongo.benchmark.update.generateOps.updateOps,
                             seconds : uo.numSeconds,
                             parallel : uo.numThreads,
                             host : uo.testServerInfo.hostname } );
        
        if (mbrd.saveResult == "yes") {
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

