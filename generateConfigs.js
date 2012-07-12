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
