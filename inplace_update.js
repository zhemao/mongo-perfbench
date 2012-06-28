/** @file inplaceupdate.js */

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

mongo.namespace("mongo.benchmark.inplaceupdate");

//Create options structure with some basic options
mongo.benchmark.inplaceupdate.options = {
    name : "inplaceUpdate",
    description : { info : "in place updates such that document doesn't grow" },
    Date : Date(),
    trials : []
};

// Add some more options. This method will either pick the default test parameters or from extra 
// options passed from the command line 
mongo.benchmark.inplaceupdate.options = mongo.benchmark.utils.
                                           addMoreOptions(mongo.benchmark.inplaceupdate.options);


// Add buildinfo 
mongo.benchmark.inplaceupdate.options.buildInfo = mongo.benchmark.utils.buildInfo(
                                      mongo.benchmark.inplaceupdate.options.testServerInfo.hostname);

mongo.benchmark.inplaceupdate.generateOps = function() {
    
    var uo = mongo.benchmark.inplaceupdate.options;
    
    var numDocsInDB = mongo.benchmark.utils.findNumOfDocsInDB(uo.testServerInfo.hostname,
            uo.dbprefix);

    var query = { _id : { "#RAND_INT" : [0, numDocsInDB] } };
    var incOp = { $inc : { counter : 1 } };
    var setOp = { $set : { blob : ".repoleved dna ytilibalacs htiw dengised metsys " +
    	                          "esabatad detneiro-tnemucod ecruos nepo na si BDognoM" } };
    
    var inplaceUpdateOps = [];
    // Generate ops evenly spread across dbs
    for (var i = 0; i < uo.numberDatabases; i++) {
        var ns = uo.dbprefix + i + ".sampledata";
        inplaceUpdateOps.push({ op : "update", ns : ns, query : query, update : incOp })
        inplaceUpdateOps.push({ op : "update", ns : ns, query : query, update : setOp })
    }
    return { inplaceUpdateOps: inplaceUpdateOps };
}();


mongo.benchmark.inplaceupdate.run = function() {
    
    var uo = mongo.benchmark.inplaceupdate.options;
    var mbrd = mongo.benchmark.result.defaults;
    
    if (mbrd.saveResult == "yes") {
        var conn = new Mongo(mbrd.resultServerInfo.hostname);
        var experimentResult = mongo.benchmark.utils.insert(conn, uo);
    }
  
    for (var i = 0; i < uo.numTrials; i++) {
        result = benchRun( { ops : mongo.benchmark.inplaceupdate.generateOps.inplaceUpdateOps,
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

// Run the inplaceupdate test
mongo.benchmark.inplaceupdate.run();

