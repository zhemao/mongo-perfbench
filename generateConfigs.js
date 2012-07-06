hardwareopts = ["ec2-ebs", "ec2-instance", "baremetal"];
ramopts = [true, false];
rbgopts = [true, false];
sbgopts = [true, false];
mongodopts = ["single", "replSet"];

hardwareopts.forEach(function (hw) {
    ramopts.forEach(function (fitsinram) {
        rbgopts.forEach(function (bgRead) {
            sbgopts.forEach(function (bgSlow) {
                mongodopts.forEach(function (md) {
                    var name = hw + ((fitsinram) ? "-inRAM" : "-notInRAM")
                                  + ((bgRead) ? "-readInBackground" : "")
                                  + ((bgSlow) ? "-slowOpsInBackground" : "")
                                  + "-" + md;

                    var config = {
                        suiteName: name,
                        datasetFitsInRam: (fitsinram) ? "yes" : "no",
                        backgroundReadRunning: (bgRead) ? "yes": "no",
                        backgroundSlowOpsRunning: (bgSlow) ? "yes": "no",
                        mongo: md,
                        hardware: hw
                    };
                    db.configs.insert(config);
                });
            });
        });
    });
});
