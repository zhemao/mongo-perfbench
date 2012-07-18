/** @file namespace.js */

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
 * Allows creating namespaces. The function is non-desctructive meaning that if a
 * namespace exists it won't be created.
 *
 * Allows all of these uses:
 * 1) var module2 = mongo.namespace("mongo.modules.modules2")
 * 2) // skip initial mongo
 *    mongo.namespace("modules.modules2")
 * 3) long namespace
 *    mongo.namespace("this.is.a.long.nested.property")
 */

var mongo = mongo || {}

mongo.namespace = function(nsString) {
    var parts = nsString.split('.');
        parent = mongo,
        i;
    // strip redundant leading global
    if (parts[0] === "mongo") {
        parts = parts.slice(1);
    }
    for (var i = 0; i < parts.length; i++) {
        // create a property if it doesn't exist
        if (typeof parent[parts[i]] === "undefined") {
            parent[parts[i]] = {};
        }
        parent = parent[parts[i]];
    }
    return parent;
}
