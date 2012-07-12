/** @file utils.js */

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
load("perfbench/default_values.js");

mongo.namespace("mongo.benchmark.utils");

mongo.benchmark.utils.experimentResult = new function() {
    this.Id = 0;
    
    var mbrd = mongo.benchmark.result.defaults;
    this.addToTrials = function(conn, query, trialDoc) {
        conn.getDB(mbrd.resultDB).getCollection(mbrd.resultColl).
                                 update(query, { $push : { trials : trialDoc } });
        return;
    };
}

mongo.benchmark.utils.findNumOfDocsInDB = function(host, dbName) {
    var conn = new Mongo(host);
    return conn.getDB(dbName+"0").getCollection("sampledata").count();
}

mongo.benchmark.utils.buildInfo = function(host) {
    var conn = new Mongo(host);
    return conn.getDB("admin").runCommand({buildInfo: 1});
}

mongo.benchmark.utils.insert = function(conn, doc) {
    var ut = mongo.benchmark.utils;
    var mbrd = mongo.benchmark.result.defaults;
    var ns = conn.getDB(mbrd.resultDB).getCollection(mbrd.resultColl);

    ns.insert(doc);
    ut.experimentResult.Id = ns._lastID;
    ns.update({_id: ut.experimentResult.Id}, 
              {$inc: { numThreads: doc.externThreads }, 
               $unset: { externThreads: 1 }});
    return ut.experimentResult;
}

mongo.benchmark.utils.addOptionsFromDB = function(conn, doc) {
    var mbrd = mongo.benchmark.result.defaults;
    var ns = conn.getDB(mbrd.resultDB).getCollection(mbrd.configColl);

    var config = null;
    
    if ( typeof suiteName !== "undefined" && suiteName !== null ){
        config = ns.findOne({"suiteName": suiteName});
    }

    if(config === null){
        config = mongo.benchmark.test.defaults;
    }
   
    doc.mongo = config.mongo;
    doc.dataSetFitsInRam = config.dataSetFitsInRam;
    doc.backgroundReadRunning = config.backgroundReadRunning;
    doc.backgroundSlowOpsRunning = config.backgroundSlowOpsRunning;
    doc.hardwareType = config.hardwareType;

    return doc;
}

// parse global or choose default value
mongo.benchmark.utils.addMoreOptions = function(type) {
 
    var mbtd = mongo.benchmark.test.defaults;
    var mbrd = mongo.benchmark.result.defaults;

    if (typeof globalExtraOption === "undefined" || globalExtraOption === null)
        return type;
    
    if (globalExtraOption.databaseURL == undefined)
        type.databaseURL = mbtd.databaseURL;
    else
        type.databaseURL = globalExtraOption.databaseURL;

    if (globalExtraOption.mongo == undefined)
        type.mongo = mbtd.mongo;
    else
        type.mongo = globalExtraOption.mongo;
    
    if (globalExtraOption.dbprefix == undefined)
        type.dbprefix = mbtd.dbprefix;
    else
        type.dbprefix = globalExtraOption.dbprefix;
    
    if (globalExtraOption.numTrials == undefined)
        type.numTrials = mbtd.numTrials;
    else
        type.numTrials = globalExtraOption.numTrials;
    
    if (globalExtraOption.numOps == undefined)
        type.numOps = mbtd.numOps;
    else
        type.numOps = globalExtraOption.numOps;
    
    if (globalExtraOption.numThreads == undefined)
        type.numThreads = mbtd.numThreads;
    else
        type.numThreads = globalExtraOption.numThreads;

    if (globalExtraOption.externThreads == undefined)
        type.externThreads = mbtd.externThreads;
    else
        type.externThreads = globalExtraOption.externThreads;

    if (globalExtraOption.numberDatabases == undefined)
        type.numberDatabases = mbtd.numberDatabases;
    else
        type.numberDatabases = globalExtraOption.numberDatabases;

    if (globalExtraOption.numSeconds == undefined)
        type.numSeconds = mbtd.numSeconds;
    else
        type.numSeconds = globalExtraOption.numSeconds;
    
    // --------------- begin testServerInfo ------------------------
    
    if (globalExtraOption.testServerInfo == undefined) {
        type.testServerInfo = mbtd.testServerInfo;
        return type;
    }
    else
        type.testServerInfo = globalExtraOption.testServerInfo;

    
    if (globalExtraOption.testServerInfo.hostname == undefined)
        type.testServerInfo.hostname = mbtd.testServerInfo.hostname;
    else
        type.testServerInfo.hostname = globalExtraOption.testServerInfo.hostname;
    
    if (globalExtraOption.testServerInfo.kernelName == undefined)
        type.testServerInfo.kernelName = mbtd.testServerInfo.kernelName;
    else
        type.testServerInfo.kernelName = globalExtraOption.testServerInfo.kernelName;
    
    if (globalExtraOption.testServerInfo.kernelRelease == undefined)
        type.testServerInfo.kernelRelease = mbtd.testServerInfo.kernelRelease;
    else
        type.testServerInfo.kernelRelease = globalExtraOption.testServerInfo.kernelRelease;
    
    if (globalExtraOption.testServerInfo.kernelVersion == undefined)
        type.testServerInfo.kernelVersion = mbtd.testServerInfo.kernelVersion;
    else
        type.testServerInfo.kernelVersion = globalExtraOption.testServerInfo.kernelVersion;
    
    if (globalExtraOption.testServerInfo.Platform == undefined)
        type.testServerInfo.Platform = mbtd.testServerInfo.Platform;
    else
        type.testServerInfo.Platform = globalExtraOption.testServerInfo.Platform;
    
    if (globalExtraOption.testServerInfo.OS == undefined)
        type.testServerInfo.OS = mbtd.testServerInfo.OS;
    else
        type.testServerInfo.OS = globalExtraOption.testServerInfo.OS;
    
    if (globalExtraOption.testServerInfo.fileSystem == undefined)
        type.testServerInfo.fileSystem = mbtd.testServerInfo.fileSystem;
    else
        type.testServerInfo.fileSystem = globalExtraOption.testServerInfo.fileSystem;
    
    // --------------- start resultServerInfo ------------------------
    
    if (globalExtraOption.saveResult == undefined)
        type.saveResult = mbrd.saveResult;
    else
        type.saveResult = globalExtraOption.saveResult;

    if (globalExtraOption.resultURL == undefined)
        type.resultURL = mbrd.resultURL;
    else
        type.resultURL = globalExtraOption.resultURL;
    
    if (globalExtraOption.resultDB == undefined)
        type.resultDB = mbrd.resultDB;
    else
        type.resultDB = globalExtraOption.resultDB;

    if (globalExtraOption.resultColl == undefined)
        type.resultColl = mbrd.resultColl;
    else
        type.resultColl = globalExtraOption.resultColl;

    if (globalExtraOption.configColl == undefined)
        type.configColl = mbrd.configColl;
    else
        type.configColl = globalExtraOption.configColl;

    return type;
    
}
