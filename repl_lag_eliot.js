N = 500;


function setup( t ) {

    if ( t.count() != N ) {
        t.drop();
        
        //var z = db.bar.findOne();
        var z = { x : 1 }
        
        for ( var i=0; i<N; i++ ) {
            z._id = i;
            t.insert( z );
        }
        
    }
}

dbs = []
for ( i=0; i<10; i++ ) {
    var x = db.getSisterDB( "foo" + i );
    setup( x.foo );
    dbs.push( x );
}

db.getLastError();

q = { _id : 0 };
inc = { x : 1 };

ops = []

for ( i=0; i<dbs.length; i++ ) {
    ops.push( { op : "update" , ns : dbs[i].foo.getFullName() , query : q , update : { $inc : inc } } );
}

while ( 1 ) {
    
    threads = [ 10 , 20 ]
    for ( var i=0; i<threads.length; i++ ) {
        res = benchRun( { ops : ops , seconds : 10 , parallel : threads[i] , host : db.getMongo().host } );
    }
    
}
