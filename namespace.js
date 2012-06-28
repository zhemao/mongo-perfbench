/** @file namespace.js */

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
