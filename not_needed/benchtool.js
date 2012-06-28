        
/** @file benchtool.js */

/*
 *    Copyright (C) 2010 10gen Inc.
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
         
var options = {
    
    // dataset options
    numberDatabases : 4,
    documentSize : 128,
    fieldPerDocument : 3,
    numberOfIndices : 1,
    dataSetSize : 1024 * 1024,
    
    //experiment options
    resultDB : "exp",
    numberTrials : 4,
    numOpsRange : [ 2, 2 ],
    numThreadsRange : [ 2, 2 ],
    
    // How long to sleep between each set of ops
    sleepTimeRange : [ 0, 1000 ]
}


var runner = function( option ) {

    var dataPerDB = option.dataSetSize/option.numberDatabases;
    var numDocsPerDB = dataPerDB/option.documentSize;
    
    var conn = MongoRunner.runMongod({auth : "", port : 27017,  nojournal : "", noprealloc: ""});
    
    // load the data
    for(var i=0; i<option.numberDatabases; i++) {
 
        var db = conn.getDB("loadData" + i);
        db.foo.drop();
        var doc = {}
        
        for(var j=0; j < numDocsPerDB; j++) {
            for( var k=0; k<option.fieldPerDocument; k++) {
                doc["field" + k] = j
                //printjson(doc)
            }
            db.foo.insert( doc )
        }

        if( option.numberOfIndices <= option.fieldPerDocument ) {
            for(var m=0; m < option.numberOfIndices; m++) {
                var index = {}
                index["field" + k] = 1
                db.foo.ensureIndex( index );
            }
        }
    }
    
    var randomInt = function( bounds ) {
        return parseInt( Random.rand() * ( bounds[1] - bounds[0] ) + bounds[0] )
    }
    
    // generate ops
    var readops = []
    var writeops = []
    var updateops = []
    var numOps = randomInt( option.numOpsRange )
    var numThreads = randomInt( option.numThreadsRange )
    
    
    // Generate numOps * numConns ops even spread across dbs
    for( var i = 0; i < 100000; i++ ) {
    
        // read evenly across dbs
        var query = { field0 : randomInt( numDocsPerDB ) }
        var ns = "loadData" + (i % option.numberDatabases) + ".foo"
        readops.push({ op : "findOne", ns : ns, query : query })
        
        numDocsPerDB++;
        // inserts evenly across dbs
        for( var k=0; k<option.fieldPerDocument; k++) {
            doc["field" + k] = numDocsPerDB
        }
        var ns = "loadData" + (i % option.numberDatabases) + ".foo"
        writeops.push({ op : "insert", ns : ns, doc : doc, safe : true })
    }
    
    
    // remove the previous results DB
    var resultdb =  conn.getDB(option.resultDB);
    resultdb.dropDatabase()
    
    // now run benchRun and save the results
    for ( var i=0; i<option.numberTrials; i++) {
        res = benchRun( { parallel : numThreads ,
                          execInterleaved : true ,
                          ops : writeops
                         } )

        var coll = "trial"+i 
        resultdb.getCollection(coll).save( res )
        
        // Sleep over a randomized interval
        sleep( randomInt( option.sleepTimeRange ) )
    }           
}

runner( options );
