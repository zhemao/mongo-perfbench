/** @file findOne.js */

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
                                              mongo.benchmark.findOne.options.testServerInfo.hostname);

mongo.benchmark.findOne.generateOps = function() {
    
    var fo = mongo.benchmark.findOne.options;
    var numDocsInDB = mongo.benchmark.utils.findNumOfDocsInDB(fo.testServerInfo.hostname,
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
    
    if (mbrd.saveResult == "yes") {
        var conn = new Mongo(mbrd.resultServerInfo.hostname);
        var experimentResult = mongo.benchmark.utils.insert(conn, fo);
    }
  
    for (var i = 0; i < fo.numTrials; i++) {
        result = benchRun( { ops : mongo.benchmark.findOne.generateOps.findOneOps,
                             seconds : fo.numSeconds,
                             parallel : fo.numThreads,
                             host : fo.testServerInfo.hostname } );
        
        if (mbrd.saveResult == "yes") {
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

