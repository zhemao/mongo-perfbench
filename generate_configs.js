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

// This script generates all the possible configurations that can be 
// used in the performance benchmarking.
// It looks pretty ugly, but there isn't really a better way of doing this.

hardwareopts = ["ec2-ebs", "ec2-instance", "baremetal"];
ramopts = [true, false];
rbgopts = [true, false];
sbgopts = [true, false];
mongodopts = ["single", "replSet"];

var i = 0;

// nasty-ass nested foreach loop
hardwareopts.forEach(function (hw) {
    ramopts.forEach(function (fitsinram) {
        rbgopts.forEach(function (bgRead) {
            sbgopts.forEach(function (bgSlow) {
                mongodopts.forEach(function (md) {
                    // set up the document
                    var config = {
                        // names are config0, config1, config2, etc.
                        suiteName: "config" + i,
                        dataSetFitsInRam: (fitsinram) ? "yes" : "no",
                        backgroundReadRunning: (bgRead) ? "yes": "no",
                        backgroundSlowOpsRunning: (bgSlow) ? "yes": "no",
                        mongo: md,
                        hardwareType: hw
                    };
                    db.configs.insert(config);
                    i++;
                });
            });
        });
    });
});
