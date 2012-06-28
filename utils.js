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
    return ut.experimentResult;
}

// parse global or choose default value
mongo.benchmark.utils.addMoreOptions = function(type) {
 
    var mbtd = mongo.benchmark.test.defaults;
    if (globalExtraOption == undefined)
        return type;
    
    if (globalExtraOption.mongo == undefined)
        type.mongo = mbtd.mongo;
    else
        type.mongo = globalExtraOption.mongo;
    
    if (globalExtraOption.dataSetFitsInRam == undefined)
        type.dataSetFitsInRam = mbtd.dataSetFitsInRam;
    else
        type.dataSetFitsInRam = globalExtraOption.dataSetFitsInRam;
    
    if (globalExtraOption.otherOpsRunning == undefined)
        type.otherOpsRunning = mbtd.otherOpsRunning;
    else
        type.otherOpsRunning = globalExtraOption.otherOpsRunning;
    
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
        type.numOps = mbtd.numOps;
    
    if (globalExtraOption.numThreads == undefined)
        type.numThreads = mbtd.numThreads;
    else
        type.numThreads = mbtd.numThreads;
    
    if (globalExtraOption.numberDatabases == undefined)
        type.numberDatabases = mbtd.numberDatabases;
    else
        type.numberDatabases = mbtd.numberDatabases;

    if (globalExtraOption.numSeconds == undefined)
        type.numSeconds = mbtd.numSeconds;
    else
        type.numSeconds = mbtd.numSeconds;
    
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
    
    // --------------- end testServerInfo ------------------------
    
    
    return type;
    
}
