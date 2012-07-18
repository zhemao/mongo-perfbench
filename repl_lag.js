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

/* Test replication lag for prefetching code */

var numDocs = 10*1000*1000;

var ns1 = db.getSisterDB( "db1" ).foo;
var ns2 = db.getSisterDB( "db2" ).foo;
var ns3 = db.getSisterDB( "db3" ).foo;
var ns4 = db.getSisterDB( "db4" ).foo;

var doc = {
    "firstName": "John",
    "lastName" : "Smith",
    "age"      : 25,
    "address"  :
    {
        "streetAddress": "21 2nd Street",
        "city"         : "New York",
        "state"        : "NY",
        "postalCode"   : "10021"
    },
    "phoneNumber":
    [
        {
          "type"  : "home",
          "number": "212 555-1234"
        },
        {
          "type"  : "fax",
          "number": "646 555-4567"
        }
    ]
};

function ensureIndexInNS(ns) {
    ns.ensureIndex({firstName:1});
    ns.ensureIndex({lastName:1});
    ns.ensureIndex({id:1});
    ns.ensureIndex({age:1});
    ns.ensureIndex({"address.postalCode":1});
    ns.ensureIndex({"address.city":1});
}

while (1) {
    
    ops = [];
    ops.push( { op : "insert" , ns : ns1.getFullName(), doc : doc } );
    ops.push( { op : "insert" , ns : ns2.getFullName(), doc : doc } );
    ops.push( { op : "insert" , ns : ns3.getFullName(), doc : doc } );
    ops.push( { op : "insert" , ns : ns4.getFullName(), doc : doc } );
    
    // insert a bunch of docs.
    threads = [5];
    for (var i=0; i < threads.length; i++) {
        result = benchRun( { ops : ops , seconds : 900 , parallel : threads[i] , 
                             host : db.getMongo().host } );
        printjson(result);
    }
    
    // Create indexes
    ensureIndexInNS(ns1);
    ensureIndexInNS(ns2);
    ensureIndexInNS(ns3);
    ensureIndexInNS(ns4);
    
    var randomDoc1 = { id : { "#RAND_INT" : [ 0, numDocs ] }, "address.city" : "New York" };
    var randomDoc2 = { id : { "#RAND_INT" : [ 0, numDocs ] }, "lastName" : "Smith" };
    var randomDoc3 = { id : { "#RAND_INT" : [ 0, numDocs ] }, "firstName" : "John" };
    var randomDoc4 = { "age" : 25 };
    
    var randNumber = Math.floor((Math.random()*4));
    var queryDoc;
    if (randNumber == 1)
        queryDoc = randomDoc1;
    else if (randNumber == 2)
        queryDoc = randomDoc2;
    else if (randNumber == 3)
        queryDoc = randomDoc3;
    else if (randNumber == 3)
        queryDoc = randomDoc4;
    
    ops = [];
    ops.push( { op : "delete" , ns : ns1.getFullName(), query : queryDoc } );
    ops.push( { op : "delete" , ns : ns2.getFullName(), query : queryDoc } );
    ops.push( { op : "delete" , ns : ns3.getFullName(), query : queryDoc } );
    ops.push( { op : "delete" , ns : ns4.getFullName(), query : queryDoc } );
    
    // delete a bunch of docs.
    threads = [5];
    for (var i=0; i < threads.length; i++) {
        result = benchRun( { ops : ops , seconds : 30 , parallel : threads[i] , 
                             host : db.getMongo().host } );
        printjson(result);
    }
}


