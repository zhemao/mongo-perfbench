/** @file default_values.js */

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

/*
 * Defines global default values for the test suite
 */

load("perfbench/namespace.js");

mongo.namespace("mongo.benchmark.result.defaults");
mongo.namespace("mongo.benchmark.test.defaults");

// The values can be overriden from the command line input
mongo.benchmark.result.defaults = {
    //some default values
    saveResult : "yes",
    resultURL: "127.0.0.1",
    resultDB : "experiment",
    resultColl : "results",
    configColl: "configs"
};

//The values can be overriden from the command line input
mongo.benchmark.test.defaults = {
    //some default values
    databaseURL : "127.0.0.1:27017",
    testServerInfo :  { hostname: "", kernelName: 12, kernelRelease: "",
                        kernelVersion: "", Platform: "", OS: "", fileSystem: ""
    },
    mongo : "single",
    dataSetFitsInRam : "yes",
    backgroundReadRunning: "no",
    backgroundSlowOpsRunning : "no",
    dbprefix : "small",
    hardwareType : "ec2-ebs",
    numTrials : 5,
    numOps : 60000,
    numThreads : 8,
    numberDatabases : 5,
    numSeconds : 120,
    externThreads: 0
};
